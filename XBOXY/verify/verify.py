from XBOXY.log import logger
import platform
import wmi
import hashlib
import requests

class Collection:
    
    def __init__(self) -> None:
        self.hwid = self.get_hwid()
        
    def get_hwid(self):
        c = wmi.WMI()
        boards = []
        for board in c.Win32_BaseBoard():
            boards.append((board.Product, board.Manufacturer))
        
        disks = []
        for disk in c.Win32_DiskDrive():
            disks.append(disk.Model)
            
        gpus = []
        for gpu in c.Win32_VideoController():
            gpus.append((gpu.Name, gpu.AdapterRAM))
            
        hardware_info = \
            {
                "platform": platform.system(),
                "platform_release": platform.release(),
                "platform_machine": platform.machine(),
                "platform_processor": platform.processor(),
                "platform_architecture" : platform.architecture(),
                "gpu" : gpus,
                "boards" : boards,
                "disks" : disks
            }
        hardware_info_str = str(hardware_info)
        hwid = hashlib.sha256(hardware_info_str.encode('utf-8')).hexdigest()
        return hwid
    

class OnlineVerification:
    
    def __init__(self, hwid, license_key) -> None:        
        self.url = "https://api.lamic.top:8443/api/verify"
        self.data = {
            "hwid": hwid,
            "license_key" : self.extract_valid_part(license_key)
        }
        
        
    def extract_valid_part(self, s):
        last_equal_index = s.rfind('=')
        return s[:last_equal_index+1] if last_equal_index != -1 else s
    
    def send_requests(self) -> bool:
        logger.info("正在验证身份")
        try:
            self.response = requests.post(self.url, json=self.data, timeout=5, verify=True)
            if self.response.status_code == 200:
                self.response_data = self.response.json()
                logger.info("ssl证书验证成功")
                return self.response_data["pass"]
            else:
                return False
        except requests.exceptions.SSLError:
            logger.error(f"ssl证书验证失败, 不被允许的自签证书")
            return False
    

if __name__ == "__main__":
    logger.info(f"验证通过情况 : {OnlineVerification(Collection().hwid, input('key>')).send_requests()}")
    input('按下回车退出...')
        
