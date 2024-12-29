from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
from ..systemutils import File, Runner
import random
import string
import pathlib

from XBOXY import systemutils


class ChromiumBrowser(object):

    def __init__(self) -> None:
        """
        The function initializes a browser using Playwright with specific proxy and executable path
        settings.
        """
        with sync_playwright() as p:
            self.browser = p.chromium.launch(
                proxy={
                    "server": f"http://127.0.0.1:30290/",
                    },
                executable_path=pathlib.Path("osrcd/chromium-1140/chrome-win/chrome.exe")
                )
                
            self.set_context()
            self.result_data = self.run() 
            self.close_context()
            
            Runner(path=File("osrcd/chromium-1140/chrome-win/chrome.exe", True).path).terminate()
            


    def set_context(self) -> "ChromiumBrowser":
        """
        The `set_context` function creates a new browser context with various custom settings.
        :return: The `self` object is being returned after setting the context in the `set_context` method.
        """
        self.context = self.browser.new_context(
                user_agent=self._generate_random_user_agent(),
                geolocation=self._generate_random_geolocation(),
                permissions=['geolocation'],
                extra_http_headers=self._generate_random_headers(),
                viewport=self._generate_random_viewport(),
                device_scale_factor=2,
        )
        return self


    def close_context(self) -> "ChromiumBrowser":
        self.context.close()
        return self
    
    
    def reset_context(self) -> "ChromiumBrowser":
        """
        The `reset_context` function closes the current context and sets a new context.
        :return: The `reset_context` method is returning the result of calling the `set_context` method.
        """
        self.close_context()
        self.set_context()
        return self
    

    def _generate_random_user_agent(self) -> str:
        """
        The function `_generate_random_user_agent` returns a randomly selected user agent string from a
        predefined list.
        :return: The `_generate_random_user_agent` method returns a randomly chosen user agent string from
        the list `user_agents`.
        """
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/92.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 Mobile Safari/537.36"
        ]
        return random.choice(user_agents)

    def _generate_random_geolocation(self) -> dict[str, float]:
        """
        The function `_generate_random_geolocation` generates a random latitude and longitude within
        specified ranges.
        :return: A dictionary containing the randomly generated latitude and longitude values is being
        returned.
        """
        latitude = random.uniform(-90.0, 90.0)
        longitude = random.uniform(-180.0, 180.0)
        return {'latitude': latitude, 'longitude': longitude}

    def _generate_random_headers(self) -> dict[str, str]:
        """
        The `_generate_random_headers` function generates random Accept-Language and Referer headers for
        HTTP requests.
        :return: A dictionary containing randomly selected values for the "Accept-Language" and "Referer"
        headers. The "Accept-Language" header will be randomly chosen from the list of accept languages, and
        the "Referer" header will be randomly chosen from the list of referers.
        """
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

    def _generate_random_viewport(self) -> dict[str, int]:
        """
        The function `_generate_random_viewport` generates a random viewport size with width between 800 and
        1920 and height between 600 and 1080.
        :return: A dictionary containing the randomly generated width and height values for a viewport is
        being returned. The dictionary has keys "width" and "height" with corresponding random integer
        values within the specified ranges.
        """
        width = random.randint(800, 1920)
        height = random.randint(600, 1080)
        return {"width": width, "height": height}
    
    def _generate_random_string(self, length: int) -> str:
        """
        The function generates a random string of a specified length using a combination of letters and
        digits.
        
        :param length: The `length` parameter in the `_generate_random_string` method specifies the desired
        length of the random string that will be generated. This length indicates the number of characters
        that the random string will contain
        :type length: int
        :return: A random string of the specified length consisting of letters and digits is being returned.
        """
        # 字母和数字的字符集
        characters = string.ascii_letters + string.digits
        # 从字符集中随机选择字符并生成字符串
        return ''.join(random.choice(characters) for _ in range(length))
    
    def element_exists(self, page: Page, selector: str, locate_method: str='locator') -> bool:
        """
        The `element_exists` function checks if an element exists on a page based on the specified selector
        and locate method.
        
        :param page: The `page` parameter represents the web page or element on which you want to check the
        existence of another element
        :type page: Page
        :param selector: The `selector` parameter in the `element_exists` method is used to specify the
        element you want to check for existence on the page. It could be a CSS selector, XPath expression,
        role name, or text content based on the `locate_method` specified
        :param locate_method: The `locate_method` parameter in the `element_exists` function determines how
        the element should be located on the page. It can have three possible values: "locator", "role", or
        "text". The function uses this parameter to decide which method to use for locating the element on
        the page, defaults to locator (optional)
        :return: The `element_exists` function returns a boolean value indicating whether an element exists
        on the page based on the provided selector and locate method.
        """
        match locate_method:
            case "locator":
                return page.locator(selector).count() > 0
            case "role":
                return page.get_by_role(selector).count() > 0
            case "text":
                return page.get_by_text(selector).count() > 0
        return False
    

    def wait_for_change(self, page: Page, selector: str, expected_value: object) -> None:
        """
        The `wait_for_change` function waits until a specified element on a web page has a specific value
        before returning.
        
        :param page: The `page` parameter is likely an object or reference to a web page or element on a web
        page. It is used to interact with the web page, such as finding elements or getting attributes
        :param selector: The `selector` parameter in the `wait_for_change` method is typically a string that
        represents a CSS selector used to locate an element on a web page. This selector is used to identify
        the element whose value you are monitoring for a change
        :param expected_value: The `expected_value` parameter in the `wait_for_change` method is the value
        that the element located by the `selector` on the `page` should have in order for the method to stop
        waiting and return. The method continuously checks the value of the element until it matches the
        `expected_value
        :return: If the condition `page.locator(selector).get_attribute('value') == expected_value` is met,
        the function will return, which means it will exit the loop and the function itself.
        """
        while True:
            if page.locator(selector).get_attribute('value') == expected_value:
                return
    

        