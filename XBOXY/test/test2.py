from XBOXY.browser import ChromiumBrowser


class TestBrowser(ChromiumBrowser):
    
    def __init__(self) -> None:
        super().__init__()
        
    def copy(self, page, locator):
        return page.locator(locator).evaluate_handle("""
            () => {
                const event = new ClipboardEvent('copy', { 
                    bubbles: true, 
                    cancelable: true, 
                    clipboardData: new DataTransfer() 
                });
                window.getSelection()?.anchorNode?.dispatchEvent(event);
                return event.clipboardData.getData('text/plain');;
            }
        """)
    
    
    def run(self):
        p = self.context.new_page()
        p.goto('https://www.gtboost.xyz/')
        
        p.wait_for_load_state("networkidle", timeout=0)
        
        p.locator('span[id="ip1"]').click()
        
        print(self.copy(p, 'span[id="ip1"]'))
        
if __name__ == '__main__':
    browser = TestBrowser()
    