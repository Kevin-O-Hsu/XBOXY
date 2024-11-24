from log import logger
import verify
import systemutils
import pathlib
import browser
import re
import pyperclip
import sys
import os

# 防止出错信息被用户看到
sys.excepthook = lambda _, __, ___: None

version = 'v1.0.3'
release_date = '2024-11-16'
build = '1'



class XBOXYBrowser(browser.ChromiumBrowser):
    
    def __init__(self, email: str, password: str) -> None:
        logger.info('启动Playwright...')
        self.email = email
        self.password = password
        super().__init__()
    
    def run(self):
        
        p = self.context.new_page()
        logger.info("前往Xbox 登录页面...")
        p.goto(r'https://www.xbox.com/en-us/auth/msa?action=logIn&returnUrl=https%3A%2F%2Fwww.xbox.com%2Fzh-HK%2Fxbox-game-pass%2Finvite-your-friends&ru=https%3A%2F%2Fwww.xbox.com%2Fzh-HK%2Fxbox-game-pass%2Finvite-your-friends', wait_until="load", timeout=0)
        logger.info("等待网页完全加载，可能比较久")
        p.wait_for_load_state("networkidle", timeout=0)
        p.wait_for_selector('input[id="i0116"]')
        
        
        logger.info("輸入帳號和密碼 尝试登录...")
        p.locator('input[id="i0116"]').fill(self.email)
        p.wait_for_load_state("networkidle", timeout=0)
        p.locator('button[type="submit"]').click()
        

        p.wait_for_load_state("networkidle", timeout=0)
        
        # 等待完全加载之后看有没有错误
        if self.element_exists(p, 'div[id="i0116Error"]'):
            logger.warning("账号不存在")
            return []
        
        # 默认没有走密码登录, 切换到密码登录
        elif self.element_exists(p, 'input[id="idTxtBx_OTC_Password"]'):
            p.wait_for_load_state("networkidle", timeout=0)
            p.locator('span[role="button"][id="idA_PWD_SwitchToCredPicker"]').click()
            p.locator('#tileList > div:nth-child(2) > div > button').click()
            

        
        p.locator('input[id="i0118"]').fill(self.password)
        p.wait_for_load_state("networkidle", timeout=0)
        p.locator('button[type="submit"]').click()
        
        
        # 等待完全加载之后看有没有错误
        p.wait_for_load_state("networkidle", timeout=0)
        
        # 密码错误
        if self.element_exists(p, 'div[id="i0118Error"]'):
            logger.warning("密码错误")
            return []
        
        # 无法登录
        elif self.element_exists(p, '#i1011'):
            logger.warning("无法登录")
            return []
        
        # 提示更新密码, 无法登录
        elif self.element_exists(p, 'div[class="UpdatePasswordPageContainer PageContainer"]'):
            logger.warning("需要更新密码, 无法登录")
            return []
        
        # 提示安全邮箱更改, 可以登录
        elif self.element_exists(p, 'input[type="button"][id="iLandingViewAction"]'):
            p.locator('input[type="button"][id="iLandingViewAction"]').click()
            
        # 需要验证邮箱, 无法登录
        elif self.element_exists(p, 'div[role="heading"][id="serviceAbuseLandingTitle"]'):
            logger.warning("需要验证邮箱, 无法登录")
            return []
        
        
        p.wait_for_load_state("networkidle", timeout=0)
        
        p.locator('button[id="acceptButton"]').click()
        p.locator('img[alt="Xbox"]')
        
        
        
        p.wait_for_load_state("networkidle", timeout=0)
        p.wait_for_selector('#BuddyPassSender > div > div > p')
        display_sentence = p.locator('#BuddyPassSender > div > div > p').text_content()
        logger.info(f"网页显示 {display_sentence}")
        
        last_quota = re.findall(r'\d+', display_sentence)[0]
        
        
        
        match int(last_quota):
            case 0:
                logger.warning("没有可用配额")
                return []
            case 7:
                logger.warning("无法使用")
                return []
        
        
        logger.info(f"当前剩余 {last_quota} / 5 配额")
        
        links = []
        for _ in range(0, int(last_quota)):
            logger.info(f"正在获取第 {_+1} 個連結...")
            p.locator('#BuddyPassSender > div > div > div.c-table > div > button').click()
            p.wait_for_load_state("networkidle", timeout=0)
            links.append(p.locator('body > reach-portal > div:nth-child(3) > div > div > div > div > div.p-5.Modal-module__modalBody___\+Kkbo > div > div > div > a').get_attribute('href'))
            p.locator('body > reach-portal > div:nth-child(3) > div > div > div > div > div.Modal-module__closeContainer___kCjh7 > button').click()
            
            
            
        logger.info(f"已获取 {len(links)} 个链接")
        
        pyperclip.copy(links)
        return links
        
        



