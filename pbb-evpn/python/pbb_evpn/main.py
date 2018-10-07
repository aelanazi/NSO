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
        serv_type = service.service_type
        serv = str(serv_type)
        serv_eline = "eline"
        serv_elan = "elan"
        serv_etree = "etree"

    	if serv_type == serv_eline:
            self.log.info("Provisioning Service type: ", serv_type)
            endpoints = service.eline.link
            num_end_points = len(endpoints)
            self.log.info("Number of endpoints: ", num_end_points)
            self.config_eline(root, service)
        if serv_type == serv_elan:
            self.log.info("Provisioning Service type: ", serv_type)
            endpoints = service.elan.link
            num_end_points = len(endpoints)
            self.log.info("Number of endpoints: ", num_end_points)
            self.config_elan(root, service)
        if serv_type == serv_etree:
            self.log.info("Provisioning Service type: ", serv_type)
            endpoints = service.etree.link
            num_end_points = len(endpoints)
            self.log.info("Number of endpoints: ", num_end_points)
            self.config_etree(root, service)

    def config_eline(self, root, service):
        customer_name = service.customer_name
        evi = service.evi
        links_data = []
        agg_idx = str(1)
        for link in service.eline.link:
            link_data = {'pe_device': link.pe_device}
            link_data['Bundle'] = "false"
            link_data['gig'] = "false"
            link_data['tengig'] = "false"
            link_data['edge_i_sid'] = link.edge_i_sid
            link_data ['svlan_id'] = link.svlan_id
            if link.interface_type == "GigabitEthernet":
                link_data['gig'] = "true"
                link_data['pe_port_1'] = link.pe_port.pe_gig_port
                link_data['pe_port_type'] = "GigabitEthernet"
            
            if link.interface_type == "TenGigabitEthernet":
                link_data['tengig'] = "true"
                link_data['pe_port_1'] = link.pe_port.pe_tengig_port
                link_data['pe_port_type'] = "TenGigabitEthernet"

            if link.nni_redundancy == "Dual-PE":
                link_data ['esi'] = link.Dual_PE.esi
    
            if link.nni_redundancy == "Protected":
                link_data['Bundle'] = "true"
                protect_name = "protect"
                protect = (protect_name+agg_idx)
                protect = []
                link_data['pe_port_type'] = "Bundle-Ether"
                for protect_loop in link.Bundle_Ether.pe_port:
                    protect.append(protect_loop.pe_port)
                link_data ['pe_port'] = protect
            
            rtx_name = "rtx"
            rtx = (rtx_name+agg_idx)
            rtx = []
            for RT_EXPORT in service.eline.route_target.rt_export:
                rtx.append(RT_EXPORT.asn_ip)
            link_data ['RT_EXPORT'] = rtx
            rtm_name = "rtx"
            rtm = (rtm_name+agg_idx)
            rtm = []
            for RT_IMPORT in service.eline.route_target.rt_import:
                rtm.append(RT_IMPORT.asn_ip)
            link_data ['RT_IMPORT'] = rtx

            agg_idx += str(1)
            links_data.append(link_data)
            self.log.info('Normalizing data for device {} for Customer {}'.format(link_data['pe_device'], customer_name))
        
        #self.log.info("Full list of dict: ", links_data)
            
        for index, link in enumerate(links_data):
            self.log.info('Configuring device {}'.format(link['pe_device']))
            vars = ncs.template.Variables()
            template = ncs.template.Template(service)
            vars.add('CUSTOMER-NAME', customer_name)
            vars.add('EVI', evi)
            vars.add('PE-DEVICE', link['pe_device'])
            vars.add('PE-PORT-1', link['pe_port_1'])
            vars.add('EDGE-I-SID', link['edge_i_sid'])
            vars.add('SVLAN-ID', link['svlan_id'])
            if link['pe_port_type'] == "Bundle-Ether":
                vars.add('INT-TYPE', '1')
                vars.add('PE-PORT-TYPE', link['pe_port_type'])
                
            else:
                vars.add('INT-TYPE', link['pe_port_1'])
                vars.add('PE-PORT-TYPE', link['pe_port_type'])

            template.apply('pbb-evpn-base-eline', vars)

            if link['Bundle'] == "true":
                for x in link['pe_port']:
                    vars.add('PE-PORT', x)
                    if link['gig'] == "true":
                        template.apply('pbb-evpn-lag-loop-eline-gig', vars)
                        
                    if link['tengig'] == "true":
                        template.apply('pbb-evpn-lag-loop-eline-tengig', vars)

            else:
                template.apply('pbb-evpn-interface-eline', vars)

            for rtx in link['RT_EXPORT']:
                vars.add('RT_EXPORT', rtx)
                for rtm in link['RT_IMPORT']:
                    vars.add('RT_IMPORT', rtm)
                    template.apply('pbb-evpn-rt-loop-eline', vars)
                    

    def config_elan(self, root, service):
        customer_name = service.customer_name
        evi = service.evi
        links_data = []
        Bundle = "false"
        gig = "false"
        tengig = "false"
        agg_idx = str(1)
        for link in service.elan.link:
            link_data = {'pe_device': link.pe_device}
            link_data['edge_i_sid'] = link.edge_i_sid
            link_data ['svlan_id'] = link.svlan_id
            if link.interface_type == "GigabitEthernet":
                gig = "true"
                link_data['pe_port_1'] = link.pe_port.pe_gig_port
                link_data['pe_port_type'] = "GigabitEthernet"

            if link.interface_type == "TenGigabitEthernet":
                tengig = "true"
                link_data['pe_port_1'] = link.pe_port.pe_tengig_port

        
            if link.nni_redundancy == "Dual-PE":
                link_data ['esi'] = link.Dual_PE.esi
    
            if link.nni_redundancy == "Protected":
                Bundle = "true"
                protect_name = "protect"
                protect = (protect_name+agg_idx)
                protect = []
                link_data['pe_port_type'] = "Bundle-Ether"
                for protect_loop in link.Bundle_Ether.pe_port:
                    protect.append(protect_loop.pe_port)
                link_data ['pe_port'] = protect
            
            rtx_name = "rtx"
            rtx = (rtx_name+agg_idx)
            rtx = []
            for RT_EXPORT in service.elan.route_target.rt_export:
                rtx.append(RT_EXPORT.asn_ip)
            link_data ['RT_EXPORT'] = rtx
            rtm_name = "rtx"
            rtm = (rtm_name+agg_idx)
            rtm = []
            for RT_IMPORT in service.elan.route_target.rt_import:
                rtm.append(RT_IMPORT.asn_ip)
            link_data ['RT_IMPORT'] = rtx

            agg_idx += str(1)
            links_data.append(link_data)
            self.log.info('Normalizing data for device {} for Customer {}'.format(link_data['pe_device'], customer_name))
        
        self.log.info("Full list of dict: ", links_data)

        for index, link in enumerate(links_data):
            self.log.info('Configuring device {}'.format(link['pe_device']))
            vars = ncs.template.Variables()
            template = ncs.template.Template(service)
            vars.add('CUSTOMER-NAME', customer_name)
            vars.add('EVI', evi)
            vars.add('PE-DEVICE', link['pe_device'])
            vars.add('PE-PORT-1', link['pe_port_1'])
            vars.add('EDGE-I-SID', link['edge_i_sid'])
            vars.add('SVLAN-ID', link['svlan_id'])
            #vars.add('PE-PORT-TYPE', link['pe_port_type'])
            if link['pe_port_type'] == "Bundle-Ether":
                vars.add('INT-TYPE', '1')
                vars.add('PE-PORT-TYPE', link['pe_port_type'])
            else:
                vars.add('INT-TYPE', link['pe_port_1'])
                vars.add('PE-PORT-TYPE', link['pe_port_type'])
            template.apply('pbb-evpn-base-elan', vars)

            if Bundle == "true":
                for x in link['pe_port']:
                    vars.add('PE-PORT', x)
                    if gig == "true":
                        template.apply('pbb-evpn-lag-loop-elan-gig', vars)
                    if tengig == "true":
                        template.apply('pbb-evpn-lag-loop-elan-tengig', vars)

            for rtx in link['RT_EXPORT']:
                vars.add('RT_EXPORT', rtx)
                for rtm in link['RT_IMPORT']:
                    vars.add('RT_IMPORT', rtm)
                    template.apply('pbb-evpn-rt-loop-elan', vars)
            

    def config_etree(self, root, service):
        customer_name = service.customer_name
        evi = service.evi
        links_data = []
        Bundle = "false"
        gig = "false"
        tengig = "false"
        agg_idx = str(1)
        for link in service.etree.link:
            link_data = {'pe_device': link.pe_device}
            link_data['edge_i_sid'] = link.edge_i_sid
            link_data ['svlan_id'] = link.svlan_id
            if link.interface_type == "GigabitEthernet":
                gig = "true"
                link_data['pe_port_1'] = link.pe_port.pe_gig_port
                link_data['pe_port_type'] = "GigabitEthernet"

            if link.interface_type == "TenGigabitEthernet":
                tengig = "true"
                link_data['pe_port_1'] = link.pe_port.pe_tengig_port

        
            if link.nni_redundancy == "Dual-PE":
                link_data ['esi'] = link.Dual_PE.esi
    
            if link.nni_redundancy == "Protected":
                Bundle = "true"
                protect_name = "protect"
                protect = (protect_name+agg_idx)
                protect = []
                link_data['pe_port_type'] = "Bundle-Ether"
                for protect_loop in link.Bundle_Ether.pe_port:
                    protect.append(protect_loop.pe_port)
                link_data ['pe_port'] = protect
            
            rtx_name = "rtx"
            rtx = (rtx_name+agg_idx)
            rtx = []
            for RT_EXPORT in service.etree.link.route_target.rt_export:
                rtx.append(RT_EXPORT.asn_ip)
            link_data ['RT_EXPORT'] = rtx
            rtm_name = "rtx"
            rtm = (rtm_name+agg_idx)
            rtm = []
            for RT_IMPORT in service.etree.link.route_target.rt_import:
                rtm.append(RT_IMPORT.asn_ip)
            link_data ['RT_IMPORT'] = rtx

            agg_idx += str(1)
            links_data.append(link_data)
            self.log.info('Normalizing data for device {} for Customer {}'.format(link_data['pe_device'], customer_name))

        self.log.info("Full list of dict: ", links_data)

        for index, link in enumerate(links_data):
            self.log.info('Configuring device {}'.format(link['pe_device']))
            vars = ncs.template.Variables()
            template = ncs.template.Template(service)
            vars.add('CUSTOMER-NAME', customer_name)
            vars.add('EVI', evi)
            vars.add('PE-DEVICE', link['pe_device'])
            vars.add('PE-PORT-1', link['pe_port_1'])
            vars.add('EDGE-I-SID', link['edge_i_sid'])
            vars.add('SVLAN-ID', link['svlan_id'])
            if link['pe_port_type'] == "Bundle-Ether":
                vars.add('INT-TYPE', '1')
                vars.add('PE-PORT-TYPE', link['pe_port_type'])
            else:
                vars.add('INT-TYPE', link['pe_port_1'])
                vars.add('PE-PORT-TYPE', link['pe_port_type'])

            template.apply('pbb-evpn-base-etree', vars)

            if Bundle == "true":
                for x in link['pe_port']:
                    vars.add('PE-PORT', x)
                    if gig == "true":
                        template.apply('pbb-evpn-lag-loop-elan-gig', vars)
                    if tengig == "true":
                        template.apply('pbb-evpn-lag-loop-elan-tengig', vars)

            for rtx in link['RT_EXPORT']:
                vars.add('RT_EXPORT', rtx)
                for rtm in link['RT_IMPORT']:
                    vars.add('RT_IMPORT', rtm)
                    template.apply('pbb-evpn-rt-loop-etree', vars)
            


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
