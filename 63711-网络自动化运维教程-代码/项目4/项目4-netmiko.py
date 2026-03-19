import json,netmiko
from netmiko import NetmikoTimeoutException
from netmiko import NetmikoAuthenticationException
import yaml
import glob
from draw_network_graph import draw_topology

def config_device(device,device_info):
    try:
        print("SSH正在登录设备 %s ......." % device )
        # netmiko连接设备
        with netmiko.ConnectHandler(**device_info) as conn:
            print("SSH已登录设备 %s " % device)
            print("SSH正在向 %s 设备发送命令" % device)
            ret = conn.send_command("display lldp neighbor brief")
            print(ret)
            lldp_filename = "display_lldp_" + device + ".txt"
            try:
                with open(lldp_filename,"w") as f:
                    f.write(ret)
            except Exception as e:
                print(e)
    except (NetmikoTimeoutException,
            NetmikoAuthenticationException) as error:
        print("SSH登录设备 %s 不成功。错误信息如下:\n %s " % (device,error))

def get_connect_info(info_filename):
    try:
        # 打开设备信息的json文件
        with open(info_filename) as f:
            # 读取json文件内容，返回字典
            devices = json.load(f)
            # print(devices)
            # 通过字典的健
            for key in devices.keys():
                # 调用函数config_device
                config_device(key,devices[key])
    except FileNotFoundError:
        print("the file does not exist.")

def parse_dis_lldp_neighbors(device_name,filename):
    list1 = []
    device_dict = {}
    connect_dict = {}
    neigh_dict = {}
    with open(filename) as f:
        content = f.readlines()
        for line in content:
            if line.startswith("<"):
                continue
            if line.startswith("["):
                continue
            if line.startswith("Local"):
                continue
            if line == "\n":
                continue
            lldp_info = line.strip().split(" ")
            for each in lldp_info:
                if each == "":
                    continue
                else:
                    list1.append(each)
            neigh_dict[list1[1]] = list1[2]
            connect_dict[list1[0]] = neigh_dict
            list1 = []
            neigh_dict = {}
        device_dict[device_name] = connect_dict
        print(device_dict)
        return device_dict

def generate_topology_from_lldp(list_of_files, save_to_filename=None):
    topology = {}
    for filename in list_of_files:
        #with open(filename) as f:
        device_name = filename.split(".")[0].split("_")[-1]
        topology.update(parse_dis_lldp_neighbors(device_name,filename))
    if save_to_filename:
        with open(save_to_filename, "w") as f_out:
            yaml.dump(topology, f_out, default_flow_style=False)
    return topology

def transform_topology(topology_filename):
    with open(topology_filename) as f:
        raw_topology = yaml.safe_load(f)
    formatted_topology = {}
    for l_device, peer in raw_topology.items():
        for l_int, remote in peer.items():
            r_device, r_int = list(remote.items())[0]
            if not (r_device, r_int) in formatted_topology:
                formatted_topology[(l_device, l_int)] = (r_device, r_int)
    return formatted_topology

# 主函数入口
if __name__ == "__main__":
    """
    filename = 'top_devices.json'
    get_connect_info(filename)
    f_list = glob.glob("display_lldp_*")
    print(f_list)
    print(generate_topology_from_lldp(f_list, save_to_filename="topology.yaml"))
    """
    formatted_topology = transform_topology("topology.yaml")
    draw_topology(formatted_topology)