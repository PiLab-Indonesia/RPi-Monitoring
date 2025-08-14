"""
Simple SNMP helper using pysnmp to fetch common OIDs: sysName, sysDescr, sysUpTime
This module is optional and only used if pysnmp is installed and enabled in config.
"""
from pysnmp.hlapi import (
    SnmpEngine, UdpTransportTarget, CommunityData, ContextData,
    ObjectType, ObjectIdentity, getCmd
)

def get_snmp_basic(host: str, community: str = 'public', port: int = 161, timeout: int = 1, retries: int = 0):
    oids = [
        ('1.3.6.1.2.1.1.5.0', 'sysName'),
        ('1.3.6.1.2.1.1.1.0', 'sysDescr'),
        ('1.3.6.1.2.1.1.3.0', 'sysUpTime'),
    ]
    result = {}
    for oid, name in oids:
        iterator = getCmd(
            SnmpEngine(),
            CommunityData(community, mpModel=0),
            UdpTransportTarget((host, port), timeout=timeout, retries=retries),
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )
        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
        if errorIndication:
            result[name] = None
        elif errorStatus:
            result[name] = None
        else:
            for varBind in varBinds:
                # varBind is (ObjectIdentity, value)
                result[name] = str(varBind[1])
    return result
