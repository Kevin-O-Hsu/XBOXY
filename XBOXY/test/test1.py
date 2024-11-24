import os
from pathlib import Path
import sys


import os
from pathlib import Path

# 获取命令行工作目录
command_line_dir = os.getcwd()

# 获取脚本文件所在目录
script_dir = Path(__file__).resolve().parent

print("命令行所在目录:", command_line_dir)
print("脚本文件所在目录:", script_dir)
