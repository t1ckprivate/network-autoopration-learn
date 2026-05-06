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
2. 使得终端位于./9-Ansible中，运行如下指令：
    ```
    ansible-playbook -i hosts get_info.yaml
    ansible-playbook -i hosts conf_vlan.yaml
    ```

---

### ① 下载 / 配置拓扑
#### 若使用本仓库提供的拓扑：
1. 下载本仓库，并使用IDE打开./9-Ansible文件夹
2. 打开/topo中的pro3.topo，**无需做任何设置，本仓库下的所有拓扑均已配置完成**
#### 若自行配置拓扑：
1. 新建一朵Cloud，添加UDP以及VMnet网卡，并使其相互映射
2. 将`S4`的`G0/0/7`连接至`Cloud`，并将其`加入vlan3`中：
    ```
        interface GigabitEthernet0/0/7
        port link-type access
        port default vlan 3 
    ```

3. 配置SZ1：
    ```
    sys
    aaa
    local-user python password cipher Huawei12#$
    local-user python service-type ssh
    quit
    stelnet server enable
    ssh user python authentication-type password
    undo ssh server compatible-ssh1x enable
    user-interface vty 0 4
    authentication-mode aaa
    user privilege level 15
    protocol inbound ssh
    quit
    rsa local-key-pair create

    # y
    # 2048
    ```
4. 配置S1、S2：
    ```
    sys
    aaa
    local-user python password cipher Huawei12#$
    local-user python service-type ssh
    quit
    stelnet server enable

    ssh user python
    ssh user python authentication-type password
    ssh user python service-type stelnet
    undo ssh server compatible-ssh1x enable
    user-interface vty 0 4
    authentication-mode aaa
    user privilege level 15
    protocol inbound ssh
    quit
    rsa local-key-pair create

    # 2048
    ```

### ② 下载本仓库提供的文件 / 下载整个仓库
- conf_vlan.yaml
- get_info.yaml
- hosts

### ② 运行！
- 使得终端位于./9-Ansible中，运行如下指令：
```
ansible-playbook -i hosts get_info.yaml
ansible-playbook -i hosts conf_vlan.yaml
```
- 出现以下结果即实验成功
<p align="center">
  <img src="/images/9-Ansible/1.png" width="50%">
</p>
<p align="center"><em>VS code</em></p>

<p align="center">
  <img src="/images/9-Ansible/2.png" width="50%">
</p>
<p align="center"><em>VS code</em></p>