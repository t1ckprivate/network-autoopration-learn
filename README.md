<div align="center">

# NetworkAutoopration-learn

### GUFL网络工程系 · 自动化运维的学习仓库  
#### **开拓视野 · 开放思维**
</div>

--- 
## ❗ 关于本仓库
- 如果**尚未具备**一定经验或技术水平，建议将本仓库中的 “**建议**” 理解为 “**必须**” ，将 “**不建议**” 理解为 “**不要**” 。在未完全理解其背后原理之前，不建议自行忽略或随意调整。

## 🛠️ 关于关闭基于虚拟化的安全性
- 找到本仓库中的[**scripts**](https://github.com/t1ckprivate/network-autoopration-learn/tree/main/scripts)文件夹并下载**DG_Readiness_Tool_v3.6.ps1**
- 打开**管理员终端**，cd至脚本所在目录
- 输入如下命令：
```powershell
# 设置执行策略
Set-ExecutionPolicy RemoteSigned

# 执行脚本
.\DG_Readiness_Tool_v3.6.ps1 -Disable
```
- 随即重启系统，重启过程中**持续点按F3**
- 重启后按**Windows徽标键**，输入**msinfo**打开系统信息，注意到**基于虚拟化的安全性**为**未启用**即成功
   
> ⚠️ **注意 ！**  
> 本操作可能在**重启系统**后**失效**  
> 重复操作即可  
> 更多信息，请参阅 [Microsoft | Device Guard and Credential Guard hardware readiness tool](https://www.microsoft.com/en-us/download/details.aspx?id=53337)
---
## 📝 更新日志
#### 2026.3.23
- 在README添加了关于**关闭基于虚拟化的安全性**
- 在README添加了**更新日志**
- 更新了README
- 添加了**项目4-netmiko**