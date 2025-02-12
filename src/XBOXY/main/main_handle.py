import os
import re
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
import concurrent
from .xboxy_browser import XBOXYBrowser
from ..log import logger
from .. import systemutils



console = Console()


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

        config_file = systemutils.JsonFile("config.json", type="dict")
        

        if not config_file.exists():
            self.setup_config(config_file)
        else:
            self.validate_config(config_file)


        self.select_input_method()

        logger.info("所有账号已加载")
        logger.info("正在连接到代理服务器...")
        try:

            systemutils.Runner(path="resources/singbox.exe", args=f"-c \"resources/ny.json\" run").run()
            logger.info("代理服务器已连接")
        except Exception as e:
            logger.warning(f"代理服务器连接失败: {e}")
            raise e


    def setup_config(self, config_file: systemutils.JsonFile):
        """
        This function sets up a configuration file by writing data indicating acceptance of an End User
        License Agreement (EULA) after user confirmation.
        
        :param config_file: The `config_file` parameter is of type `systemutils.JsonFile`, which is likely a
        class or object representing a JSON file that can be read from or written to. In the provided code
        snippet, the `setup_config` method takes a `config_file` parameter of type `systemutils.Json
        :type config_file: systemutils.JsonFile
        """
        assert input("是否同意EULA[Y/N]>>> ").lower() == 'y'
        config_file.write_json_data({"accept_eula": True})

    def validate_config(self, config_file: systemutils.JsonFile) -> bool:
        """
        The function `validate_config` checks if the user has accepted the End User License Agreement (EULA)
        in a JSON configuration file and updates the file accordingly.
        
        :param config_file: The `config_file` parameter is of type `systemutils.JsonFile`, which is likely a
        class or object representing a JSON file. The `validate_config` method reads data from this JSON
        file, checks if a specific key `"accept_eula"` is present and has a truthy value. If
        :type config_file: systemutils.JsonFile
        :return: The `validate_config` method returns a boolean value. It returns `True` if the
        "accept_eula" key in the JSON data obtained from the `config_file` is `True` or if the user inputs
        'Y' when prompted to agree to the EULA. Otherwise, it returns `False`.
        """
        data = config_file.get_json_data()
        if not data.get("accept_eula"):
            if input("同意EULA[Y/N]>>> ").lower() != 'y':
                return False
            else:
                config_file["accept_eula"] = True
        return True
    
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

        match Prompt.ask("请选择 (1/2)"):
            case "1":
                self.load_accounts_from_file()
            case "2":
                self.input_single_account()
            case _:
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
    
    def process_account(self, email: str, password: str) -> tuple[list, bool]:
        """单个账号的处理逻辑"""
        try:
            return list(XBOXYBrowser(email=email, password=password).result_data), True
        except Exception as e:
            return [f"Error for {email}: {e}"], False
        


    def run(self):
        """
        The `run` function iterates through a list of accounts, logs in using the provided email and
        password, and appends the resulting links to a list.
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            # 使用 map 来并发处理每个账号
            future_to_account = {executor.submit(self.process_account, email, password): (email, password)
                                 for email, password in self.accounts}
            
            results = []
            for future in concurrent.futures.as_completed(future_to_account):
                result = future.result()
                
                if result[1]:
                    results.extend(result[0])
                else:
                    logger.error(result)
                

        # logger.info(results)
        # 将结果展平并添加到 self.result 中
        self.result.extend([item for sublist in results for item in sublist])
                
        