> 😅 **提示**  
> ---
> 本节中内容覃老师并未提供任何指导材料  
> 因此本节在实践过程中对步骤进行了详细描述，以便更系统地理解相关技术  
> **具体如本README中的操作步骤所示**
>
> 若**需要更多教程** 或 **发现本仓库有错误** 或 **需要帮助**  
> 请在本仓库[提交issue](https://github.com/t1ckprivate/network-autoopration-learn/issues) 或 私聊我 或 电邮联系[i@t1ck.me](mailto:i@t1ck.me)  

## 如何使用？
1. 详细阅读**操作步骤**中所给出的指导
2. 在IDE中使得终端位于./8-Restconf中，运行code.py

## 操作步骤
### 零 安装并配置环境
> ❕ **注意**  
> ---
> 由于老师指出的方法过于抽象且无趣  
> 此处教程使用 `EVE-ng仿真器` 进行  
> 同时为照顾普通同学，教程 `**依然提供覃老师方式**`  
> 关于使用覃老师方式完成本次作业，请[**点我！**](#覃老师方式)

#### 安装EVE-ng
1. 访问 [CNB | eve-ng/repo](https://cnb.cool/eve-ng/repo/-/releases)  
2. 下载 `EVE-NG社区懒人版5.1-Large.ova`
    <p align="center">
      <img src="/images/8-Restconf/1.png" width="50%">
    </p>
    <p align="center"><em>CNB | eve-ng/repo</em></p>

3. 导入VMware  
    直接在VMware左侧的库中`右键`，选择打开  
    <p align="center">
      <img src="/images/8-Restconf/2.png" width="50%">
    </p>
    <p align="center"><em>VMware</em></p>

    <p align="center">
      <img src="/images/8-Restconf/3.png" width="50%">
    </p>
    <p align="center"><em>VMware</em></p>  

    导入时间会`比较长`，这是正常的

4. 配置网卡  
    在VMware`左上角`的`编辑`，打开`虚拟网络适配器`  
    添加`两张`网卡，选`仅主机模式`  
    这两张网卡配置个自己喜欢的网段  
    <p align="center">
      <img src="/images/8-Restconf/4.png" width="50%">
    </p>
    <p align="center"><em>VMware</em></p> 

    > 为什么是两张？
    > ---
    > 因为EVE-ng与eNSP连接到宿主机网络的方式不是很相同  
    > 且该仿真器是基于发行版的Linux，并无像软件一样的前台，只有web作为前台  
    > 这两张网卡分别用来：  
    > - 第一张：提供用户访问介面，既web前台
    > - 第二张：提供与宿主机网络互通的通道，既类似于eNSP中Cloud的功能

5. 配置虚拟机  
    **最重要的是记得添加两张网卡！**  
    <p align="center">
      <img src="/images/8-Restconf/5.png" width="50%">
    </p>
    <p align="center"><em>VMware</em></p> 

    然后这玩意其实不是很吃配置，所以其它的你们看你们电脑的性能来

6. 开启虚拟机  
    然后你们会看到这个界面：
    <p align="center">
      <img src="/images/8-Restconf/6.png" width="50%">
    </p>
    <p align="center"><em>VMware</em></p> 

    给了个ip，所以很显然，把它丢到浏览器里，就成了
    <p align="center">
      <img src="/images/8-Restconf/7.png" width="50%">
    </p>
    <p align="center"><em>EVE-ng login</em></p> 

    > - web里面默认账号是 `admin` ，密码是 `eve`  
    > - EVE那个Linux的默认账号是 `root` ，密码是 `eve` ，这个你们大概用不到，不用管  
    > - 如果没有显示IP，一直在一个logo上，就是`网卡没添加成功`，重新看一下网卡什么情况，必要时候重新配置一下

7. 使用  
    就正常登录就好  
    然后有个选项框：
    <p align="center">
      <img src="/images/8-Restconf/8.png" width="50%">
    </p>
    <p align="center"><em>EVE-ng login</em></p> 

    你们选`HTML5 console`就好，这个是网页的终端  
    Native是呼出CRT软件，刚上手就用网页的就行  

    > 关于使用EVE-ng  
    > 请参阅 [BILIBILI | 万能模拟器EVE-NG使用教程](https://www.bilibili.com/video/BV1NBtEz7Eey/)

#### 基本操作
1. 新建拓扑
    红框的就是
    <p align="center">
      <img src="/images/8-Restconf/9.png" width="50%">
    </p>
    <p align="center"><em>EVE-ng</em></p> 
2. 往拓扑中添加设备
    右键拓扑空白的地方会出来个`Add a new object`
    <p align="center">
      <img src="/images/8-Restconf/10.png" width="50%">
    </p>
    <p align="center"><em>EVE-ng</em></p> 

    `Node`是节点，也就是`设备`
    `Network`是`桥、云之类的`
3. 配置设备
    添加完设备点一下就进终端了，就点一下它，蒽
    <p align="center">
      <img src="/images/8-Restconf/11.png" width="50%">
    </p>
    <p align="center"><em>EVE-ng</em></p> 

> 不知道哪些设备是啥怎么办？ 
> --- 
> 上网查咯（

### ① 绘制&配置拓扑
1. 绘制如图的拓扑
    <p align="center">
      <img src="/images/8-Restconf/12.png" width="50%">
    </p>
    <p align="center"><em>EVE-ng</em></p> 
    
    其中的 `CSR` 是 `Cisco CSR 1000V (XE 16.x)`  
    其中的 `Switch` 是 `Cisco vlOS Router`  
    `Net（那朵云）` 的 `Type` 选用 `Cloud1`
    <p align="center">
      <img src="/images/8-Restconf/13.png" width="50%">
    </p>
    <p align="center"><em>EVE-ng</em></p>

2. 配置路由器（交换机不用配置）   
    *Tips: 开启设备时间有点长，是正常的*  
    分别配置四台路由器，如下:
    ```
    enable
    conf t
    hostname CSR1        # 这里记得换数字

    ip domain name cisco.com
    crypto key generate rsa
    768
    username cisco privilege 15 password 0 cisco
    line vty 0 4
    login local
    transport preferred ssh
    exit
    ip ssh version 2

    restconf
    ip http authentication local
    ip http secure-server

    int g1
    ip add 192.168.201.101 255.255.255.0        # 这里IP改成另一张网卡的，每台路由器都改不一样的
    no shutdown
    exit

    ```
    > **❕ 关于上面的ip**
    > ---
    > 那会不是让加了两张网卡吗，然后还显示了个ip  
    > 看网段，`除了给出的那个ip`，`另一个网段`才是这里需要写进去的网段

### ② 修改代码
修改本仓库提供的`./8-Restconf/code.py `   
其中的`第251至254行`
将其中的IP`修改为`刚才`给路由器配置的那四个IP`，从`上至下`分别是`1-4`  
  <p align="center">
    <img src="/images/8-Restconf/14.png" width="50%">
  </p>
  <p align="center"><em>VS code</em></p>

### ③ 运行代码！
- 出现以下结果即实验成功
<p align="center">
  <img src="/images/8-Restconf/15.png" width="50%">
</p>
<p align="center"><em>VS code</em></p>

---

### 覃老师方式
> 所以，老师给出的是个啥？
> ---
> 其实就是去掉了模拟器  
> 事实上这章任务本身就是个星型拓扑，中间是一台交换机，周围是思科的路由器  
> 其实华为的也能用，我也搞不明白为什么要用思科的，可能就是~~恶心一下我们~~（
>
> 所以，我们就可以直接在VMware里面跑CSR1000来做到同等效果
> 怎么做看下面吧

#### 1. 把CSR1000的镜像导入到VMware里面  
  - 很简单吧，就单纯导入就好了，像安装其他的系统一样  
  - 然后克隆下，一共`整四台`    

#### 2. 配置网卡
  - 这里直接加一张网卡吧，随便什么都好，比如VMnet10  
  - 加这一张网卡是为了`让这四个路由器`还有`宿主机或虚拟机`互连起来  

  - 然后你`如果用CentOS里的pycharm`写代码，就把这张网卡也加进那个虚拟机里面  
  - 如果是用宿主机写代码，就不需要任何操作了

#### 3. 开机配置
  - 给所有的路由器都配置，像下面这样：
    ```
      enable
      conf t
      hostname CSR1        # 这里记得换数字

      ip domain name cisco.com
      crypto key generate rsa
      768
      username cisco privilege 15 password 0 cisco
      line vty 0 4
      login local
      transport preferred ssh
      exit
      ip ssh version 2

      restconf
      ip http authentication local
      ip http secure-server

      int g1
      ip add 192.168.201.101 255.255.255.0        # 这里IP改成另一张网卡的，每台路由器都改不一样的
      no shutdown
      exit
    ```
#### 4. 改代码
  - 修改本仓库提供的`./8-Restconf/code.py `   
  - 其中的`第251至254行`
  - 将其中的IP`修改为`刚才`给路由器配置的那四个IP`，从`上至下`分别是`1-4` 

#### 5. 跑代码
  - 没了
  - 其实还是很简单的。。



---
## 🎉 恭喜！
- 你完成了这章的内容！





