from playwright.sync_api import sync_playwright
import random
import string
import pathlib


class ChromiumBrowser(object):

    def __init__(self) -> None:
        with sync_playwright() as p:
            self.browser = p.chromium.launch(
                proxy={
                    "server": f"http://127.0.0.1:30290/",
                    },
                executable_path=pathlib.Path("osrcd/chromium-1140/chrome-win/chrome.exe")
                )
                
            self.context = self.browser.new_context()
            self.result_data = self.run()

    def reset_context(self):
        self.context.close()
        self.context = self.browser.new_context(
                user_agent=self._generate_random_user_agent(),
                geolocation=self._generate_random_geolocation(),
                permissions=['geolocation'],
                extra_http_headers=self._generate_random_headers(),
                viewport=self._generate_random_viewport(),
                device_scale_factor=2,
        )
        return self
        
        
        

    def _generate_random_user_agent(self):
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/92.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36"
        ]
        return random.choice(user_agents)

    def _generate_random_geolocation(self):
        latitude = random.uniform(-90.0, 90.0)
        longitude = random.uniform(-180.0, 180.0)
        return {'latitude': latitude, 'longitude': longitude}

    def _generate_random_headers(self):
        accept_languages = [
            "en-US,en;q=0.9",
            "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
            "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
            "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        ]
        referers = [
            "https://www.google.com/",
            "https://www.bing.com/",
            "https://www.yahoo.com/",
            "https://duckduckgo.com/",
            "https://www.baidu.com/"
        ]
        return {
            "Accept-Language": random.choice(accept_languages),
            "Referer": random.choice(referers)
        }

    def _generate_random_viewport(self):
        width = random.randint(800, 1920)
        height = random.randint(600, 1080)
        return {"width": width, "height": height}
    
    def _generate_random_string(self, length: int):
        # 字母和数字的字符集
        characters = string.ascii_letters + string.digits
        # 从字符集中随机选择字符并生成字符串
        return ''.join(random.choice(characters) for _ in range(length))
    
    def element_exists(self, page, selector):
        return page.locator(selector).count() > 0
    

    def wait_for_change(self, page, selector, expected_value):
        while True:
            if page.locator(selector).get_attribute('value') == expected_value:
                return
    

        