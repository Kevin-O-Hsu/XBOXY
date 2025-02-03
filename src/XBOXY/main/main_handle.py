# The `XBOXY` class is a program class responsible for managing multiple accounts, initializing
# authentication and proxy connection, and providing methods for loading accounts from files or manual
# input.
from asyncio import as_completed
import pathlib
import os
import re
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from concurrent.futures import ThreadPoolExecutor

from .xboxy_browser import XBOXYBrowser
from .. import log
from .. import systemutils
from .. import verify

logger = log.logger
console = Console()

# The `XBOXY` class manages multiple accounts, handles initialization, configuration setup, account
# loading, and proxy connection in a Python program.
class XBOXY:
    """
    主程序类，负责多账号管理、代理启动等功能。
    """
    def __init__(self) -> None:
        """
        The function initializes two empty lists, `accounts` and `result`.
        """
        self.accounts = []
        self.result = []
    
    def initialize(self):
        """
        The `initialize` function in Python initializes the program by performing identity verification,
        connecting to a proxy, validating a license key, and loading accounts.
        """
        logger.info("开始身份验证...")
        config_file = systemutils.JsonFile(pathlib.Path("config.json"), needed=True)
        
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
            raise Exception


    def setup_config(self, config_file: systemutils.JsonFile):
        """
        This Python function sets up a configuration file, prompts the user to agree to an End User License
        Agreement (EULA), and collects a software activation key.
        
        :param config_file: The `config_file` parameter is an instance of the `JsonFile` class from the
        `systemutils` module. It is used to handle operations related to a JSON configuration file, such as
        creating the file, writing JSON data to it, and reading JSON data from it
        :type config_file: systemutils.JsonFile
        """
        config_file.create_file()
        config_file.write_json_data({})
        logger.info("配置文件已创建")
        if input("是否同意EULA[Y/N]>>> ").lower() != 'y':
            logger.warning("未同意EULA, 程序退出")
            raise Exception
        logger.info("请输入你的软件激活码: ")
        pass_key = input("激活码>>> ")
        config_file.write_json_data({"license_key": pass_key, "accept_eula": True})

    def validate_config(self, config_file: systemutils.JsonFile):
        """
        This Python function validates an existing configuration file by checking and updating certain
        key-value pairs.
        
        :param config_file: The `config_file` parameter in the `validate_config` method is of type
        `systemutils.JsonFile`. This parameter is used to read and update a JSON configuration file that
        contains settings for the program. The method reads the JSON data from the `config_file`, checks if
        certain keys exist in the
        :type config_file: systemutils.JsonFile
        """
        data = config_file.get_json_data()
        if not data.get("accept_eula"):
            if input("同意EULA[Y/N]>>> ").lower() != 'y':
                logger.warning("未同意EULA, 程序退出")
                raise Exception
            config_file.update_json_data({"accept_eula": True})
        if not data.get("license_key"):
            logger.info("请输入你的软件激活码: ")
            pass_key = input("激活码>>> ")
            config_file.update_json_data({"license_key": pass_key})

    def verify_license(self, pass_key, config_file: systemutils.JsonFile):
        """
        This Python function verifies a license key by sending online verification requests and updates a
        JSON configuration file with the valid key.
        
        :param pass_key: The `pass_key` parameter is the activation code that is used to verify the license.
        It is provided by the user and is used in the online verification process to check the validity of
        the license
        :param config_file: The `config_file` parameter is of type `systemutils.JsonFile`, which is likely a
        class or object that handles reading and writing JSON data to a file. In this context, it seems to
        be used for storing and updating license key information. The `update_json_data` method is likely a
        :type config_file: systemutils.JsonFile
        """
        while not verify.OnlineVerification(verify.Collection().hwid, pass_key).send_requests():
            logger.info("激活码无效，请重新输入:")
            pass_key = input("激活码>>> ")
        
        # 有效了之后要记得更新文件
        config_file.update_json_data(("license_key", pass_key))
        
    
    def select_input_method(self):
        """
        The `select_input_method` function allows the user to choose between loading accounts from a file or
        manually inputting a single account.
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
            raise Exception

    def load_accounts_from_file(self):
        """
        This Python function loads accounts from a file by parsing email and password pairs from each line.
        """
        file_path = Prompt.ask("请输入文件路径")
        if not os.path.exists(file_path):
            logger.warning("文件不存在，程序退出")
            raise Exception 
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
        This function allows the user to manually input a single Xbox account with email and password.
        """
        email = input("请输入你的 Xbox 账号: ").strip()
        password = input("请输入该账号的密码: ").strip()
        self.accounts.append((email, password))
    
    def process_account(self, email: str, password: str) -> list:
        """单个账号的处理逻辑"""
        try:
            return list(XBOXYBrowser(email=email, password=password).result_data)
        except Exception as e:
            return [f"Error for {email}: {e}"]

    def run(self):
        """
        The `run` function iterates through a list of accounts, logs in using the provided email and
        password, and appends the resulting links to a list.
        """
        with ThreadPoolExecutor(max_workers=12) as executor:
            
            future_to_account = {
                executor.submit(self.process_account, email, password): (email, password)
                for email, password in self.accounts
            }
            
            for future in as_completed(future_to_account):
                # 获取任务的返回结果
                links = future.result()
                self.result.extend(links)  # 将结果添加到总列表
                


    def cleanup(self):
        """
        The `cleanup` function closes the proxy server when the program exits.
        """
        logger.info("关闭代理服务器...")
        systemutils.Runner(path=f"{systemutils.File(pathlib.Path("resources/singbox.exe")).path}").terminate()
        logger.info("代理服务器已关闭")
        