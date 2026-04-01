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
    pip install ncclient
    pip install jinja2
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
    sys immediately
    int g1/0/9
    undo portswitch
    ip add ___.___.___.___  # 自己填ip
    q
    commit

    aaa
    local-user netconf password irreversible-cipher Huawei12#$
    local-user netconf service-type ssh
    local-user netconf level 3
    q
    commit

    stelnet server enable
    ssh user netconf authentication-type password
    ssh user netconf service-type snetconf
    user-interface vty 0 4
    authentication-mode aaa
    user privilege level 3
    q
    commit

    snetconf server enable
    netconf
    protocol inbound ssh port 830
    work-mode yang schema
    q
    commit
    ```
    > ⚠️ **注意 ！**
    > ---
    > 若在输入命令 *[*HUAWEI-netconf]work-mode yang schema*  
    > 出现 *Error: NETCONF agent is not enabled.*
    > 1. 请 **quit** 至 **系统视图（既[HUAWEI]）** 下  
    > 2. 输入 *commit* 并重新输入 *netconf* 进入 **netconf试图（既[HUAWEI-netconf]）** 后  
    > 3. 重新输入命令 *work-mode yang schema*
    >  
    > 这是因为，在该版本的CE12800上：  
    > - 设备在未保存配置前 NETCONF agent 可能未真正启用或未完成初始化，保存配置并重新进入 netconf 视图后即可正常使用相关命令。

### ② 运行代码！
- 运行三次，分别输入1、2、3
- 出现以下结果即实验成功
<p align="center">
  <img src="/images/6-Netconf/3.png" width="50%">
</p>
<p align="center"><em>VS code</em></p>

---
## 🎉 恭喜！
- 你完成了这章的内容！
