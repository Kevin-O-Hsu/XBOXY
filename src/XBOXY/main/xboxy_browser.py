import re
import time

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
        super().__init__()
    
    def run(self) -> list[str]:
        """
        模拟浏览器登录流程并获取可用链接。
        """
        p = self.context.new_page()
        logger.info(f"前往Xbox 登录页面... - {self.email}")
        p.goto(
            r'https://www.xbox.com/zh-hk/auth/msa?action=logIn&returnUrl=https%3A%2F%2Fwww.xbox.com%2Fzh-HK%2Fxbox-game-pass%2Finvite-your-friends&ru=https%3A%2F%2Fwww.xbox.com%2Fzh-HK%2Fxbox-game-pass%2Finvite-your-friends'
        )
        p.wait_for_load_state("load", timeout=0)
        p.wait_for_load_state("networkidle", timeout=0)
        # 输入账号和密码进行登录
        logger.info(f"输入账号和密码尝试登录... - {self.email}")
        
        while True:
            if self.element_exists(p, 'input[id="i0116"]'):
                email_selector = 'input[id="i0116"]'
                break
            elif self.element_exists(p, 'input[type="email"][id="usernameEntry"]'):
                email_selector = 'input[type="email"][id="usernameEntry"]'
                break
            else:
                continue
            
        p.locator(email_selector).fill(self.email)
        self.wait_for_change(p, email_selector, self.email)
        p.locator('button[type="submit"]').click()
        p.wait_for_load_state("networkidle", timeout=0)
        
        
        start_time = time.time()
        while True:
            p.wait_for_load_state("networkidle", timeout=0)
            
            if time.time() - start_time > 10:
                logger.warning(f"登录超时 - {self.email}")
                return []
            
            if self.element_exists(p, 'div[data-testid="deviceShieldCheckmarkVideo"]'):
                p.locator('#view > div > span > div > span').click()
                continue
            
            if (self.element_exists(p, 'span[tabindex="0"][id="idA_PWD_SwitchToPassword"]')\
                and p.locator('span[tabindex="0"][id="idA_PWD_SwitchToPassword"]').is_visible()):
                p.locator('span[tabindex="0"][id="idA_PWD_SwitchToPassword"]').click()
                continue
            
            if self.element_exists(p, 'div[id="field-7__validationMessage"]'):
                logger.warning(f"无法登录 - {self.email}")
                return []
            
            if self.element_exists(p, 'div[data-testid="codeEntry"]'):
                logger.warning(f"需要验证码, 无法登录 - {self.email}")
                return []
            
            if self.element_exists(p, 'div[id="i0116Error"]'):
                logger.warning(f"账号错误 - {self.email}")
                return []
            
            if (self.element_exists(p, 'input[id="idTxtBx_OTC_Password"]')\
                and p.locator('span[role="button"][id="idA_PWD_SwitchToCredPicker"]').is_visible()):
                p.locator('span[role="button"][id="idA_PWD_SwitchToCredPicker"]').click()
                p.locator('#tileList > div:nth-child(2) > div > button').click()
                continue
            
            if self.element_exists(p, 'input[id="i0118"]'):
                password_selector = 'input[id="i0118"]'
                break
            
            elif self.element_exists(p, 'input[type="password"][name="passwd"]'):
                password_selector = 'input[type="password"][name="passwd"]'
                break

        p.locator(password_selector).fill(self.password)
        self.wait_for_change(p, password_selector, self.password)
        p.locator('button[type="submit"]').click()
        p.wait_for_load_state('networkidle', timeout=0)
        
        wait_start_time = time.time()
        
        while not self.element_exists(p, 'button[id="acceptButton"]'):
            p.wait_for_load_state("networkidle", timeout=0)
            
            if time.time() - wait_start_time > 10:
                logger.warning(f"登录超时 - {self.email}")
                return []
            
            if self.element_exists(p, 'div[id="idTD_Error"]'):
                logger.warning(f"登录被阻止 - {self.email}")
                return []
            
            if self.element_exists(p, 'img[data-testid="errorImage"]'):
                logger.warning(f"登录被阻止 - {self.email}")
                return []
            
            if self.element_exists(p, 'div[id="i0118Error"]'):
                logger.warning(f"密码错误 - {self.email}")
                return []
            
            if self.element_exists(p, 'alert', 'role'):
                logger.warning(f"无法登录 - {self.email}")
                return []
            
            if self.element_exists(p, '#i1011'):
                logger.warning(f"无法登录 - {self.email}")
                return []
            
            if self.element_exists(p, 'div[class="UpdatePasswordPageContainer PageContainer"]'):
                logger.warning(f"需要更新密码, 无法登录 - {self.email}")
                return []
            
            if self.element_exists(p, 'input[id="otc-confirmation-input"]'):
                logger.warning(f"有两步验证, 无法登录 - {self.email}")
                return []
            
            if self.element_exists(p, 'input[type="button"][id="iLandingViewAction"]'):
                p.locator('input[type="button"][id="iLandingViewAction"]').click()
                continue
                
            if self.element_exists(p, 'div[role="heading"][id="serviceAbuseLandingTitle"]'):
                logger.warning(f"需要验证邮箱, 无法登录 - {self.email}")
                return []
            
            if self.element_exists(p, 'div[id="iSelectProofTitle"]'):
                logger.warning(f"需要验证身份, 无法登录 - {self.email}")
                return []
            
            if self.element_exists(p, 'select[id="iProofOptions"]'):
                if self.element_exists(p, 'a[id="iShowSkip"]'):
                    p.locator('a[id="iShowSkip"]').click()
                else:
                    logger.warning(f"无法登录 - {self.email}")
                    return []
            
            if self.element_exists(p, 'div[id="identityPageBanner"]'):
                p.locator('button[id="iLandingViewAction"]').click()
                continue
            
            if self.element_exists(p, '#pageContent > form:nth-child(2) > div.___1cj7yg8.f183mx53.f1turhiw.f1rmqj0e > div > div > div > div:nth-child(1) > button'):
                p.locator('#pageContent > form:nth-child(2) > div.___1cj7yg8.f183mx53.f1turhiw.f1rmqj0e > div > div > div > div:nth-child(1) > button').click()
                continue

        p.wait_for_load_state("networkidle", timeout=0)
        p.locator('button[id="acceptButton"]').click()
        p.wait_for_load_state("networkidle", timeout=0)
        p.wait_for_load_state("load", timeout=0)
        
               
        if self.element_exists(p, 'input[id="create-account-gamertag-input"]'):
            logger.warning(f"该账号还没有创建XBOX账号, 不可能有配额 - {self.email}")
            return []
            
        
        p.wait_for_selector('p[class="c-paragraph-1 nonMemDisclaimerText"]')
        display_sentence = p.locator('p[class="c-paragraph-1 nonMemDisclaimerText"]').text_content()
        logger.info(f"网页显示 {display_sentence}")
        
        last_quota = re.findall(r'\d+', display_sentence)[0]
        
        
        match int(last_quota):
            case 0:
                logger.warning(f"没有可用配额 - {self.email}")
                return []
            
            case 7:
                logger.warning(f"不可使用 - {self.email}")
                return []
            
        
        links = []
        for _ in range(int(last_quota)):
            logger.info(f"正在获取第 {_ + 1} 个链接... - {self.email}")
            p.locator('#BuddyPassSender > div > div > div.c-table > div > button').click()
            p.wait_for_load_state("networkidle", timeout=0)
            link = p.locator('a[class="c-call-to-action c-glyph f-lightweight"]').nth(-1).get_attribute('href')
            links.append(link)
            p.locator(
                'body > reach-portal > div:nth-child(3) > div > div > div > div > div.Modal-module__closeContainer___kCjh7 > button'
            ).click()
        
        logger.info(f"已获取 {len(links)} 个链接 - {self.email}")

        return links