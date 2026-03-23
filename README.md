<div align="center">

# NetworkAutoopration-learn

### GUFL网络工程系 · 自动化运维的学习仓库  
#### **开拓视野 · 开放思维**
</div>

--- 
## 🛠️ 关于关闭基于虚拟化的安全性
- 找到本仓库中的[**scripts**](https://github.com/t1ckprivate/network-autoopration-learn/tree/main/1-PythonBasic)文件夹并下载**DG_Readiness_Tool_v3.6.ps1**
- 打开**管理员终端**，cd至脚本所在目录
- 输入如下命令：
```powershell
# 设置执行策略（仅当前进程，避免污染系统）
Set-ExecutionPolicy RemoteSigned

# 执行脚本
.\DG_Readiness_Tool_v3.6.ps1 -Disable
```
- 随即重启系统，重启过程中**持续点按F3**
- 重启后按**Windows徽标键**，输入**msinfo**打开系统信息，注意到**基于虚拟化的安全性**为**未启用**即成功
   
> ⚠️ **注意 ！**  
> 本操作可能在**重启系统**后**失效**  
> 重复操作即可
---
## 📝 更新日志
#### 2026.3.23
- 在README添加了关于**关闭基于虚拟化的安全性**
- 在README添加了**更新日志**
- 更新了README
- 添加了**项目4-netmiko**