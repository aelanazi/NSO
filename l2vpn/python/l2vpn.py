# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service
import ncs.template
import device_helper

# ------------------------
# SERVICE CALLBACK EXAMPLE
# ------------------------
class ServiceCallbacks(Service):

    # The create() callback is invoked inside NCS FASTMAP and
    # must always exist.
    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        #vpn_name = str(service.name) + ',' + str(service.pw-id)
        self.log.info('Service create(service=', service._path, ')')
         
        vpn_name = service.name
        customer = service.customer
        pw_id = service.pw_id
        
        links_data = []
        for link in service.link:
            link_data = {'device': link.device}
            device_type = device_helper.get_device_type(root, link.device)
            self.log.info('Normalizing data for device {} of type {}'.format(link.device, device_type))
            device_type_container = getattr(link, device_helper.DEVICE_LOOKUP[device_type])
            self.log.info(device_type_container)

            link_data['intf-number'] = device_type_container.intf_number
            link_data['svlan-id'] = device_type_container.svlan_id
            link_data['loopback-address'] = device_helper.get_loopback_address(root, link.device, device_type, device_type_container.loopback_interface)
            links_data.append(link_data)

        self.log.info(link_data)

        for index, link in enumerate(links_data):
            self.log.info('Configuring device {}'.format(link['device']))
            tvars = ncs.template.Variables()
            tvars.add('SERVICE', vpn_name)
            tvars.add('CUSTOMER', customer)
            tvars.add('PW-ID', pw_id)
            tvars.add('SVLAN-ID', link['svlan-id'])
            tvars.add('DEVICE', link['device'])
            tvars.add('INTERFACE-ID', link['intf-number'])
            tvars.add('REMOTE-IP', links_data[1-index]['loopback-address'])
            template = ncs.template.Template(service)
            template.apply('l2vpn-template', tvars)
# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class L2vpn(ncs.application.Application):
    def __init__(self, *args, **kwargs):
        self.sub = None
        super(L2vpn, self).__init__(*args, **kwargs)

    def setup(self):
        # The application class sets up logging for us. Is is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('L2vpn RUNNING')

        # Service callbacks require a registration for a 'service point',
        # as specified in the corresponding data model.
        #
        self.register_service('l2vpn-servicepoint', ServiceCallbacks)

        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).
        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('L2vpn FINISHED')
