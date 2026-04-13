> 😅 **提示**  
> ---
> 本节中的部分内容参考了覃老师提供的指导材料  
> 但原有指导内容过于简要，对关键原理与实际操作的说明不够完整  
> 因此本节在实践过程中对相关步骤与原理进行了补充、整理与扩展，以便更系统地理解相关技术  
> **具体如本README中的操作步骤所示**
>
> 若你的设备依旧有连接不到eNSP的问题  
> 请参阅：[GITHUB | t1ckprivate/network-autoopration-learn/tree/main/2-Telnetlib](https://github.com/t1ckprivate/network-autoopration-learn/tree/main/2-Telnetlib)
>
> 若**需要更多教程** 或 **发现本仓库有错误** 或 **需要帮助**  
> 请在本仓库[提交issue](https://github.com/t1ckprivate/network-autoopration-learn/issues) 或 私聊我 或 电邮联系[i@t1ck.me](mailto:i@t1ck.me)  

## 如何使用？
1. 详细阅读**操作步骤**中所给出的指导
2. 在IDE中使得终端位于./6-Netconf中，运行code.py

## 操作步骤
### 零 安装并配置环境
#### 使用python3.11并输入如下命令：
    pip install grpcio-tools
> 若你的虚拟机存在Python版本不兼容这些第三方库，请参阅：  
> [GITHUB | TICKUNLOCK - CentOS_network-autooperathon
](https://github.com/t1ckunlock/CentOS_network-autooperathon?tab=readme-ov-file)

#### 配置VMware网卡
1. 按下图打开虚拟网络适配器
2. 找到你的 **与eNSP互通的那张网卡**
3. 修改子网地址为 **自己想一个 / 老师给出的那个** ，此处*我*使用*172.16.100.0/24*

<p align="center">
  <img src="/images/6-Netconf/1.png" width="50%">
</p>
<p align="center"><em>VMware</em></p>

#### 配置eNSP的cloud
1. 绑定三张 **接口为GE** 的 **UDP** 网卡
2. 绑定你的那张VMware网卡 **接口为GE**
3. 设置端口映射
    - 入端口编号**始终为** **VMware网卡**
    - 出端口**分别为** **那三张UDP网卡**
<p align="center">
  <img src="/images/6-Netconf/2.png" width="50%">
</p>
<p align="center"><em>Cloud配置</em></p>

### ① 下载 / 配置拓扑
#### 若使用本仓库提供的拓扑：
1. 下载本仓库，并使用IDE打开./6-Netconf文件夹
2. 打开/topo中的topo.topo，**无需做任何设置，本仓库下的所有拓扑均已配置完成**
#### 若自行配置拓扑：
1. 复制并修改以下内容，粘贴至CE1,2,3窗口中：
    ```
    aaa
    local-user python password irreversible-cipher Huawei12#$
    local-user python user-group manage-ug
    local-user python service-type ssh
    q
    stelnet server enable
    user-interface vty 0 4
    authentication-mode aaa
    user privilege level 3
    protocol inbound ssh
    q
    ssh user python
    ssh user python authentication-type password
    ssh user python service-type stelnet

    telemetry
    destination-group dest1
    ipv4-address ___.___.___.___ port 20000 protocol grpc no-tls    # 自己填ip
    q

    sensor-group sensor1
    sensor-path huawei-devm:devm/cpuInfos/cpuInfo condition express op-field systemCpuUsage op-type gt op-value 1
    sensor-path huawei-devm:devm/memoryInfos/memoryInfo condition express op-field osMemoryUsage op-type gt op-value 6
    q

    subscription sub1
    sensor-group sensor1
    destination-group dest1
    ```


### ② 运行代码！
- 出现以下结果即实验成功
<p align="center">
  <img src="/images/7-Telemetry/1.png" width="50%">
</p>
<p align="center"><em>VS code</em></p>

---
## 🎉 恭喜！
- 你完成了这章的内容！
