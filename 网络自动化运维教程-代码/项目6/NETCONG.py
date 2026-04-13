from jinja2 import Template
from ncclient import manager
from ncclient import operations


# 将CE12800默认二层端口转成三层接口
def process_L3_template(interface_name, interface_status,
                        interface_ip, interface_mask):
    with open(template_path + "config_L3_int.xml") as f:
        netconf_template = Template(f.read())
    XML_out = netconf_template.render(interface_name=interface_name,
                                      interface_status=interface_status,
                                      interface_ip=interface_ip,
                                      interface_mask=interface_mask)
    return XML_out


# 处理1个接口运行OSPF
def process_OSPF_template_1_int(ospf_process_id,
                                ospf_area_num,
                                ospf_interface_1):
    with open(template_path + "config_ospf_1_int.xml") as f:
        netconf_template = Template(f.read())

    XML_out = netconf_template.render(ospf_process_id=ospf_process_id,
                                      ospf_area_num=ospf_area_num,
                                      ospf_interface_1=ospf_interface_1)
    return XML_out


# 处理2个接口运行OSPF
def process_OSPF_template_2_int(ospf_process_id,
                                ospf_area_num,
                                ospf_interface_1,
                                ospf_interface_2):
    with open(template_path + "config_ospf_2_int.xml") as f:
        netconf_template = Template(f.read())

    XML_out = netconf_template.render(ospf_process_id=ospf_process_id,
                                      ospf_area_num=ospf_area_num,
                                      ospf_interface_1=ospf_interface_1,
                                      ospf_interface_2=ospf_interface_2)
    return XML_out


# 处理5个接口运行OSPF
def process_OSPF_template_5_int(ospf_process_id,
                                ospf_area_num,
                                ospf_interface_1,
                                ospf_interface_2,
                                ospf_interface_3,
                                ospf_interface_4,
                                ospf_interface_5):
    with open(template_path + "config_ospf_5_int.xml") as f:
        netconf_template = Template(f.read())

    XML_out = netconf_template.render(ospf_process_id=ospf_process_id,
                                      ospf_area_num=ospf_area_num,
                                      ospf_interface_1=ospf_interface_1,
                                      ospf_interface_2=ospf_interface_2,
                                      ospf_interface_3=ospf_interface_3,
                                      ospf_interface_4=ospf_interface_5,
                                      ospf_interface_5=ospf_interface_5)
    return XML_out


# 创建VLAN
def process_VLAN_template(vlan_id):
    with open(template_path + "create_vlan.xml") as f:
        netconf_template = Template(f.read())

    XML_out = netconf_template.render(vlan_id=vlan_id)
    return XML_out


# 将接口加入VLAN
def process_VLAN_join_template(interface_name, vlan_id):
    with open(template_path + "join_interface_vlan.xml") as f:
        netconf_template = Template(f.read())

    XML_out = netconf_template.render(interface_name=interface_name,
                                      vlan_id=vlan_id)
    return XML_out


# 创建Eth-Trunk
def process_eth_trunk_template(Eth_Trunk_num,
                               link_type,
                               interface_name_1,
                               interface_name_2,
                               trunk_vlans):
    with open(template_path + "create_eth_trunk.xml") as f:
        netconf_template = Template(f.read())

    XML_out = netconf_template.render(Eth_Trunk_num=Eth_Trunk_num,
                                      link_type=link_type,
                                      interface_name_1=interface_name_1,
                                      interface_name_2=interface_name_2,
                                      trunk_vlans=trunk_vlans)
    return XML_out


# 创建vlanif接口
def process_create_vlanif_template(vlanif_num, vlanif_name,
                                   vlanif_mask, vlanif_ip):
    with open(template_path + "create_vlanif.xml") as f:
        netconf_template = Template(f.read())

    XML_out = netconf_template.render(vlanif_num=vlanif_num,
                                      vlanif_name=vlanif_name,
                                      vlanif_mask=vlanif_mask,
                                      vlanif_ip=vlanif_ip)
    return XML_out


def huawei_connect(host, port, user, password):
    return manager.connect(host=host,
                           port=port,
                           username=user,
                           password=password,
                           hostkey_verify=False,
                           device_params={'name': "huawei"},
                           allow_agent=False,
                           look_for_keys=False)

