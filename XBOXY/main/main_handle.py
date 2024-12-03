from log import logger
import verify
import systemutils
import pathlib
import sys
import os
import re
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from main.xboxy_browser import XBOXYBrowser


console = Console()

class XBOXY:
    """
    主程序类，负责多账号管理、代理启动等功能。
    """
    def __init__(self) -> None:
        self.accounts = []
        self.result = []
    
    def initialize(self):
        """
        初始化程序，完成身份验证和代理连接。
        """
        logger.info("开始身份验证...")
        config_file = systemutils.JsonFile(pathlib.Path("config/config.json"))
        
        # 这里只是验证文件的格式是否正确，并确保同意了eula
        if not config_file.is_exist:  # 修正用法为属性访问
            self.setup_config(config_file)
        else:
            self.validate_config(config_file)

        # 这里开始验证激活码
        pass_key = config_file.get_json_data().get("license_key")
        self.verify_license(pass_key, config_file)
        logger.info("激活码验证成功")

        # 这个方法就是通过各种方式向self.account里面增加键值对
        self.select_input_method()

        logger.info("所有账号已加载")
        logger.info("正在连接到代理服务器...")
        try:
            og_config = systemutils.JsonFile(pathlib.Path("resources/ny.json")).get_json_data()
            
            proxy_config_path = systemutils.JsonFile(pathlib.Path("resources/fix_ny.json")).create_file()
            for rule in og_config["route"]["rule_set"]:
                rule["path"] = str(systemutils.File(pathlib.Path(rule["path"])).path)
            
            proxy_config_path.write_json_data(og_config)
            
            systemutils.Runner(
                f"{systemutils.File(pathlib.Path("resources/singbox.exe")).path} -c {proxy_config_path.path} run"
            ).run()
            logger.info("代理服务器已连接")
        except Exception as e:
            logger.warning(f"代理服务器连接失败: {e}")
            sys.exit()


    def setup_config(self, config_file: systemutils.JsonFile):
        """
        创建配置文件并进行初始化设置。
        """
        config_file.create_file()
        config_file.write_json_data({})
        logger.info("配置文件已创建")
        if input("是否同意EULA[Y/N]>>> ").lower() != 'y':
            logger.warning("未同意EULA, 程序退出")
            sys.exit()
        logger.info("请输入你的软件激活码: ")
        pass_key = input("激活码>>> ")
        config_file.write_json_data({"license_key": pass_key, "accept_eula": True})

    def validate_config(self, config_file: systemutils.JsonFile):
        """
        验证现有配置文件。
        """
        data = config_file.get_json_data()
        if not data.get("accept_eula"):
            if input("同意EULA[Y/N]>>> ").lower() != 'y':
                logger.warning("未同意EULA, 程序退出")
                sys.exit()
            config_file.update_json_data({"accept_eula": True})
        if not data.get("license_key"):
            logger.info("请输入你的软件激活码: ")
            pass_key = input("激活码>>> ")
            config_file.update_json_data({"license_key": pass_key})

    def verify_license(self, pass_key, config_file: systemutils.JsonFile):
        """
        验证激活码。
        """
        while not verify.OnlineVerification(verify.Collection().hwid, pass_key).send_requests():
            logger.info("激活码无效，请重新输入:")
            pass_key = input("激活码>>> ")
        
        # 有效了之后要记得更新文件
        config_file.update_json_data(("license_key", pass_key))
        
    
    def select_input_method(self):
        """
        选择账号输入方式。
        """
        console.print("请选择账号输入方式:", style="bold cyan")
        table = Table(title="输入方式")
        table.add_column("编号", justify="center")
        table.add_column("方式", justify="left")
        table.add_row("1", "从文件加载 (文件格式: 账号密码中间有冒号就可以, 其余会根据文件全自动判断, 随便往里面丢就行)")
        table.add_row("2", "手动输入单个账号")
        console.print(table)

        choice = Prompt.ask("请选择 (1/2)")
        if choice == "1":
            self.load_accounts_from_file()
        elif choice == "2":
            self.input_single_account()
        else:
            logger.warning("无效选择，程序退出")
            sys.exit()

    def load_accounts_from_file(self):
        """
        从文件加载账号。
        """
        file_path = Prompt.ask("请输入文件路径")
        if not os.path.exists(file_path):
            logger.warning("文件不存在，程序退出")
            sys.exit()
        logger.info("正在加载文件...")
        with open(file_path, 'r') as f:
            for line in f:
                match_enp = re.findall(r"([\w\.\-]+@[a-zA-Z_]+(?:\.[a-zA-Z]{2,})+):([^\s,]+)", line.strip())
                if (not line) or (not match_enp):
                    continue
                logger.info(match_enp)
                email, password = match_enp[0]
                self.accounts.append((email.strip(), password.strip()))

    def input_single_account(self):
        """
        手动输入单个账号。
        """
        email = input("请输入你的 Xbox 账号: ").strip()
        password = input("请输入该账号的密码: ").strip()
        self.accounts.append((email, password))

    def run(self):
        """
        遍历所有账号，执行登录流程。
        """
        for email, password in self.accounts:
            for link in XBOXYBrowser(email=email, password=password).result_data:
                self.result.append(link)

    def cleanup(self):
        """
        程序退出时关闭代理。
        """
        logger.info("关闭代理服务器...")
        systemutils.Runner(f"{systemutils.File(pathlib.Path("resources/singbox.exe")).path}").terminate()
        logger.info("代理服务器已关闭")