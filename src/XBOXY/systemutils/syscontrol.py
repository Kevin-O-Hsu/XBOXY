import subprocess
import psutil
import pathlib
from ..log import logger


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
        
            