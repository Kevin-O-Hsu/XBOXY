## XBOXY

### 项目简介

XBOXY 是一个自动化工具，用于管理和操作 Xbox 账号，包括登录、获取游戏邀请链接等。该项目旨在提高工作效率，减少手动操作的繁琐步骤。

### 版本信息

- **版本**: `v1.0.3`
- **发布日期**: `2024-12-12`
- **构建号**: `3`

### 更新日志

#### v1.0.3 b1
- 修复了一些已知问题
- 解决了无法下一步的问题
- 使用无头模式，即浏览器窗口不可见
- 可以从文件导入账号密码，且会根据格式自动识别，乱七八糟的格式也可以尝试丢进来
- 优化了部分代码
- 拒绝selenium等老套框架，更加高效先进
- 优化了Build的流程和release的文件管理

#### v1.0.3 b2
- 修复了一些已知问题

#### v1.0.3 b3
- 修复了部分已知问题
- 优化了部分代码

### 项目结构

```
XBOXY/
├── main/
│   ├── user_interaction.py
│   ├── main_handle.py
│   └── xboxy_browser.py
├── resources/
│   ├── singbox.exe
│   ├── ny.json
│   └── fix_ny.json
├── config/
│   └── config.json
└── logs/
    └── log.txt
```

### 安装依赖

确保安装以下依赖：

```bash
pip install playwright rich
playwright install
```

### 配置文件

- `config/config.json`: 配置文件，包含激活码和EULA同意状态。
- `resources/ny.json` 和 `resources/fix_ny.json`: 代理配置文件。
- `resources/singbox.exe`: 代理服务器可执行文件。

### 运行项目

1. **初始化配置**:
   - 运行项目前，确保 `config/config.json` 文件存在并已同意EULA。
   - 输入激活码。

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

1. **运行主程序**:

   ```bash
   python main/user_interaction.py
   ```

2. **查看日志**:
   - 日志文件位于 `logs/log.txt`，记录了程序的运行情况和错误信息。

### 注意事项

- **EULA**: 在首次运行时，需要同意EULA才能继续。
- **激活码**: 输入有效的激活码，否则程序将无法继续。
- **账号格式**: 从文件加载账号时，确保文件格式正确，账号和密码之间用冒号分隔。

### 联系方式

如需帮助或报告问题，请联系项目维护者：

- **邮箱**: support@example.com
- **GitHub**: [项目仓库](https://github.com/yourusername/XBOXY)

### 许可证

本项目采用 MIT 许可证，详情参见 [LICENSE](LICENSE) 文件。

---

希望这个 README 对您有所帮助！如果有任何问题或建议，请随时联系。