import os
import sys
import time
import subprocess
import signal

def start_watchdog(timeout, revert_cmd):
    print(f"[HIVE WATCHDOG] Started. Timeout: {timeout}s. Revert Command: {revert_cmd}")
    
    # 创建一个信号文件，用于主脑解除警报
    disarm_file = "data/watchdog_disarm.signal"
    if os.path.exists(disarm_file):
        os.remove(disarm_file)
        
    start_time = time.time()
    
    try:
        while time.time() - start_time < timeout:
            if os.path.exists(disarm_file):
                print("[HIVE WATCHDOG] Disarmed by Overmind. Mission Success.")
                os.remove(disarm_file)
                return
            time.sleep(5)
            
        # 超时，触发灾难恢复
        print("[HIVE WATCHDOG] TIMEOUT! Triggering emergency revert...")
        subprocess.run(revert_cmd, shell=True)
        print("[HIVE WATCHDOG] Revert complete. System should be stable.")
        
    except Exception as e:
        print(f"[HIVE WATCHDOG] Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python hive_watchdog.py <timeout_sec> <revert_cmd>")
    else:
        start_watchdog(int(sys.argv[1]), sys.argv[2])
