from pysnmp.hlapi import (
    SnmpEngine,
    UsmUserData,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity,
    getCmd,
    bulkCmd,
    usmHMACSHAAuthProtocol,
    usmAesCfb128Protocol
)
import csv  

def use_getCmd(engine, userdata, target, context, oid_str, desc_oid):
    oid = ObjectIdentity(oid_str)
    obj = ObjectType(oid)
    g = getCmd(engine, userdata, target, obj)
    errorIndication, errorStatus, errorIndex, varBinds = next(g)
    for i in varBinds:
        print(desc_oid, i)

def use_bulkCmd(engine, userdata, target, context, oid_str, desc_oid):
    oid = ObjectIdentity(oid_str)
    obj = ObjectType(oid)
    g = bulkCmd(engine, userdata, target, context, 0, 50, obj, lexicographicMode = False)
    MAX_REPS = 500
    count = 0
    while(count < MAX_REPS):
        try:
            errorIndication, errorStatus, errorIndex, varBinds = next(g)
            for i in varBinds:
                print(desc_oid, i)
        except StopIteration:
            break
        count += 1
    
def SNMP_Init(ip):
    engine = SnmpEngine()
    userdata = UsmUserData("user01",
                           authKey = "Huawei@123", 
                           privKey = "Huawei@123",
                           authProtocol = usmHMACSHAAuthProtocol,
                           privProtocol = usmAesCfb128Protocol
                           )
    target = UdpTransportTarget((ip, 161))
    context = ContextData()
    return engine, userdata, target, context

if __name__ == "__main__":
    mgmt_ip = input("请输入管理设备IP地址：")
    engine, userdata, target, context = SNMP_Init(mgmt_ip)
    try:
        with open("oid_string.csv") as f:
            oid_info = csv.reader(f)
            for oid in oid_info:
                if oid[-1] == "S":
                    use_getCmd(engine, userdata, target, context, oid[0], oid[1])
                elif oid[-1] == "M":
                    use_bulkCmd(engine, userdata, target, context, oid[0], oid[1])
                else:
                    print("something error")
    except FileNotFoundError:
        print("the file dose not exist.")