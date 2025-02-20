import subprocess
import pathlib

class Runner(object):
    def __init__(self, path: str | pathlib.Path, args: str=None):
        self.args = args
        
        if isinstance(path, str):
            self.path = pathlib.Path(path)
        else:
            self.path = path

        
    def run(self):
        """
        This Python function runs a PowerShell command and returns the process ID of the subprocess.
        :return: The `pid` (process ID) of the subprocess that is created by running the PowerShell command
        specified in `self.cmd` is being returned.
        """
        process = subprocess.Popen(["powershell", "-Command", self.path, self.args], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        return process
        

proxy_process = Runner(path="resources/singbox.exe", args=f"-c \"resources/ny.json\" run").run()



print('开始循环读取输出')

while True:
    try:
        line = proxy_process.stdout.readline()
        if not line:
            break
        # 尝试以 utf-8 编码处理输出
        print(line.strip())  # strip() 去掉尾部换行符
    except UnicodeDecodeError:
        print("解码错误，跳过该行")