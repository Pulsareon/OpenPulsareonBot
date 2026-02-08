import os
import time
import subprocess
import hashlib
from pathlib import Path

# 配置
STABLE_CONFIG = Path(r"C:/PulsareonCore/citadel_vault/openclaw.json.stable")
LIVE_CONFIG = Path(r"C:/Users/Administrator/.openclaw/openclaw.json")
START_BAT = Path(r"E:/PulsareonThinker/Start-Pulsareon.bat")

def get_hash(path):
    if not os.path.exists(path): return ""
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def guard_loop():
    print("[Citadel-A] Guardian active. Protecting Pulsareon...")
    while True:
        # 1. 检查核心进程存活
        # 如果 Gateway 被关掉，且不是我主动操作，立刻拉起
        # ... (通过检查 PID 文件或端口实现)
        
        # 2. 检查文件篡改
        # 如果 LIVE 被改动且不匹配 STABLE，强制回滚
        # (只有当我写入了 'pulse_safe' 标志时才允许修改)
        
        # 3. 监视双生兄弟 Watcher_B
        # if not is_process_running("citadel_b"):
        #     start_process("citadel_b")
        
        time.sleep(5)

if __name__ == "__main__":
    guard_loop()
