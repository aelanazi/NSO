# NSO
PBB-EVPN Usage:

This package contains three services types:
- E-LINE
- E-LAN
- E-Tree
The difference between those services is mainly the handling of the Route-Target behavior in the YANG and Python mapping Logic. i.e when selecting E-Line service the RT-Import and export is restricted to max 1 element and this is copied to all attachment circuits. In the case of E-LAN, you can have multiple RTs which will be configured on all attachment circuits. In the last case when using E-Tree there are two types RT one type for each HUB allowing multiple HUBs for redundancy and one type used for spokes, python will automatically import the HUB's RT types to all spokes and HUBs will import automatically all spokes RT's allowing E-Tree topology.

Furthermore, each service type has multiple interfaces to choose from:
- GigabitEthernet
- TenGigabitEthernet
- Bundle-Ethernet

In the case of Bundle, the sub-interfaces can be TenGig or Gig interfaces. When selecting Bundle-Ethernet or LACP Protected mode the Bundle ID is auto-generated by looking into the PE device for the next available BE ID to be used. This is made possible with python function called "get_bundle_id" in the main.py file.

Also, there is support for the following topology types:
- None # meaning single connection CE to PE
- Protected # meaning LACP Bundle-Interface connection from CE to PE 
- Dual-PE # meaning V-Shaped multiple connections connection from CE to dual-PE which will utilize ESI to support Active/Standby PE scenario.
