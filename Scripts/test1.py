import ncs
#with ncs.maapi.single_write_trans('admin', 'system') as t:    
#    t.set_elem2('Duli was here', '/ncs:devices/device{ce0}/description')    
#    t.apply()

with ncs.maapi.single_read_trans('admin', 'system') as t:
    root = ncs.maagic.get_root(t)    
    #desc = t.get_elem('/ncs:devices/device{ce0}/description')    
    #print("Description for device ce0 = %s" % desc)
    #print("\n \n")
    device_config = root.devices.device['ce0'].config
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
                virtringpath = root.devices.device['ce0'].config.cienacli_acos__ring_protection.virtual_ring.create.virtual_ring_name
                for virtring in virtringpath:
                    virtringpath1 = root.devices.device['ce0'].config.cienacli_acos__ring_protection.virtual_ring.create.virtual_ring_name[virtring.name].logical_ring
                    #print (virtringpath1)
                    #print (virtring.name)
                    if virtringpath1 == ring.name:
                        print (virtring.name)

        else:
            print("Cannot find Uplinks used by RING-Topology!")

    