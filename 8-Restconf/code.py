import json
import requests
from requests.auth import HTTPBasicAuth
from collections import OrderedDict
import urllib3
from time import sleep

# 关闭SSL告警
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# 定义路由器接口IP地址
CSR1kv_1_int_ip = [
    {"Loopback0": {"address": "1.1.1.1", "mask": "255.255.255.255"}},
    {"GigabitEthernet2":{"address":"192.168.1.11","mask":"255.255.255.0"}},
    {"GigabitEthernet3":{"address":"10.1.13.1","mask":"255.255.255.0"}},
    {"GigabitEthernet4":{"address":"10.2.14.1","mask":"255.255.255.0"}}]

CSR1kv_2_int_ip = [
    {"Loopback0": {"address": "2.2.2.2", "mask": "255.255.255.255"}},
    {"GigabitEthernet2":{"address":"192.168.1.12","mask":"255.255.255.0"}},
    {"GigabitEthernet3":{"address":"10.3.23.2","mask":"255.255.255.0"}},
    {"GigabitEthernet4":{"address":"10.4.24.2","mask":"255.255.255.0"}}]

CSR1kv_3_int_ip = [
    {"Loopback0": {"address": "3.3.3.3", "mask": "255.255.255.255"}},
    {"GigabitEthernet2":{"address":"10.1.13.3","mask":"255.255.255.0"}},
    {"GigabitEthernet3":{"address":"10.3.23.3","mask":"255.255.255.0"}}]

CSR1kv_4_int_ip = [
    {"Loopback0": {"address": "4.4.4.4", "mask": "255.255.255.255"}},
    {"GigabitEthernet2":{"address":"10.2.14.4","mask":"255.255.255.0"}},
{"GigabitEthernet3":{"address":"10.4.24.4","mask":"255.255.255.0"}}]

# 定义路由器CSR1kv-1的OSPF请求消息体
CSR1kv_1_ospf_body = {
    "Cisco-IOS-XE-native:router": {
        "Cisco-IOS-XE-ospf:ospf": [
            {
                "id": 10,
                "area": [
                    {
                        "id": 10,
                        "stub": {}
                    },
                    {
                        "id": 20,
                        "stub": {}
                    }
                ],
                "router-id": "1.1.1.1",
                "network": [
                    {
                        "ip": "1.1.1.1",
                        "mask": "0.0.0.0",
                        "area": 0
                    },
                    {
                        "ip": "10.1.13.1",
                        "mask": "0.0.0.0",
                        "area": 10
                    },
                    {
                        "ip": "10.2.14.1",
                        "mask": "0.0.0.0",
                        "area": 20
                    },
                    {
                        "ip": "192.168.1.11",
                        "mask": "0.0.0.0",
                        "area": 0
                    }
                ]
            }
        ]
    }
}
# 定义路由器CSR1kv-2的OSPF请求消息体
CSR1kv_2_ospf_body = {
    "Cisco-IOS-XE-native:router": {
        "Cisco-IOS-XE-ospf:ospf": [
            {
                "id": 10,
                "area": [
                    {
                        "id": 10,
                        "stub": {}
                    },
                    {
                        "id": 20,
                        "stub": {}
                    }
                ],
                "router-id": "2.2.2.2",
                "network": [
                    {
                        "ip": "2.2.2.2",
                        "mask": "0.0.0.0",
                        "area": 0
                    },
                    {
                        "ip": "10.3.23.2",
                        "mask": "0.0.0.0",
                        "area": 10
                    },
                    {
                        "ip": "10.4.24.2",
                        "mask": "0.0.0.0",
                        "area": 20
                    },
                    {
                        "ip": "192.168.1.12",
                        "mask": "0.0.0.0",
                        "area": 0
                    }
                ]
            }
        ]
    }
}
# 定义路由器CSR1kv-3的OSPF请求消息体
CSR1kv_3_ospf_body = {
    "Cisco-IOS-XE-native:router": {
        "Cisco-IOS-XE-ospf:ospf": [
            {
                "id": 10,
                "area": [
                    {
                        "id": 10,
                        "stub": {}
                    }
                ],
                "router-id": "3.3.3.3",
                "network": [
                    {
                        "ip": "3.3.3.3",
                        "mask": "0.0.0.0",
                        "area": 10
                    },
                    {
                        "ip": "10.1.13.3",
                        "mask": "0.0.0.0",
                        "area": 10
                    },
                    {
                        "ip": "10.3.23.3",
                        "mask": "0.0.0.0",
                        "area": 10
                    }
                ]
            }
        ]
    }
}
# 定义路由器CSR1kv-4的OSPF请求消息体
CSR1kv_4_ospf_body = {
    "Cisco-IOS-XE-native:router": {
        "Cisco-IOS-XE-ospf:ospf": [
            {
                "id": 10,
                "area": [
                    {
                        "id": 20,
                        "stub": {}
                    }
                ],
                "router-id": "4.4.4.4",
                "network": [
                    {
                        "ip": "4.4.4.4",
                        "mask": "0.0.0.0",
                        "area": 20
                    },
                    {
                        "ip": "10.2.14.4",
                        "mask": "0.0.0.0",
                        "area": 20
                    },
                    {
                        "ip": "10.4.24.4",
                        "mask": "0.0.0.0",
                        "area": 20
                    }
                ]
            }
        ]
    }
}

