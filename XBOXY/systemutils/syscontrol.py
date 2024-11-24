import subprocess
import psutil
import pathlib


class Runner(object):
    def __init__(self, cmd=None, path=None):
        self.cmd = cmd
        self.path = path

        
    def run(self):
        process = subprocess.Popen(["powershell", "-Command", self.cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        return process.pid
        
    def terminate(self):
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                if proc.info['exe'] == pathlib.Path(self.path):
                    print(f"终止进程: {proc.info['name']} (PID: {proc.info['pid']})")
                    proc.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass