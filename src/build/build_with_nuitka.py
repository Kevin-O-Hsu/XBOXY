import subprocess


command = f'nuitka --playwright-include-browser=none --include-data-dir=resources=resources --include-data-file=resources/singbox.exe=resources/singbox.exe --windows-uac-admin --output-dir=cache --standalone xboxy.py'


process = subprocess.Popen(["powershell", "-Command", command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
for line in process.stdout:
    print(line, end="")
    