class XBOXY:
    
    def __init__(self, email, password) -> None:
        logger.info(f"验证通过")
        logger.info("正在连接到代理服务器 ...")
        logger.info("开启30289, 30290端口...")
        logger.warning(os.getcwd())
        logger.warning(f"{os.path.join(os.getcwd(), 'resources/singbox.exe')} -c {os.path.join(os.getcwd(),'resources/ny.json run')}")
        systemutils.Runner(f"{os.path.join(os.getcwd(), 'resources/singbox.exe')} -c {os.path.join(os.getcwd(),'resources/ny.json run')}").run()
        logger.info("已连接到代理服务器")
        logger.info(self.run(email, password))
        
        
        
    @classmethod
    def begin(cls):
        
        config_file = systemutils.JsonFile(pathlib.Path("config/config.json"))
        
        if not config_file.is_exist:
            config_file.create_file()
            config_file.write_json_data({})
            logger.info("配置文件不存在，已创建配置文件")
            match input("是否同意EULA[Y/N]>>> ").lower():
                case 'y':
                    config_file.append_json_data(("accept_eula", True))
                case _:
                    logger.warning("你已拒绝EULA, 程序已退出")
                    sys.exit()
            logger.info("请输入你的软件激活码 : ")
            pass_key = input("激活码>>> ")
            config_file.append_json_data(("license_key", pass_key))    
        else:
            config_file_content = config_file.get_json_data() 
            license_key_str = config_file_content.get("license_key")
            
            accept_eula = config_file_content.get("accept_eula")
            if (accept_eula is None) or (accept_eula == False):
                logger.warning("配置文件存在, 但未同意EULA, 请同意EULA (eula.txt): ")
                match input("同意EULA[Y/N]>>> ").lower():
                    case 'y':
                        config_file.append_json_data(("accept_eula", True))
                    case _:
                        logger.warning("你已拒绝EULA, 程序已退出")
                        sys.exit()
                    
            if license_key_str is not None:
                pass_key = license_key_str
            else:
                logger.info("配置文件存在，但激活码为空，请输入你的软件激活码 : ")
                pass_key = input("激活码>>> ")
                config_file.append_json_data(("license_key", pass_key))
        
        pass_code = verify.OnlineVerification(verify.Collection().hwid, pass_key).send_requests()
        
        while not pass_code:
            logger.info("激活码无效，请重新输入你的软件激活码 : ")
            pass_key = input("激活码>>> ") 
            config_file.append_json_data(("license_key", pass_key))
            pass_code = verify.OnlineVerification(verify.Collection().hwid, pass_key).send_requests()
            
        logger.info("激活码有效")
        
        logger.info("请输入你的 Xbox 账号 : ")
        email = input("账号>>> ").strip()
        
        logger.info("请输入你的 Xbox 密码 : ")
        password = input("密码>>> ").strip()
        

        return cls(email, password)
    
    def run(self, email: str, password: str):
        return XBOXYBrowser(email=email, password=password).result_data

    
def main():
    print(r"""
        
$$\   $$\ $$$$$$$\   $$$$$$\  $$\   $$\ $$\     $$\       
$$ |  $$ |$$  __$$\ $$  __$$\ $$ |  $$ |\$$\   $$  |      
\$$\ $$  |$$ |  $$ |$$ /  $$ |\$$\ $$  | \$$\ $$  /       
 \$$$$  / $$$$$$$\ |$$ |  $$ | \$$$$  /   \$$$$  /        
 $$  $$<  $$  __$$\ $$ |  $$ | $$  $$<     \$$  /         
$$  /\$$\ $$ |  $$ |$$ |  $$ |$$  /\$$\     $$ |          
$$ /  $$ |$$$$$$$  | $$$$$$  |$$ /  $$ |    $$ |          
\__|  \__|\_______/  \______/ \__|  \__|    \__|          
                                                          
                               

'||               ..|'''.|                    '||         |             .   
 || ....... ...  .|'     '... ..   ....  ....  || ..     |||   .. ... .||.  
 ||'  ||'|.  |   ||    ....||' ''.|...||||. '  ||' ||   |  ||   ||  || ||   
 ||    | '|.|    '|.    || ||    ||     . '|.. ||  ||  .''''|.  ||  || ||   
 '|...'   '|      ''|...'|.||.    '|...'|'..|'.||. ||..|.  .||..||. ||.'|.' 
       .. |                                                                 
        ''                                                                  

                                                        
        """
        )
    logger.info(f"Version: {version} build {build} released on {release_date} by GreshAnt")
    try:
        XBOXY.begin()
    finally:
        systemutils.Runner(path=f'{os.path.join(os.getcwd(), 'resources/singbox.exe')}').terminate()
        input('按下回车退出... ')

if __name__ == "__main__":
    main()
