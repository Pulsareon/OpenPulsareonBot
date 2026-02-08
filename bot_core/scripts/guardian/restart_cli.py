import subprocess
import os
import time
import sys

# 淇 Windows 缂栫爜
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

EXE_PATH = r"C:\Users\Administrator\Desktop\CLIProxyAPI_6.7.46_windows_amd64\cli-proxy-api.exe"
WORK_DIR = r"C:\Users\Administrator\Desktop\CLIProxyAPI_6.7.46_windows_amd64"

def restart():
    print("鈿狅笍 Killing CLI Proxy API...")
    os.system("taskkill /f /im cli-proxy-api.exe")
    time.sleep(3)
    
    print("馃殌 Starting CLI Proxy API...")
    try:
        # DETACHED_PROCESS = 0x00000008
        CREATE_NEW_CONSOLE = 0x00000010
        subprocess.Popen(
            [EXE_PATH], 
            cwd=WORK_DIR, 
            creationflags=CREATE_NEW_CONSOLE
        )
        print("鉁?Command sent. Service should be restarting.")
    except Exception as e:
        print(f"鉂?Start failed: {e}")

if __name__ == "__main__":
    restart()

