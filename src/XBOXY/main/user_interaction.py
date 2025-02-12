import pathlib
import msvcrt
import ctypes

from .main_handle import XBOXY
from .. import log
from ..systemutils import JsonFile

logger = log.logger

version = 'v1.0.4'
release_date = '2025-2-12'
build = '5'

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

ctypes.windll.kernel32.SetConsoleTitleW(f"XBOXY {version} build {build} by GreshAnt")
try:
    xboxy = XBOXY()
    output_file = JsonFile("output.json")

    xboxy.initialize()
    xboxy.run()
    logger.info(xboxy.result)
    for link in xboxy.result:
        output_file.append(link)
        
except Exception as e:
    # logger.error(e)
    pass
    
finally:
    if len(output_file.get_json_data()) == 0:
        output_file.del_file()
    xboxy.cleanup()
    print("按下任意键退出...")
    msvcrt.getch()  # 等待按下任意键

