import pathlib
import os


from .main_handle import XBOXY
from .. import log
from ..systemutils import JsonFile

logger = log.logger

version = 'v1.0.3'
release_date = '2024-12-23'
build = '4'
update_note = \
    """
    v1.0.3 b1
    * 修复了一些已知问题
    * 解决了无法下一步的问题
    * 使用无头模式，即浏览器窗口不可见
    * 可以从文件导入账号密码，且会根据格式自动识别，乱七八糟的格式也可以尝试丢进来
    * 优化了部分代码
    * 拒绝selenium等老套框架，更加高效先进
    * 优化了Build的流程和release的文件管理
    
    v1.0.3 b2
    * 修复了一些已知问题
    
    v1.0.3 b3
    * 修复了部分已知问题
    * 优化了部分代码
    
    v1.0.3 b4
    * 修复了输入账户后一直卡住的问题
    * 增加了发包的随机性，不易检测出是机器人
    * 修复了一些已知问题
    
    """
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
logger.info(update_note)

try:
    xboxy = XBOXY()
    output_file = JsonFile(pathlib.Path("output.json"), needed=True)
    output_file.create_file()
    xboxy.initialize()
    xboxy.run()
    logger.info(xboxy.result)
    for link in xboxy.result:
        output_file.append(link)
        
except Exception as e:
    pass
    
finally:
    if len(output_file.get_json_data()) == 0:
        output_file.del_file()
    xboxy.cleanup()
    input("按回车退出...")
    os._exit(0)

    