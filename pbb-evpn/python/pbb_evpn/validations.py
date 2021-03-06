import ncs
import ncs.maapi as maapi
import ncs.maagic as maagic


def is_svlan_id_in_use(**link):
    """
    Check if a svlan-id is already in use on a device.
    :param link:               Dictionary contains all service data per link.
    :return: True if the svlan-id is in use, otherwise False.
    """
    m = maapi.Maapi()
    m.start_user_session('admin', 'system')
    t = m.start_read_trans()
    root = maagic.get_root(t)

    device = link['pe_device']
    a = [link['pe_port_1'], link['svlan_id']]
    values = '.'.join(str(v) for v in a)

    result = False
    if link['pe_port_type'] == "Bundle-Ether":
        bundle_config = root.ncs__devices.device[device].config.cisco_ios_xr__interface['Bundle-Ether-subinterface'][
            'Bundle-Ether']
        if values in bundle_config:
            result = True

    elif link['pe_port_type'] == "GigabitEthernet":
        gig_config = root.ncs__devices.device[device].config.cisco_ios_xr__interface['GigabitEthernet-subinterface'][
            'GigabitEthernet']
        if values in gig_config:
            result = True
    else:
        tengig_config = root.ncs__devices.device[device].config.cisco_ios_xr__interface['TenGigE-subinterface'][
            'TenGigE']
        if values in tengig_config:
            result = True

    return result
