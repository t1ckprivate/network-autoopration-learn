import telnetlib              # telnetlib是Python标准模块，可直接使用
import time

def get_config_command(filename):
    ret = []                       # 创建一个空列表
    try:                           # 文件读写的异常处理
        with open(filename) as f:  # with语句处理文件，可自动关闭文件
            lines = f.readlines()  # readlines将文件每一行作为列表的一个元素
            for line in lines:     # 遍历readlines方法返回的列表
                ret.append(line.strip()) # 删除列表元素中的换行符，追加到列表
        return ret                       # 返回处理后的配置列表
    except FileNotFoundError:            # 如果没有配置文件，打印异常
        print("the file does not exist.")

def send_show_command(ip, username, password, commands):
    print("telnet %s",ip)
    with telnetlib.Telnet(ip) as tn:
        tn.read_until(b"Username:")
        tn.write(username.encode("ascii")+ b"\n")
        tn.read_until(b"Password:")
        tn.write(password.encode("ascii")+ b"\n")
        tn.write(b"system-view"+ b"\n")
        time.sleep(2)
        for command in commands:
            tn.write(command.encode("ascii") + b"\n")
            time.sleep(1)
        print(tn.read_very_eager().decode('ascii'))     # 接收回显
    print("设备 %s 已经配置完成 ！"%ip)
    time.sleep(1)

if __name__ == "__main__":
    devices_R = {                                     # 保存路由器IP地址
        "SZ1":"10.2.12.1",
        "SZ2":"10.2.12.2",
    }
    devices_S = {                                     # 保存交换机IP地址
        "S4":"10.3.1.254",
        "S1":"10.1.4.252",
        "S2":"10.1.4.253"
    }
    username = "python"
    password = "Huawei12#$"
    config_file_R = "config_6_1_R.txt"                # 路由器配置文件
    config_file_S = "config_6_1_S.txt"                # 交换机配置文件
    commands_S = get_config_command(config_file_S)    # 解析交换机配置命令
    commands_R = get_config_command(config_file_R)    # 解析路由器配置命令
    for device in devices_R.keys():                   # 配置路由器
        ip = devices_R[device]
        send_show_command(ip, username, password, commands_R)
    for device in devices_S.keys():                   # 配置交换机
        ip = devices_S[device]
        send_show_command(ip, username, password, commands_S)
