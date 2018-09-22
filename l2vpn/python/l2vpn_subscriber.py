# -*- mode: python; python-indent: 4 -*-

import ncs
import ncs.maapi
import ncs.experimental

import _ncs

import fake_external_allocator


# ------------------------------------------------
# SUBSCRIBER ITERATOR OBJECT
# ------------------------------------------------
class AllocatorSubscriber(ncs.experimental.Subscriber):
    """This subscriber subscribes to changes in the..."""

    # custom initializer which gets called from the
    # constructor (__int__)
    def init(self):
        self.service_path = '/ncs:services/l2vpn:l2vpn'
        self.register(self.service_path, priority=100)

    # Initate your local state
    def pre_iterate(self):
        self.log.info('AllocatorSubscriber: pre_iterate')
        return []

    # Iterate over the change set
    def iterate(self, keypath, operation, oldval, newval, state):
        self.log.debug('iterate: {} {} old:{} new:{}'.format(operation, keypath, oldval, newval))

        if operation == ncs.MOP_CREATED and str(keypath[1:]) == self.service_path:
            state.append({'operation': 'create', 'path': str(keypath)})
            return ncs.ITER_STOP
        elif operation == ncs.MOP_DELETED and str(keypath[1:]) == self.service_path:
            path = str(keypath) + '/l2vpn:pw-id'
            try:
                with ncs.maapi.single_read_trans('admin', 'system', db=ncs.OPERATIONAL) as t:
                    val = t.get_elem(path)
                    state.append({'operation': 'delete', 'path': str(keypath), 'value': val})
            except Exception as e:
                self.log.error('Error in iterate: ', e)
            return ncs.ITER_STOP

        return ncs.ITER_RECURSE

    # This will run in a separate thread to avoid a transaction deadlock
    def post_iterate(self, state):
        self.log.info('AllocatorSubscriber: post_iterate, state=', state)

        for request in state:
            if request['operation'] == 'create':
                allocated_id = fake_external_allocator.allocate_id()
                self.log.info('Allocated pwid ', allocated_id)
                path = request['path'] + '/pw-id'

                with ncs.maapi.single_write_trans('admin', 'system', db=ncs.OPERATIONAL) as t:
                    t.set_elem(_ncs.Value(allocated_id, _ncs.C_UINT32), path)
                    t.apply()

                    path = request['path'] + '/reactive-re-deploy'
                    self.log.info('Redeploying ', path)
                    redeploy = ncs.maagic.get_node(t, path)
                    redeploy()
            elif request['operation'] == 'delete':
                fake_external_allocator.deallocate_id(request['value'])
                self.log.info('Deallocated pwid ', request['value'])

    # determine if post_iterate() should run
    def should_post_iterate(self, state):
        return state != []

    def cleanup(self):
        pass