
import paramiko  # paramiko模块需要安装后使用
import time

def send_dis_cmd(ip, username, password, commands):
    try:
        # 创建SSH对象.使用Paramiko SSHClient()实例化SSH对象
        ssh = paramiko.SSHClient()

        # 允许连接未知主机.即新建立ssh连接时不需要再输入yes或no进行确认。
        # 自动添加主机名及主机密钥到本地HostKeys对象。
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 建立SSH会话连接
        ssh.connect(hostname=ip, username=username,
                    password=password, look_for_keys=False)
        print(f"SSH 已经登陆 {ip}")
        cli = ssh.invoke_shell()
        cli.send('screen-length 0 temporary\n')
        for cmd in commands_S:
            cli.send(cmd + "\n")
            # Python默认无间隔按顺序执行所有代码，在使用paramiko向交换机发
            # 送配置命令时候可能会遇到SSH响应不及时或者设备回显信息显示不
            # 全。此时，可以使用time模块下的sleep方法来人为暂停程序。
            time.sleep(1)
        # 抓取channel回显信息。invoke_shell()已经创建了一个channel逻辑通
        # 道。此前所有的输入输出的过程信息都在此channel中，获取此channel中
        # 所有信息，输出显示。调用cli.recv()，然后使用decode()进行对其解码，
        # 最后赋值给dis_cu。cli.recv(999999)作用是接收channel中的数据，数
        # 据最大量为999999 bytes。decode( )方法作用是以指定的编码格式解码
        # bytes对象，默认编码格式为utf-8
        dis_cu = cli.recv(999999).decode()
        # 打印回显内容
        print(dis_cu)
        ssh.close()
    except paramiko.ssh_exception.AuthenticationException:
        print(f"\n\tUser authentication failed for {ip}.\n")

if __name__ == "__main__":
    # 路由器上执行的运维命令
    commands_R = ["display version", "display patch-information",
                  "display clock", "display device",
                  "display health", "display memory-usage",
                  "display logbuffer"]
    # 交换机上执行的运维命令
    commands_S = ["display version", "display patch-information",
                  "display clock", "display device",
                  "display cpu-usage configuration",
                  "display memory-usage",
                  "display logbuffer summary"]
    # 网络设备地址信息，通过字典的键的第一字母表示是路由器还是交换机
    devices = {"R_SZ1": "10.2.12.1",
               "R_SZ2": "10.2.12.2",
               "S_S4": "10.3.1.254",
               "S_S1": "10.1.4.252",
               "S_S2": "10.1.4.253"
               }
    username = "python"
    password = "Huawei12#$"
    for key in devices.keys():
        ip = devices[key]
        if key.startswith("R"):  # 路由器执行commands_R
            send_dis_cmd(ip, username, password, commands_R)
        else:  # 交换机执行commands_S
            send_dis_cmd(ip, username, password, commands_S)
