> 😅 **提示**  
> ---
> 本节中的部分内容参考了覃老师提供的指导材料  
> 但原有指导内容过于简要，对关键原理与实际操作的说明不够完整  
> 因此本节在实践过程中对相关步骤与原理进行了补充、整理与扩展，以便更系统地理解相关技术  
> **具体如本README中的操作步骤所示**
>
> 若你的设备依旧有连接不到eNSP的问题  
> 请参阅：[GITHUB | t1ckprivate/network-autoopration-learn/tree/main/2-Telnetlib](https://github.com/t1ckprivate/network-autoopration-learn/tree/main/2-Telnetlib)

> ❗警告
> ---  
> 本节为便于演示，插入了部分示例图  
> **不建议**直接用于个人实验报告中  
> 若自行引用或使用，由使用者自行承担相关责任  

## 如何使用？
- 详细阅读**操作步骤**中所给出的指导
- 在IDE中使得终端位于./5-PySNMP中，运行code.py

## 操作步骤
### ① 下载 / 配置拓扑
#### 若使用本仓库提供的拓扑：
- 下载本仓库，并使用IDE打开./5-PySNMP文件夹
- 打开topo中的pro3.topo，**无需做任何设置，本仓库下的所有拓扑均已配置完成**
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

### ③ 查看路由器IP
- 打开拓扑
- 进入SZ1及SZ2
- 输入如下指令：
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

### ④ 启动MIB Bowser并配置用户
#### 初步了解 | 启动后注意到如下界面：
<p align="center">
  <img src="/images/5-PySNMP/MIB_BROWSER_1.png" width="70%">
</p>
<p align="center"><em>MIB_BROWSER主界面</em></p>

- ①为**填写IP**的地方  
- ②为**SNMP偏好设置**  
- ③为**输出框**  

#### 配置用户 | 打开SNMP偏好设置
- 注意到红框内的按钮，单击：  
<p align="center">
  <img src="/images/5-PySNMP/SNMP_1.png" width="70%">
</p>
<p align="center"><em>SNMP偏好设置_1</em></p>

- 随后注意到如下界面，单击红框内的按钮：  
<p align="center">
  <img src="/images/5-PySNMP/USM_user_1.png" width="70%">
</p>
<p align="center"><em>用户设置_1</em></p>

- 按照图示内填写：
<p align="center">
  <img src="/images/5-PySNMP/USM_user_2.png" width="70%">
</p>
<p align="center"><em>用户设置_2</em></p>

- 填写完毕后分别单击箭头指向的按钮，填写密码：
<p align="center">
  <img src="/images/5-PySNMP/USM_user_3.png" width="70%">
</p>
<p align="center"><em>用户设置_3</em></p>

> ⚠️ **注意 ！**  
> 上下两个按钮各会弹出一个窗口，都需填写  
> 密码为：Huawei@123

- 填写完毕后按如图填写与勾选：
<p align="center">
  <img src="/images/5-PySNMP/SNMP_2.png" width="70%">
</p>
<p align="center"><em>SNMP偏好设置_2</em></p>

- 随后点击OK：
<p align="center">
  <img src="/images/5-PySNMP/SNMP_3.png" width="70%">
</p>
<p align="center"><em>SNMP偏好设置_3</em></p>

