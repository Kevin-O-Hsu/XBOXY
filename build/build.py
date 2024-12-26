import subprocess

working_directory = r'G:\Programming\XBOXY_313'

command = f'nuitka --playwright-include-browser=none --onefile --include-data-dir=resources=resources --include-data-file=resources/singbox.exe=resources/singbox.exe --show-scons --windows-uac-admin --output-dir=build/cache --standalone xboxy.py '


process = subprocess.Popen(["powershell", "-Command", command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, cwd=working_directory, bufsize=1)
for line in process.stdout:
    print(line, end="")
    
