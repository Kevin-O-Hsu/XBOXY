## XBOXY

### 项目简介

XBOXY 是一个自动化工具，用于管理和操作 Xbox 账号，包括登录、获取游戏邀请链接等。该项目旨在提高工作效率，减少手动操作的繁琐步骤。


### 项目结构

```
XBOXY/
├── main/
│   ├── user_interaction.py
│   ├── main_handle.py
│   └── xboxy_browser.py
├── resources/
│   ├── singbox.exe
│   └── ny.json
└── config/
    └── config.json

```

### 安装依赖

确保安装以下依赖：

CPython >= 3.11 

```bash
pip install -r requirements.txt
```

### 配置文件

- `config/config.json`: 配置文件。
- `resources/ny.json` : 代理配置文件。
- `resources/singbox.exe`: 代理服务器可执行文件。

### 运行项目

1. **初始化配置**:
   - 运行项目前，确保 `config/config.json` 文件存在。

2. **选择账号输入方式**:
   - 从文件加载账号（文件格式：账号密码中间有冒号即可）。
   - 手动输入单个账号。

3. **启动代理服务器**:
   - 项目会自动连接到代理服务器。

4. **执行登录流程**:
   - 遍历所有账号，模拟登录Xbox并获取可用链接。
   - 将结果保存到 `output.json` 文件中。

5. **关闭代理服务器**:
   - 程序退出时，自动关闭代理服务器。

### 使用说明

  **运行主程序**

   ```bash
   python xboxy.py
   ```


### 注意事项

- **账号格式**: 从文件加载账号时，确保文件格式正确，账号和密码之间用冒号分隔。

### 联系方式

如需帮助或报告问题，请联系项目维护者：

- **邮箱**: vmcgresh@proton.me
- **GitHub**: [项目仓库](https://github.com/Kevin-O-Hsu/XBOXY)

