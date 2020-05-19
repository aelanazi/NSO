import ncs
import ncs.maapi as maapi
import ncs.maagic as maagic


def get_bundle_id(**link):
    m = maapi.Maapi()
    m.start_user_session('admin', 'system')
    t = m.start_write_trans()
    root = maagic.get_root(t)
    id = 1
    agg_idx = 1
    device = link['pe_device']
    bundle_list = root.ncs__devices.device[device].config.cisco_ios_xr__interface.Bundle_Ether

    while id in bundle_list:
        agg_idx += 1
        id = agg_idx
    return id
