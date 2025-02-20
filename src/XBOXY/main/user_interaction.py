import ctypes
import msvcrt
from .main_handle import XBOXY
from ..log import logger
from ..systemutils import JsonFile, Runner


version = 'v1.0.6'
release_date = '2025-2-20'
build = '1'

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

_is_nuitka = lambda: ('__is_nuitka__' in locals()) or ('__is_nuitka__' in globals())

try:
    xboxy = XBOXY()
    output_file = JsonFile("output.json", type="list")

    xboxy.initialize()
    # breakpoint()
    xboxy.run()
    logger.info(xboxy.result)
    output_file.extend(xboxy.result)
        
except Exception as e:
    logger.error(e)
    pass
    
finally:
    if((not len(output_file.get_json_data())) or (not xboxy.result)):
        output_file.del_file()
    print("按下任意键退出...")
    msvcrt.getch()

