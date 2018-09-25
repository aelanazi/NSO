# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service


# ------------------------
# SERVICE CALLBACK EXAMPLE
# ------------------------
class ServiceCallbacks(Service):

    # The create() callback is invoked inside NCS FASTMAP and
    # must always exist.
    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')
        
        customer_name = service.customer_name
        evi = service.evi

        links_data = []
        for link in service.link:
            link_data = {'pe_device': link.pe_device}
            link_data['pe_port_1'] = link.pe_port_1
            link_data['edge_i_sid'] = link.edge_i_sid
            link_data ['svlan_id'] = link.svlan_id
            links_data.append(link_data)
            for RT_IMPORT in link.route_target.rt_export:
                link_data['route_target_export'] = RT_IMPORT.asn_ip
                links_data.append(link_data)
                for RT_EXPORT in link.route_target.rt_import:
                    link_data['route_target_import'] = RT_EXPORT.asn_ip
                    links_data.append(link_data)

            self.log.info('Normalizing data for device {} for Customer {}'.format(link_data['pe_device'], customer_name))

        for index, link in enumerate(links_data):
            self.log.info('Configuring device {}'.format(link['pe_device']))
            vars = ncs.template.Variables()
            vars.add('CUSTOMER-NAME', customer_name)
            vars.add('EVI', evi)
            vars.add('PE-DEVICE', link['pe_device'])
            vars.add('PE-PORT-1', link['pe_port_1'])
            vars.add('EDGE-I-SID', link['edge_i_sid'])
            vars.add('SVLAN-ID', link['svlan_id'])
            vars.add('RT_EXPORT', link['route_target_export'])
            vars.add('RT_IMPORT', link['route_target_import'])
            template = ncs.template.Template(service)
            template.apply('pbb-evpn-base', vars)





    # The pre_modification() and post_modification() callbacks are optional,
    # and are invoked outside FASTMAP. pre_modification() is invoked before
    # create, update, or delete of the service, as indicated by the enum
    # ncs_service_operation op parameter. Conversely
    # post_modification() is invoked after create, update, or delete
    # of the service. These functions can be useful e.g. for
    # allocations that should be stored and existing also when the
    # service instance is removed.

    # @Service.pre_lock_create
    # def cb_pre_lock_create(self, tctx, root, service, proplist):
    #     self.log.info('Service plcreate(service=', service._path, ')')

    # @Service.pre_modification
    # def cb_pre_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')

    # @Service.post_modification
    # def cb_post_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')


# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Main RUNNING')

        # Service callbacks require a registration for a 'service point',
        # as specified in the corresponding data model.
        #
        self.register_service('pbb-evpn-servicepoint', ServiceCallbacks)

        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')