def configure_ip_address(interface, ip):
    if interface == "Loopback0":
        # 如果创建换回接口，接口类型为"iana-if-type:softwareLoopback"
            interface_type = "iana-if-type:softwareLoopback"
            print("    正在路由器上配置 %s 接口......"%interface)
    else:
        # 如果创建以太接口，接口类型为'iana-if-type:ethernetCsmacd'
        interface_type = 'iana-if-type:ethernetCsmacd'
        print("    正在路由器上配置 %s 接口......" % interface)
        # 组成URL
        url = url_base + "/data/ietf-interfaces:interfaces/interface={i}".format(i=interface)
        print("    "+ url)

    # 请求消息体。OrderedDicts方法用于保证元素的顺序
        body = OrderedDict([('ietf-interfaces:interface',
                             OrderedDict([
                                 ('name', interface),
                                 ('type', interface_type),
                                 ('ietf-ip:ipv4',
                                  OrderedDict([
                                      ('address', [OrderedDict([
                                          ('ip', ip["address"]),
                                          ('netmask', ip["mask"])
                                      ])]
                                       )
                                  ])
                                  ),
                             ])
                             )])

        # 发送PUT请求配置接口
        response = requests.put(url,auth=(USER, PASS),
                                headers=headers,
                                verify=False,
                                json=body
                                )
        sleep(0.5)

def config_interface_ip(interface_ip):
    for interface in interface_ip:
        for key in interface:
            configure_ip_address(key, interface[key])

def configure_ospf(ospf_body):
    url = url_base + "/data/Cisco-IOS-XE-native:native/router"
    print("    " + url)
    # 发送PUT请求
    response = requests.put(url, auth=(USER, PASS),
                            headers=headers,
                            verify=False,
                            data=json.dumps(ospf_body)
                            )

if __name__ == "__main__":
    # 登陆路由器的用户名和密码
    USER = 'cisco'
    PASS = 'cisco'

    # 添加HTTP head信息，使用 yang+json 作为数据格式
    headers = {'Content-Type': 'application/yang-data+json',
               'Accept': 'application/yang-data+json'}
	# 定义设备信息。包括路由器管理IP地址，接口以及OSPF配置信息
    device_conf_info =[
        ["192.168.201.101",CSR1kv_1_int_ip,CSR1kv_1_ospf_body],
        ["192.168.201.102",CSR1kv_2_int_ip,CSR1kv_2_ospf_body],
        ["192.168.201.103",CSR1kv_3_int_ip,CSR1kv_3_ospf_body],
        ["192.168.201.104",CSR1kv_4_int_ip,CSR1kv_4_ospf_body]
    ]
	# 遍历设备信息
for device in device_conf_info:
    # 获取设备管理IP地址
        host = device[0]
        url_base = "https://{host}/restconf".format(host=host)

        print("在路由器 %s 上配置接口IP地址........."%host)
        # 获取设备接口配置信息
        interface_ip = device[1]
        # 调用函数config_interface_ip配置设备IP地址
        config_interface_ip(interface_ip)
        print("路由器 %s 上接口IP地址配置完毕........." % host)

        print("在路由器 %s 上配置OSPF........." %host)
        # 获取设备的OSPF配置消息体
        ospf_body = device[2]
        # 调用函数configure_ospf配置设备OSPF
        configure_ospf(ospf_body)
        print("路由器 %s 上OSPF配置完毕........." % host)