def config_SZ_CE1():
    print("\n--------Start config SZ_CE1---------\n")
    host_ip = '192.168.56.101'
    netconf_port = '830'
    netconf_user = 'netconf'
    netconf_password = 'Huawei12#$'

    # 连接SZ_CE1
    print("Netconf connect to %s ......", host_ip)
    m = huawei_connect(host=host_ip, port=netconf_port, user=netconf_user, password=netconf_password)

    # 配置SZ_CE1接口IP地址
    interface_list = [
        ["G1/0/1", "up", "10.2.26.1", "255.255.255.0"],
        ["G1/0/2", "up", "10.2.12.1", "255.255.255.0"],
        ["G1/0/3", "up", "10.2.23.1", "255.255.255.0"],
        ["G1/0/4", "up", "10.2.24.1", "255.255.255.0"],
        ["G1/0/5", "up", "10.2.25.1", "255.255.255.0"]
    ]
    print("Config interface IP address ......")
    for interface in interface_list:
        interface_name = interface[0]
        interface_status = interface[1]
        interface_ip = interface[2]
        interface_mask = interface[3]
        XML_out = process_L3_template(interface_name, interface_status, interface_ip, interface_mask)
        m.edit_config(target='running', config=XML_out)

    # 配置SZ_CE1 OSPF
    print("Add interface G1/0/3 into OSPF area 2 ......")
    XML_1 = process_OSPF_template_1_int(10, "0.0.0.2", "G1/0/3")
    m.edit_config(target='running', config=XML_1)

    print("Add interface G1/0/4 and G1/0/5 into OSPF area 0 ......")
    XML_2 = process_OSPF_template_2_int(10, "0.0.0.0", "G1/0/4", "G1/0/5")
    m.edit_config(target='running', config=XML_2)

    print("Add interface G1/0/1 and G1/0/2 into OSPF area 1 ......")
    XML_3 = process_OSPF_template_2_int(10, "0.0.0.1", "G1/0/1", "G1/0/2")
    m.edit_config(target='running', config=XML_3)

def config_CE2():
    print("\n--------Start config CE2------------\n")
    host_ip = '192.168.56.102'
    netconf_port = '830'
    netconf_user = 'netconf'
    netconf_password = 'Huawei12#$'
    vlans = [4, 5, 6, 7, 24]

    # 连接CE2
    print("Netconf connect to %s ......", host_ip)
    m = huawei_connect(host=host_ip, port=netconf_port, user=netconf_user, password=netconf_password)

    # 创建VLAN: 4,5,6,7,24
    print("Create vlans : 4,5,6,7,24 ......")
    for vlan in vlans:
        XML_VLAN = process_VLAN_template(vlan)
        m.edit_config(target='running', config=XML_VLAN)

    # 将 G1/0/4 加入VLAN 24
    print("Config G1/0/4 to vlans 24  ......")
    XML_VLAN_join = process_VLAN_join_template("G1/0/4", 24)
    m.edit_config(target='running', config=XML_VLAN_join)

    # 创建Eth-Trunk1，配置为trunk链路，成员接口的G1/0/2和G1/0/3,允许VLAN 4,5,6,7通过
    print("Config Eth-Trunk1 interface  ......")
    trunk_vlans = [4, 5, 6, 7]
    XML_eth_trunk = process_eth_trunk_template("Eth-Trunk1", "trunk", "G1/0/2", "G1/0/3", trunk_vlans)
    m.edit_config(target='running', config=XML_eth_trunk)

    # 创建 VLANif 4
    print("Create VLANif 4 interface  ......")
    XML_VLANIF4 = process_create_vlanif_template("4", "VLANIF 4", "255.255.255.0", "10.1.4.252")
    m.edit_config(target='running', config=XML_VLANIF4)

    # 创建 VLANif 5
    print("Create VLANif 5 interface  ......")
    XML_VLANIF5 = process_create_vlanif_template("5", "VLANIF 5", "255.255.255.0", "10.1.5.252")
    m.edit_config(target='running', config=XML_VLANIF5)

    # 创建 VLANif 6
    print("Create VLANif 6 interface  ......")
    XML_VLANIF6 = process_create_vlanif_template("6", "VLANIF 6", "255.255.255.0", "10.1.6.252")
    m.edit_config(target='running', config=XML_VLANIF6)

    # 创建 VLANif 7
    print("Create VLANif 7 interface  ......")
    XML_VLANIF7 = process_create_vlanif_template("7", "VLANIF 7", "255.255.255.0", "10.1.7.252")
    m.edit_config(target='running', config=XML_VLANIF7)

    # 创建 VLANif 24
    print("Create VLANif 24 interface  ......")
    XML_VLANIF24 = process_create_vlanif_template("24", "VLANIF 24", "255.255.255.0", "10.2.24.4")
    m.edit_config(target='running', config=XML_VLANIF24)

    # 在VLANif 4,VLANif 5,VLANif 6,VLANif 7,VLANif 24接口运行OSPF Area 0
    print("Config OSPF area 1  ......")
    XML_5 = process_OSPF_template_5_int(10, "0.0.0.0", "VLANif 4", "VLANif 5", "VLANif 6", "VLANif 7", "VLANif 24")
    m.edit_config(target='running', config=XML_5)


