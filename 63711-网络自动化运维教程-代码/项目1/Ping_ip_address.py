import ipaddress
import subprocess

# 该函数功能是对每个IP地址发起ping命令，并记录ping的结果。能ping通的地址保存到reachable列表，
# 不能ping通的地址保存到unreachable列表。
def ping_ip_addresses(ip_addresses):
    reachable = []
    unreachable = []

    for ip in ip_addresses:
        result = subprocess.run(
            # "-n"是ping包数量，"-w"是超时时间，单位是毫秒
            ["ping","-n", "2","-w","1000", ip], capture_output=True
        )
        if result.returncode == 0:
            reachable.append(ip)
        else:
            unreachable.append(ip)
    return reachable, unreachable

# 该函数功能是将输入的IP地址段拆分成一个一个的IP地址
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

#if __name__ == '__main()__':

ip_addresses = []

# 读取文件,获取文件中的所有行
with open("net.txt") as f:
    lines = f.readlines()
    for line in lines:
        # 去掉每行的'\n'
        ip_addresses.append(line.strip())

print("需要Ping的IP地址是：",ip_addresses)

# 将地址段转成一个一个的IP地址
addresses = convert_ranges_to_ip_list(ip_addresses)

# 批量ping每个IP地址，reach中存放能ping通的地址，unreach中存放不能ping通的地址，
reach,unreach = ping_ip_addresses(addresses)

print("能ping通的IP地址有：\n",reach)
print("不能ping通的IP地址有：\n",unreach)
