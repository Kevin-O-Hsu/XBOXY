from log import logger
import sys
from main.main_handle import XBOXY
from systemutils import JsonFile
import pathlib


# 防止出错信息被用户看到
sys.excepthook = lambda _, __, ___: None

version = 'v1.0.3'
release_date = '2024-11-17'
build = '1'
update_note = \
    """
    * 修复了一些已知问题
    * 解决了无法下一步的问题
    * 使用无头模式，即浏览器窗口不可见
    * 可以从文件导入账号密码，且会根据格式自动识别，乱七八糟的格式也可以尝试丢进来
    * 优化了部分代码
    * 拒绝selenium等老套框架，更加高效先进
    """

def main():
    """
    主函数，控制程序执行流程。
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
        output_file = JsonFile(pathlib.Path("output.json"))
        output_file.create_file()
        xboxy.initialize()
        xboxy.run()
        logger.info(xboxy.result)
        for link in xboxy.result:
            output_file.append(link)
    finally:
        xboxy.cleanup()
        input("按回车退出...")


if __name__ == "__main__":
    main()