def config_CE3():
    print("\n--------Start config CE3------------\n")
    host_ip = '192.168.56.103'
    netconf_port = '830'
    netconf_user = 'netconf'
    netconf_password = 'Huawei12#$'
    vlans = [4, 5, 6, 7, 25]

    # 连接CE2
    print("Netconf connect to %s ......", host_ip)
    m = huawei_connect(host=host_ip, port=netconf_port, user=netconf_user, password=netconf_password)

    # 创建VLAN: 4,5,6,7,24
    print("Create vlans : 4,5,6,7,25 ......")
    for vlan in vlans:
        XML_VLAN = process_VLAN_template(vlan)
        m.edit_config(target='running', config=XML_VLAN)

    # 将 G1/0/5 加入VLAN 25
    print("Config G1/0/5 to vlans 25  ......")
    XML_VLAN_join = process_VLAN_join_template("G1/0/5", 25)
    m.edit_config(target='running', config=XML_VLAN_join)

    # 创建Eth-Trunk1，配置为trunk链路，成员接口的G1/0/2和G1/0/3,允许VLAN 4,5,6,7通过
    print("Config Eth-Trunk1 interface  ......")
    trunk_vlans = [4, 5, 6, 7]
    XML_eth_trunk = process_eth_trunk_template("Eth-Trunk1", "trunk", "G1/0/2", "G1/0/3", trunk_vlans)
    m.edit_config(target='running', config=XML_eth_trunk)

    # 创建 VLANif 4
    print("Create VLANif 4 interface  ......")
    XML_VLANIF4 = process_create_vlanif_template("4", "VLANIF 4", "255.255.255.0", "10.1.4.253")
    m.edit_config(target='running', config=XML_VLANIF4)

    # 创建 VLANif 5
    print("Create VLANif 5 interface  ......")
    XML_VLANIF5 = process_create_vlanif_template("5", "VLANIF 5", "255.255.255.0", "10.1.5.253")
    m.edit_config(target='running', config=XML_VLANIF5)

    # 创建 VLANif 6
    print("Create VLANif 6 interface  ......")
    XML_VLANIF6 = process_create_vlanif_template("6", "VLANIF 6", "255.255.255.0", "10.1.6.253")
    m.edit_config(target='running', config=XML_VLANIF6)

    # 创建 VLANif 7
    print("Create VLANif 7 interface  ......")
    XML_VLANIF7 = process_create_vlanif_template("7", "VLANIF 7", "255.255.255.0", "10.1.7.253")
    m.edit_config(target='running', config=XML_VLANIF7)

    # 创建 VLANif 25
    print("Create VLANif 25 interface  ......")
    XML_VLANIF25 = process_create_vlanif_template("25", "VLANIF 25", "255.255.255.0", "10.2.25.5")
    m.edit_config(target='running', config=XML_VLANIF25)

    # 在VLANif 4,VLANif 5,VLANif 6,VLANif 7,VLANif 24接口运行OSPF Area 0
    print("Config OSPF area 1  ......")
    XML_5 = process_OSPF_template_5_int(10, "0.0.0.0", "VLANif 4", "VLANif 5", "VLANif 6", "VLANif 7", "VLANif 25")
    m.edit_config(target='running', config=XML_5)


if __name__ == "__main__":
    # 模板文件所在的文件夹
    template_path = "./jinja2/"
    print("Please choose :")
    choose_num = """
    1 -> Config SZ_CE1
    2 -> Config CE2
    3 -> Config CE3
    \n
    """
    fun = input(choose_num)
    if fun == "1":
        config_SZ_CE1()
    elif fun == "2":
        config_CE2()
    elif fun == "3":
        config_CE3()
    else:
        print("input error,please choose again!")