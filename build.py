import subprocess
from pathlib import Path
from typing import List
working_directory = r'G:\Programming\XBOXY'
def get_all_file_relative_paths(directory: str) -> List[str]:
    """
    获取指定目录中所有文件的相对路径。

    :param directory: 要搜索的目录路径。
    :return: 包含所有文件相对路径的列表。
    """
    file_paths = []
    dir_path = Path(directory)
    
    if not dir_path.exists() or not dir_path.is_dir():
        raise ValueError(f"指定路径 {directory} 不是有效的目录！")
    
    # 遍历目录及子目录中的所有文件
    for file in dir_path.rglob("*"):  # 使用 rglob("*") 遍历所有文件和子文件夹
        if file.is_file():           # 确保是文件
            file_paths.append(str(file.relative_to(dir_path.parent)))  # 转为相对路径
    
    return file_paths


all_list = []

for x in get_all_file_relative_paths('osrcd'):
    all_list.append(f"--include-data-file={x}={x}")

all_str = ' '.join(all_list)


# # 要运行的 PowerShell 命令
# with open('ar.txt', 'w') as f:
#     f.write(all_str)
    



command = f'nuitka --onefile --include-data-dir=resources=resources --include-data-file=resources/singbox.exe=resources/singbox.exe --show-scons --windows-uac-admin --user-package-configuration-file=nuitka-playwright.yml --output-dir=cache --standalone xboxy.py '


process = subprocess.Popen(["powershell", "-Command", command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, cwd=working_directory, bufsize=1)
for line in process.stdout:
    print(line, end="")
    
