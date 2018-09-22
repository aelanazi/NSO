import traceback

import ncs
from ncs.experimental import Query

#with ncs.maapi.single_write_trans('admin', 'system') as t:    
#    t.set_elem2('Duli was here', '/ncs:devices/device{ce0}/description')    
#    t.apply()

with ncs.maapi.single_read_trans('admin', 'system') as t:
    root = ncs.maagic.get_root(t) 
    #desc = t.get_elem('/ncs:devices/device{ce0}/description')    
    #print("Description for device ce0 = %s" % desc)
    #print("\n \n")
    device_config = root.devices.device['ce0'].config
    #ringcheck = device_config.cienacli_acos__ring_protection.logical_ring.create.logical_ring_name
    #is_ring_in_use = False
    #for x in ringcheck:
    #    print (x.name)
    #    if x.name > 0:
    #        print("Yes Yes yoh!")
    #        is_ring_in_use = True
    #lag_ports = [key[0].as_pyval() for key in service.lag.enniport.keys()]
    #service = ncs.maagic.get_node(t)
    print(dir(root))

    print(dir(service.ncs__services))
    print("Service above \n")
    print("Service above \n")
    print(dir(service.ncs__services.eaccess_eline_enni__eaccess_eline_enni))
    print("Service above")
    print(dir(service.lag))
    print(dir(service.dual_lag))

    ringcheck = device_config.cienacli_acos__ring_protection.logical_ring.create.logical_ring_name
    is_ring_in_use = False
    for x in ringcheck:
        if x.name > 0:
            #log.debug("is_ring_in_use: True", x.name)
            is_ring_in_use = True
    if is_ring_in_use == True:

        nni_ports_list = []
        port_list = root.devices.device['ce0'].config.cienacli_acos__port.set.port

        for key in port_list.keys():
            elem = port_list[key]
            if (str(elem.description).startswith("UPLINK_")):
                nni_ports_list.append((str(key[0])))
                #pass
        print ("UPLinks NNIs found on device those are", nni_ports_list)
    else:
        print("Cannot find RING-Topology used by ce0")

    ringpath = root.devices.device['ce0'].config.cienacli_acos__ring_protection.logical_ring.create.logical_ring_name
    for ring in ringpath:
        if ring.west_port in nni_ports_list:
            if ring.east_port in nni_ports_list:
                virtringpath = root.devices.device['ce0'].config.cienacli_acos__ring_protection.virtual_ring.create.virtual_ring_name
            for virtring in virtringpath.keys():
                elem1 = virtringpath[virtring]
                print ("lukt wel")
                virtringpath1 = root.devices.device['ce0'].config.cienacli_acos__ring_protection.virtual_ring.create.virtual_ring_name[virtring].logical_ring
                print (virtringpath1)
                if virtringpath1 == ring.name:
                    print (virtring)
        else:
            print("Cannot find Uplinks used by RING-Topology!")


            virtringpath = root.devices.device['ce0'].config.cienacli_acos__ring_protection.virtual_ring.create.virtual_ring_name
            for virtring in virtringpath:
                #virtringpath1 = root.devices.device['ce0'].config.cienacli_acos__ring_protection.virtual_ring.create.virtual_ring_name[virtring].logical_ring
                #print (virtringpath1)
                if virtring.name == ring.name:
                    print (virtring)