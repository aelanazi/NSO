# This is an investigations script outside of the services packages to help find the logic that has to be implemented in serviceBase under mef-common. 
# Once founded this logic can be integrated inside the serviceBase after LGI agrees. 
# Additional to this it's important to add it in the right order in the servicebase also XML template will have to be created to facilitate the actual command into Ciena.
# The following is an example of how to create such a template save it in seperate file under the follwoing name: mef-ring-protection.xml.

"""
<config-template 
    xmlns="http://tail-f.com/ns/config/1.0">
    <devices 
        xmlns="http://tail-f.com/ns/ncs">
        <device>
            <name>{$EDU-DEVICE}</name>
                 <config>
                   <ring-protection xmlns="http://tail-f.com/ned/cienacli-acos">
                     <virtual-ring>
                       <add>
                         <ring>
                           <name>{$VIRTUAL-RING-NAME}</name>
                           <vid>{$SVLAN-ID}</vid>
                         </ring>
                       </add>
                     </virtual-ring>
                   </ring-protection>
                </config>
        </device>
    </devices>
</config-template>


# suggest adding this configurations under __apply_base_service_config in service base somewhere after mef-cfm-performance is applied:
# The following snippets are requierd only:

#Check ring topology  #Abdel RING-Topology start!
    device_config = root.devices.device[device_name].config
    ringcheck = device_config.cienacli_acos__ring_protection.logical_ring.create.logical_ring_name
    is_ring_in_use = False
    for x in ringcheck:
        if x.name > 0:
            log.debug("is_ring_in_use: True \n RING-Name = ", x.name)
            is_ring_in_use = True
    if is_ring_in_use == True:

        nni_ports_list = []
        port_list = root.devices.device[device_name].config.cienacli_acos__port.set.port

        for key in port_list.keys():
            elem = port_list[key]
            if (str(elem.description).startswith("UPLINK_")):
                nni_ports_list.append((str(key[0])))
        log.debug("UPLinks NNIs found on device those are: ", nni_ports_list)
    else:
        log.debug("Cannot find RING-Topology used by: ", device_name)

    ringpath = root.devices.device[device_name].config.cienacli_acos__ring_protection.logical_ring.create.logical_ring_name
    for ring in ringpath:
        if ring.west_port in nni_ports_list:
            if ring.east_port in nni_ports_list:
                log.debug("lukt wel")
                virtringpath = root.devices.device[device_name].config.cienacli_acos__ring_protection.virtual_ring.create.virtual_ring_name
                for virtring in virtringpath:
                    virtringpath1 = root.devices.device[device_name].config.cienacli_acos__ring_protection.virtual_ring.create.virtual_ring_name[virtring.name].logical_ring
                    if virtringpath1 == ring.name:
                        log.debug(virtring.name)
                    tvars.add("VIRTUAL-RING-NAME", virtring.name)
                    template.apply("mef-ring-protection", tvars)

        else:
            log.debug("Cannot find Uplinks used by RING-Topology!")
    
    # Abdel RING-Topology done!


"""

# Here is the working and explanation if the scripts which can be tested offline outside of mef-common servicebase.

import ncs
with ncs.maapi.single_read_trans('admin', 'system') as t:
    root = ncs.maagic.get_root(t)
    #devices is hardcoded to ce0 which is equal to Ciena 5160-A in R&D Lab
    device_config = root.devices.device['ce0'].config
    #set the path to ring protection to check if this exsist on the device.
    ringcheck = device_config.cienacli_acos__ring_protection.logical_ring.create.logical_ring_name
    #set is_ring_in_use to false as default. 
    is_ring_in_use = False
    
    #loop over the ring topology path defined in ring check and check if there is a name created. If name contain any character then is_ring_in_use will be set to True so we can build future checking on it.
    for x in ringcheck:
        if x.name > 0:
            is_ring_in_use = True
    
    # check if is_ring_in_use is True if condition is met constract a empty list called nni_ports_list which will be the placeholder which will hold the NNI ports. 
    if is_ring_in_use == True:
        nni_ports_list = []
        
        #set the path to Ciena interfaces using the command port set port and loop over it in a for loop to lookup description which start with UPLINK_ when found add them to the nni_ports_list list then print them out.
        # If port description UPLINK_ cannot be found then a message will be printed Cannot find RING-Topology used by ce0.
        port_list = root.devices.device['ce0'].config.cienacli_acos__port.set.port
        for key in port_list.keys():
            elem = port_list[key]
            if (str(elem.description).startswith("UPLINK_")):
                nni_ports_list.append((str(key[0])))
        print ("UPLinks NNIs found on device those are", nni_ports_list)
    else:
        print("Cannot find RING-Topology used by ce0")
    
    # set new path to loop over it and lookup if NNI ports are used by logical_ring create, checking both ring-port east and ring-port west if they have can be found in nni_ports_list.
    ringpath = root.devices.device['ce0'].config.cienacli_acos__ring_protection.logical_ring.create.logical_ring_name
    for ring in ringpath:
        if ring.west_port in nni_ports_list:
            if ring.east_port in nni_ports_list:
                # if any or both NNI ports from nni_ports_list are found then used by west_port or east_port then set the following path to the virtual_ring to retrive 
                # the virtual_ring name which can be used later for SVLAN addition.
                virtringpath = root.devices.device['ce0'].config.cienacli_acos__ring_protection.virtual_ring.create.virtual_ring_name
            # Loop over virtual_ring_name and check if it contains the name of the create.logical_ring_name found used by the NNI ports. If condition is met then print the name of the logicical ring name.
            # Only if it match the condition that it's used by the logical ring. This virtring.name will be used by NSO XML template ti insert the SVLAN using the correct Virtual ring name. Otherwyse a message will be printed
            # Cannot find Uplinks used by RING-Topology!
            for virtring in virtringpath.keys():
                elem1 = virtringpath[virtring]
                virtringpath = root.devices.device['ce0'].config.cienacli_acos__ring_protection.virtual_ring.create.virtual_ring_name
                for virtring in virtringpath:
                    virtringpath1 = root.devices.device['ce0'].config.cienacli_acos__ring_protection.virtual_ring.create.virtual_ring_name[virtring.name].logical_ring
                    if virtringpath1 == ring.name:
                        print (virtring.name)
        else:
            print("Cannot find Uplinks used by RING-Topology!")

    