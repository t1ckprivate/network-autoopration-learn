import json
import netmiko
from netmiko import NetmikoTimeoutException, NetmikoAuthenticationException
import yaml
import glob
from draw_network_graph import draw_topology


# 名称统一函数
def normalize_name(name):
    return name.split('.')[0].upper()


# 连接设备并获取 LLDP
def config_device(device, device_info):
    try:
        print(f"SSH正在登录设备 {device} .......")

        with netmiko.ConnectHandler(**device_info) as conn:
            print(f"SSH已登录设备 {device}")
            print(f"正在获取 {device} 的 LLDP 信息...")

            ret = conn.send_command("show lldp neighbors")

            filename = f"display_lldp_{device}.txt"
            with open(filename, "w") as f:
                f.write(ret)

    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(f"SSH登录设备 {device} 失败:\n{error}")


# 读取设备信息
def get_connect_info(info_filename):
    try:
        with open(info_filename) as f:
            devices = json.load(f)

        for device in devices:
            config_device(device, devices[device])

    except FileNotFoundError:
        print("设备信息文件不存在")


# 解析 Cisco LLDP
def parse_cisco_lldp_neighbors(device_name, filename):
    topology = {}
    connect_dict = {}

    device_name = normalize_name(device_name)

    with open(filename) as f:
        lines = f.readlines()

    start = False

    for line in lines:
        if "Device ID" in line:
            start = True
            continue

        if not start:
            continue

        if line.strip() == "":
            continue

        parts = line.split()

        if len(parts) < 5:
            continue

        remote_device = normalize_name(parts[0])
        local_intf = parts[1]
        remote_intf = parts[-1]

        connect_dict[local_intf] = {remote_device: remote_intf}

    topology[device_name] = connect_dict
    print(f"解析 {device_name}: {topology}")

    return topology


# 汇总拓扑
def generate_topology_from_lldp(file_list, save_to_filename=None):
    topology = {}

    for filename in file_list:
        device_name = filename.split(".")[0].split("_")[-1]
        device_name = normalize_name(device_name)

        topo_part = parse_cisco_lldp_neighbors(device_name, filename)
        topology.update(topo_part)

    if save_to_filename:
        with open(save_to_filename, "w") as f:
            yaml.dump(topology, f, default_flow_style=False)

    return topology


# 转换拓扑（去重链路）
def transform_topology(topology_filename):
    with open(topology_filename) as f:
        raw_topology = yaml.safe_load(f)

    formatted_topology = {}
    seen_links = set()

    for l_device, peers in raw_topology.items():
        for l_int, remote in peers.items():
            r_device, r_int = list(remote.items())[0]

            # 构造无向链路标识（去重关键）
            link = tuple(sorted([
                (l_device, l_int),
                (r_device, r_int)
            ]))

            if link in seen_links:
                continue

            seen_links.add(link)
            formatted_topology[(l_device, l_int)] = (r_device, r_int)

    return formatted_topology


# 主程序
if __name__ == "__main__":

    # 抓 LLDP
    get_connect_info("cisco_devices.json")

    # 解析
    file_list = glob.glob("display_lldp_*")
    print("找到文件:", file_list)

    topology = generate_topology_from_lldp(
        file_list,
        save_to_filename="topology.yaml"
    )

    print("生成拓扑:", topology)

    # 画图
    formatted_topology = transform_topology("topology.yaml")
    draw_topology(formatted_topology)