""" This module handles with device ned type already implemneted in l2vpn device helper. this was used for testing.
import ncs
#with ncs.maapi.single_write_trans('admin', 'system') as t:    
#    t.set_elem2('Duli was here', '/ncs:devices/device{ce0}/description')    
#    t.apply()

with ncs.maapi.single_read_trans('admin', 'system') as t:
    root = ncs.maagic.get_root(t)    
    #desc = t.get_elem('/ncs:devices/device{ce0}/description')    
    #print("Description for device ce0 = %s" % desc)
    #print("\n \n")
    #device_config = root.devices.device['ce0'].config
    #device = "pre-region2-pe1, rd-region1-pe2, rd-region3-pe1"
    modules = root.devices.device['rd-region1-pe2'].module
    #modules1 = root.devices.device['rd-region1-pe2'].module.keys()
    #modules2 = root.devices.device['rd-region1-pe2'].platform.name
    #modules3 = root.devices.device['rd-region3-pe1'].platform.name 
    #print (modules)
    #print("\n \n")
    #print (modules2)
    #print (dir(modules))
    #print (modules1)
    #modules_list = []
    for x in modules.keys():
        #print (x)
        
        if str(modules.keys()[0]) == "{junos}":
            print ("test1")
            print str(modules.keys()[0])
            break   
        elif str(modules.keys()[2]) == "{tailf-ned-cisco-ios-xr}":
            print ("test2")
            print str(modules.keys()[2])
            break   
        else:
            print str(modules.keys()[0])
"""

### takes CSV files and read rows and import them to NSO ###

import ncs
import csv
import socket

def add_device(device_name, devicegroup, ip_addr, rule_list_name, rule_name, country, rule_name_main):
    """
    This function takes a device hostname as an input and adds that device into NSO.
    Then does an nslookup on the hostname
    This function uses 3 seperate transactions do to sequencing and default admin-state in NSO of locked.
    First Transaction: Adds the device and IP to add the device into the cDB
    Second Transaction: adds the port and creates the device-type/ NED info and unlocks the device.
    Third Transaction: Gets ssh keys, syncs-from and southbound-locks the device.
    """
    #ip_addr = socket.getaddrinfo(device_name,0,0,0,0)
    #root.devices.device[device_name].address = ip_addr[0][4][0]
    with ncs.maapi.single_write_trans('admin', 'system') as t:
        root = ncs.maagic.get_root(t)
        root.devices.device.create(device_name)
        root.devices.device[device_name].address = (ip_addr)
        root.devices.device[device_name].port = 22
        root.devices.device[device_name].device_type.cli.create()
        root.devices.device[device_name].device_type.cli.ned_id = "cienacli-acos"
        root.devices.device[device_name].device_type.cli.protocol = "ssh"
        root.devices.device[device_name].authgroup = "ciena"
        root.devices.device[device_name].state.admin_state = "unlocked"
        t.apply()
    with ncs.maapi.single_write_trans('admin', 'system') as t2:
        root = ncs.maagic.get_root(t2)
        #root.devices.device[device_name].ssh.fetch_host_keys()
        t2.apply()
    with ncs.maapi.single_write_trans('admin', 'system') as t1:
        root = ncs.maagic.get_root(t1)
        root.devices.device_group.create(devicegroup)
        root.devices.device_group[devicegroup].device_name.create([device_name])
        t1.apply()
    with ncs.maapi.single_write_trans('admin', 'system') as t3:
        root = ncs.maagic.get_root(t3)
        #root.devices.device_group[devicegroup].sync_from()
        #root.devices.device[device_name].sync_from()
        #root.devices.device[device_name].state.admin_state = "southbound-locked"
        root.nacm__nacm.rule_list.create(rule_list_name)
        root.nacm__nacm.rule_list[rule_list_name].group.create(["B2B-CE_%s" % (country)])
        root.nacm__nacm.rule_list[rule_list_name].rule.create([rule_name_main])
        root.nacm__nacm.rule_list[rule_list_name].rule.create([rule_name_main]).path = "/nacm/rule-list[name='B2B-CE_%s']/*" %(country)
        root.nacm__nacm.rule_list[rule_list_name].rule.create([rule_name_main]).access_operations = "*"
        root.nacm__nacm.rule_list[rule_list_name].rule.create([rule_name_main]).action = "permit"

        root.nacm__nacm.rule_list[rule_list_name].rule.create([rule_name])
        root.nacm__nacm.rule_list[rule_list_name].rule.create([rule_name]).path = "/devices/device[name='%s']" %(device_name)
        root.nacm__nacm.rule_list[rule_list_name].rule.create([rule_name]).access_operations = "*"
        root.nacm__nacm.rule_list[rule_list_name].rule.create([rule_name]).action = "permit"
        t3.apply()

with open('devices-lab.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    country = []
    device_name = []
    ip_addr = []
    
    for row in reader:
        country = row['Country']
        device_name = row['Hostname']
        ip_addr = row['Mgmt IP']
        devicegroup = ("B2B-EDU-"+(country))
        print ("Onboarding device %s into NSO...") % device_name
        print ("Adding device to group '%s %s'") % ((device_name) , (devicegroup))
        rule_name = ("t" + (country) + "_CENMS_" + (device_name))
        rule_name_main = ("t" + (country) + "-CENMS_nacm")
        rule_name_main_upper = ("t%s-CENMS_nacm") % (country.upper())
        rule_list_name = ("B2B-CE_" + (country))
        add_device(device_name, devicegroup, ip_addr, rule_list_name, rule_name, country, rule_name_main)

        # fetch-host-keys and sync-from does not require a transaction            
        # continue using the Maapi object
        with ncs.maapi.Maapi() as m:
            with ncs.maapi.Session(m, 'admin', 'system'):
                root = ncs.maagic.get_root(m)
                device = root.devices.device[device_name]
                print("Fetching SSH keys...")            
                output = device.ssh.fetch_host_keys()            
                print("Result: %s" % output.result)
                print("Syncing configuration...")

                output = device.sync_from()            
                print("Result: %s" % output.result)            
                if not output.result:                
                    print("Error: %s" % output.info)