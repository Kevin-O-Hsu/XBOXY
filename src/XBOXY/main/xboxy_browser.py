import re
from .. import browser
from ..log import logger

class XBOXYBrowser(browser.ChromiumBrowser):
    """
    浏览器操作类，用于模拟登录 Xbox。
    """
    def __init__(self, email: str, password: str) -> None:
        logger.info('启动Playwright...')
        self.email = email
        self.password = password
        logger.info(f'当前处理的账号是{self.email}')
        super().__init__()
    
    def run(self) -> list[str]:
        """
        模拟浏览器登录流程并获取可用链接。
        """
        p = self.context.new_page()
        logger.info("前往Xbox 登录页面...")
        p.goto(
            r'https://www.xbox.com/zh-hk/auth/msa?action=logIn&returnUrl=https%3A%2F%2Fwww.xbox.com%2Fzh-HK%2Fxbox-game-pass%2Finvite-your-friends&ru=https%3A%2F%2Fwww.xbox.com%2Fzh-HK%2Fxbox-game-pass%2Finvite-your-friends'
        )
        p.wait_for_load_state("networkidle", timeout=0)

        # 输入账号和密码进行登录
        logger.info("输入账号和密码尝试登录...")
        p.locator('input[id="i0116"]').fill(self.email)
        self.wait_for_change(p, 'input[id="i0116"]', self.email)
        p.locator('button[type="submit"]').click()
        p.wait_for_load_state("networkidle", timeout=0)
        
        while not self.element_exists(p, 'input[id="i0118"]'):
            if self.element_exists(p, 'alert', 'role'):
                logger.warning("无法登录")
                return []
            
            if self.element_exists(p, 'input[id="idTxtBx_OTC_Password"]'):
                p.locator('span[role="button"][id="idA_PWD_SwitchToCredPicker"]').click()
                p.locator('#tileList > div:nth-child(2) > div > button').click()
            
        p.wait_for_load_state("networkidle", timeout=0)
        p.locator('input[id="i0118"]').fill(self.password)
        self.wait_for_change(p, 'input[id="i0118"]', self.password)
        p.locator('button[type="submit"]').click()
        p.wait_for_load_state("networkidle", timeout=0)


        if self.element_exists(p, 'div[id="i0118Error"]'):
            logger.warning("密码错误")
            return []
        
        if self.element_exists(p, '#i1011'):
            logger.warning("无法登录")
            return []
        
        if self.element_exists(p, 'div[class="UpdatePasswordPageContainer PageContainer"]'):
            logger.warning("需要更新密码, 无法登录")
            return []
        
        if self.element_exists(p, 'input[type="button"][id="iLandingViewAction"]'):
            p.locator('input[type="button"][id="iLandingViewAction"]').click()
            p.wait_for_load_state("networkidle", timeout=0)
            
        if self.element_exists(p, 'div[role="heading"][id="serviceAbuseLandingTitle"]'):
            logger.warning("需要验证邮箱, 无法登录")
            return []
        
        if self.element_exists(p, 'div[id="iSelectProofTitle"]'):
            logger.warning("需要验证身份, 无法登录")
            return []
        
        if self.element_exists(p, 'select[id="iProofOptions"]'):
            if self.element_exists(p, 'a[id="iShowSkip"]'):
                p.locator('a[id="iShowSkip"]').click()
            else:
                logger.warning("无法登录")
                return []
            
        if self.element_exists(p, '#pageContent > form:nth-child(2) > div.___1cj7yg8.f183mx53.f1turhiw.f1rmqj0e > div > div > div > div:nth-child(1) > button'):
            p.locator('#pageContent > form:nth-child(2) > div.___1cj7yg8.f183mx53.f1turhiw.f1rmqj0e > div > div > div > div:nth-child(1) > button').click()
            
        p.wait_for_load_state("networkidle", timeout=0)
        p.locator('button[id="acceptButton"]').click()
        p.wait_for_load_state("networkidle", timeout=0)
        
        if self.element_exists(p, 'input[id="create-account-gamertag-input"]'):
            logger.warning("该账号还没有创建XBOX账号, 不可能有配额")
            return []
            
        
        p.wait_for_selector('#BuddyPassSender > div > div > p')
        display_sentence = p.locator('#BuddyPassSender > div > div > p').text_content()
        logger.info(f"网页显示 {display_sentence}")
        
        last_quota = re.findall(r'\d+', display_sentence)[0]
        
        
        match int(last_quota):
            case 0:
                logger.warning("没有可用配额")
                return []
            
            case 7:
                logger.warning("不可使用")
                return []
            
        
        links = []
        for _ in range(int(last_quota)):
            logger.info(f"正在获取第 {_ + 1} 个链接...")
            p.locator('#BuddyPassSender > div > div > div.c-table > div > button').click()
            p.wait_for_load_state("networkidle", timeout=0)
            link = p.locator('a[class="c-call-to-action c-glyph f-lightweight"]').nth(-1).get_attribute('href')
            links.append(link)
            p.locator(
                'body > reach-portal > div:nth-child(3) > div > div > div > div > div.Modal-module__closeContainer___kCjh7 > button'
            ).click()
        
        logger.info(f"已获取 {len(links)} 个链接")

        return links