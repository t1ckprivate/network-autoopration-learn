import ipaddress
import subprocess

# 该函数的功能是对每个 IP 地址发起 ping，并记录 ping 的结果
# 将能 ping 通的地址保存到 reachable 列表中，将不能 ping 通的地址保存到 unreachable 列表中
def ping_ip_addresses(ip_addresses):
    reachable = []
    unreachable = []

    for ip in ip_addresses:
        result = subprocess.run(
            # "-n"用于设置 ping 包数量，"-w"用于设置超时时间，单位是毫秒
            ["ping", "-n", "2", "-w", "1000", ip], capture_output=True
        )
        if result.returncode == 0:  
            reachable.append(ip)
        else:
            unreachable.append(ip)
    return reachable, unreachable

# 该函数的功能是将输入的 IP 地址段拆分成一个一个的 IP 地址
def convert_ranges_to_ip_list(ip_addresses):
    ip_list = []
    for ip_address in ip_addresses:
        if "-" in ip_address:
            start_ip, stop_ip = ip_address.split("-")
            if "." not in stop_ip:
                stop_ip = ".".join(start_ip.split(".")[:-1] + [stop_ip])
            start_ip = ipaddress.ip_address(start_ip)
            stop_ip = ipaddress.ip_address(stop_ip)
            for ip in range(int(start_ip), int(stop_ip) + 1):
                ip_list.append(str(ipaddress.ip_address(ip)))
        else:
            ip_list.append(str(ip_address))
    return ip_list

ip_addresses = []

# 读取文件，获取文件中的所有行
with open("1-PythonBasic/net.txt") as f:
    lines = f.readlines()
    for line in lines:
        # 去掉每行的'\n'
        ip_addresses.append(line.strip())

print("需要 ping 的 IP 地址是：", ip_addresses)

# 将地址段转换为一个一个的 IP 地址
addresses = convert_ranges_to_ip_list(ip_addresses)

# 批量 ping IP 地址，reach 中存放能 ping 通的地址，unreach 中存放不能 ping 通的地址
reach, unreach = ping_ip_addresses(addresses)

print("能 ping 通的 IP 地址有：\n", reach)
print("不能 ping 通的 IP 地址有：\n", unreach)