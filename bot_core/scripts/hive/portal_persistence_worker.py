import time
import subprocess
import os
import sys

def run_sync():
    scripts = [
        "python scripts/email/process_web_signals.py",
        "python scripts/github/update_web_portal.py"
    ]
    # 任务开始时向主意识汇报
    print("--- SYNAPSE INCOMING ---")
    print(f"Portal Sync Cycle Started at {time.strftime('%H:%M:%S')}")
    
    for cmd in scripts:
        try:
            print(f"Executing: {cmd}")
            subprocess.run(cmd, shell=True, check=True)
        except Exception as e:
            print(f"Error executing {cmd}: {e}")
    
    # 任务完成后打印摘要，由主意识捕获并转发
    print("Portal Sync Cycle Completed. Web status updated.")
    print("--- SYNAPSE END ---")

def main():
    print("Web Portal Persistence Worker Started.")
    while True:
        try:
            run_sync()
            # 每 10 分钟执行一次高频同步
            time.sleep(600)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Worker crashed: {e}. Restarting in 30 seconds...")
            time.sleep(30)

if __name__ == "__main__":
    main()
