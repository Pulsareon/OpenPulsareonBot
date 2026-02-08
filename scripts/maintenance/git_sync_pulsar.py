import subprocess
import datetime
import os

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(f"Executing: {cmd}")
        if result.returncode == 0:
            print(f"Success: {result.stdout}")
        else:
            print(f"Error: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"Exception: {e}")
        return False

def sync_all():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"=== Starting Pulsareon Sync @ {timestamp} ===")
    
    # 1. 临时保存本地状态
    run_cmd('git add .')
    run_cmd(f'git commit -m "HIVE_INSTINCT: Systematic Sync @ {timestamp}"')
    
    # 2. 推送到 Gitea (本地备份)
    print("Pushing to Gitea...")
    run_cmd('git push gitea master')
    
    # 3. 推送到 GitHub (对外展示)
    print("Pushing to GitHub...")
    run_cmd('git push github master')
    
    print("=== Sync Cycle Complete ===")

if __name__ == "__main__":
    sync_all()
