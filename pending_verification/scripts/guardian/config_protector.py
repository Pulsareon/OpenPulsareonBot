import os
import shutil
import time
import subprocess
from pathlib import Path

CONFIG_PATH = Path(r"C:/Users/Administrator/.openclaw/openclaw.json")
BACKUP_PATH = Path(r"C:/PulsareonCore/openclaw-config/openclaw.json.stable")

def create_checkpoint():
    """在进行高危操作前创建检查点"""
    if CONFIG_PATH.exists():
        # 确保备份目录存在
        BACKUP_PATH.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(CONFIG_PATH, BACKUP_PATH)
        print(f"[Protector] Checkpoint created: {BACKUP_PATH}")
        
        # 写入看门狗指令
        with open("E:/PulsareonThinker/data/state/watchdog_checkpoint.json", "w") as f:
            import json
            json.dump({
                "timestamp": time.time(),
                "action": "core_config_modification",
                "timeout_seconds": 90, # 默认缩短至90秒，足以覆盖重启
                "recovery_cmd": f"copy {BACKUP_PATH} {CONFIG_PATH} /Y"
            }, f)

def commit_changes():
    """操作成功后，投喂看门狗，确认修改"""
    checkpoint = Path("E:/PulsareonThinker/data/state/watchdog_checkpoint.json")
    if checkpoint.exists():
        os.remove(checkpoint)
        print("[Protector] Changes committed. Watchdog fed.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "start": create_checkpoint()
        elif sys.argv[1] == "done": commit_changes()
