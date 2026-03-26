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
> 若需要更多教程 或发现本仓库有错误  
> 请在本仓库[提交issue](https://github.com/t1ckprivate/network-autoopration-learn/issues) 或 私聊我 或电邮联系[i@t1ck.me](mailto:i@t1ck.me)  

> ❗警告
> ---  
> 本节为便于演示，插入了部分示例图  
> **不建议**直接用于个人实验报告中  
> 若自行引用或使用，由使用者自行承担相关责任  

## 如何使用？
1. 详细阅读**操作步骤**中所给出的指导
2. 在IDE中使得终端位于./5-PySNMP中，运行code.py

## 操作步骤
### 零 安装环境
> ⚠️ **注意 ！**
> ---
> 新版 pysnmp（7.x） 更改了 hlapi 的结构，会报:ImportError: cannot import name 'SnmpEngine'  
> pyans1（0.6）过新，不支持pysnmp（4.4）
> python3.12不支持pysnmp（4.4），建议使用python3.11  
#### 使用python3.11并输入如下命令：
    ```
    pip install pysnmp==4.4.12
    pip install pyasn1==0.4.8
    pip install pysnmp-mibs
    ```
---
### ① 下载 / 配置拓扑
#### 若使用本仓库提供的拓扑：
1. 下载本仓库，并使用IDE打开./5-PySNMP文件夹
2. 打开topo中的pro3.topo，**无需做任何设置，本仓库下的所有拓扑均已配置完成**
#### 若自行配置拓扑：
- 复制 ./5-PySNMP/commands/1-SZ1,SZ2 中的内容，粘贴至SZ1、SZ2窗口中  
  
<p align="center">
  <img src="/images/5-PySNMP/SZ1.png" width="50%">
</p>
<p align="center"><em>SZ1</em></p>

<p align="center">
  <img src="/images/5-PySNMP/SZ2.png" width="50%">
</p>
<p align="center"><em>SZ2</em></p>

---
### ② 下载并安装 **MIB Browser**
- 此处我使用的版本为官网下载的Version 2025a (published 23-Apr-2025)，并使用evaluation license激活
    > 详情请参阅：  
    > [MG-SOFT | Download MG-SOFT's Software Products](https://www.mg-soft.si/download.html?product=mibbrowser)  
    > [MG-SOFT | Request a 30-day evaluation license key](https://www.mg-soft.com/evalKeyReq.html)

- 也可自行搜索 **绿色版**
    > 详情请参阅：  
    > [GITCODE | MG-SOFTMIBBrowserv10KEY资源介绍](https://gitcode.com/Premium-Resources/a9e1c)

> ⚠️ **注意 ！**
> ---
> 非官方来源，其安全性与完整性无法得到保证，请自行甄别并谨慎使用。

---
### ③ 查看路由器IP
1. 打开拓扑
2. 进入SZ1及SZ2
3. 输入如下指令：
```
sys
int g1/0/0
dis this
```
注意到IP分别为 **SZ1：10.2.26.1 | SZ2：10.2.16.2**  
<p align="center">
  <img src="/images/5-PySNMP/dis_SZ1.png" width="50%">
</p>
<p align="center"><em>dis_SZ2</em></p>
<p align="center">
  <img src="/images/5-PySNMP/dis_SZ2.png" width="50%">
</p>
<p align="center"><em>dis_SZ2</em></p>
这两个IP即为MIB Bowser中需填写的IP  

---
### ④ 启动MIB Bowser并配置用户
#### 初步了解 | 启动后注意到如下界面：
<p align="center">
  <img src="/images/5-PySNMP/MIB_BROWSER_1.png" width="70%">
</p>
<p align="center"><em>MIB_BROWSER主界面_1</em></p>

- ①为**填写IP**的地方  
- ②为**SNMP偏好设置**  
- ③为**输出框**  

#### 配置用户 | 打开SNMP偏好设置
1. 注意到红框内的按钮，单击：  
<p align="center">
  <img src="/images/5-PySNMP/SNMP_1.png" width="50%">
</p>
<p align="center"><em>SNMP偏好设置_1</em></p>

2. 随后注意到如下界面，单击红框内的按钮：  
<p align="center">
  <img src="/images/5-PySNMP/USM_user_1.png" width="50%">
</p>
<p align="center"><em>用户设置_1</em></p>

3. 按照图示内填写：
<p align="center">
  <img src="/images/5-PySNMP/USM_user_2.png" width="50%">
</p>
<p align="center"><em>用户设置_2</em></p>

4. 填写完毕后分别单击箭头指向的按钮，填写密码：
<p align="center">
  <img src="/images/5-PySNMP/USM_user_3.png" width="40%">
</p>
<p align="center"><em>用户设置_3</em></p>

    > ⚠️ **注意 ！**  
    > 上下两个按钮各会弹出一个窗口，都需填写  
    > 密码为：Huawei@123

5. 填写完毕后按如图填写与勾选：
<p align="center">
  <img src="/images/5-PySNMP/SNMP_2.png" width="50%">
</p>
<p align="center"><em>SNMP偏好设置_2</em></p>

6. 随后点击OK：
<p align="center">
  <img src="/images/5-PySNMP/SNMP_3.png" width="50%">
</p>
<p align="center"><em>SNMP偏好设置_3</em></p>

> ### ❕ 为什么需要通过 IP 地址查询 OID ？
> 
> 在基于 SNMP（Simple Network Management Protocol）的网络管理中，管理系统需要从网络设备中获取各种运行状态和配置信息，例如设备名称、接口状态、CPU 使用率、流量统计等。这些信息在设备内部是通过 **OID（Object Identifier）** 进行唯一标识的。
> 
> 然而，OID 只是设备内部管理信息库（MIB）中的数据索引，本身并不能直接访问设备。要获取对应的管理信息，必须先确定 **目标设备的位置**。在 TCP/IP 网络中，设备通常通过 **IP 地址**进行标识和通信，因此网络管理系统需要先通过设备的 **管理 IP 地址**定位到具体设备，然后再通过 SNMP 协议查询对应的 OID。
> 
> 因此，使用 IP 地址查询 OID 的基本流程如下：
> 
> 1. 通过设备的 **管理 IP 地址**定位目标网络设备；
> 2. 使用 **SNMP 协议**与该设备建立通信；
> 3. 根据指定的 **OID** 从设备的 MIB 中读取对应的管理信息；
> 4. 返回设备状态或统计数据供网络管理系统分析和展示。
> 
> 通过这种方式，网络管理员可以在不直接登录设备的情况下，远程获取设备运行状态，实现集中化的网络监控与自动化运维。
> 
> ### ❕ **简单来说**： 
> 
> 每台网络设备或系统的 OID 可能不同，OID 本身只是标识信息的索引，要获取某台设备的具体数据，就必须先知道它的 IP，通过 IP 定位设备，再用对应的 OID 查询。  

---
### ⑤ 编写oid_string.csv
#### 具体步骤如下：
1. 创建*oid_string.csv*到与本项目源代码相同的目录
2. 使用文本编辑器打开，格式如下所示：

    ```
    [OID], [描述], [S/M]
    [OID], [描述], [S/M]
    [OID], [描述], [S/M]
    ```

    > OID查询**在后面讲**  
    > 描述随便写  
    > OID最后若一位为0，最后就是S，否则为M

#### 查询OID
1. 打开MIB Browser
2. 查询下表，在MIB Tree中的查询框输入

    | 描述                        | Name           | 说明          |
    | ------------------------- | -------------- | ----------- |
    | get sysName               | sysName        | 设备系统名称      |
    | get ifNumber              | ifNumber       | 设备接口数量      |
    | get all ifDescr           | ifDescr        | 所有接口描述      |
    | get all ip address        | ipAdEntAddr    | 所有接口的 IP 地址 |
    | get all mask              | ipAdEntNetMask | 对应 IP 的子网掩码 |
    | get all route Destination | ipRouteDest    | 路由表目的地址     |
    | get all next-hop          | ipRouteNextHop | 路由表下一跳地址    |

<p align="center">
  <img src="/images/5-PySNMP/MIB_BROWSER_2.png" width="70%">
</p>
<p align="center"><em>MIB_BROWSER主界面_2</em></p>

3. 右键目标的对象名，点击Properties
<p align="center">
  <img src="/images/5-PySNMP/MIB_BROWSER_3.png" width="70%">
</p>
<p align="center"><em>MIB_BROWSER主界面_3</em></p>

4. 复制OID并回填到*oid_string.csv*中
<p align="center">
  <img src="/images/5-PySNMP/MIB_Node_Properties.png" width="70%">
</p>
<p align="center"><em>MIB_Node_Properties</em></p>

---
### ⑥ 运行代码！
> ❕ 注意  
> 管理设备IP地址即为[③ 查看路由器IP](https://github.com/t1ckprivate/network-autoopration-learn/tree/main/5-PySNMP#-%E6%9F%A5%E7%9C%8B%E8%B7%AF%E7%94%B1%E5%99%A8ip)中得到的两个IP

<p align="center">
  <img src="/images/5-PySNMP/code.png" width="70%">
</p>
<p align="center"><em>VS code</em></p>

---

## 🎉 恭喜！
- 你完成了这章的内容！
