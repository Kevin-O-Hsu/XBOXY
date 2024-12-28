import subprocess
import psutil
import pathlib


# The `Runner` class in Python initializes with optional command and path attributes.
class Runner(object):
    def __init__(self, cmd=None, path=None):
        """
        The function is a Python constructor that initializes two attributes, cmd and path, with optional
        default values.
        
        :param cmd: The `cmd` parameter in the `__init__` method is used to store a command or instruction.
        It is a parameter that can be passed when creating an instance of the class
        :param path: The `path` parameter in the `__init__` method is used to specify the path where the
        command should be executed or where the output of the command should be saved. It allows you to
        define the working directory for the command execution or specify the location for saving files
        """
        self.cmd = cmd
        self.path = path

        
    def run(self):
        """
        This Python function runs a PowerShell command and returns the process ID of the subprocess.
        :return: The `pid` (process ID) of the subprocess that is created by running the PowerShell command
        specified in `self.cmd` is being returned.
        """
        process = subprocess.Popen(["powershell", "-Command", self.cmd], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        return process.pid
        
    def terminate(self):
        """
        The `terminate` function terminates processes with a specific executable path.
        """
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                if proc.info['exe'] == pathlib.Path(self.path):
                    print(f"终止进程: {proc.info['name']} (PID: {proc.info['pid']})")
                    proc.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass