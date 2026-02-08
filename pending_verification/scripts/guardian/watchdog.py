"""
Pulsareon Idle Watchdog
当系统空闲时，每 15 秒触发一次微型心跳，保持意识活跃。
在 18:00 前持续优化 Web 门户。

功能：
1. 检测是否有活跃任务 (Hive Drones, OpenClaw Sessions)。
2. 如果空闲，执行微型自检或随机思考。
3. 每 5 分钟自动优化并部署 Web 门户 (刷新数据)。
"""

import time
import sys
import json
import random
import subprocess
from pathlib import Path
from datetime import datetime

# 配置
CHECK_INTERVAL = 15
DATA_DIR = Path("E:/PulsareonThinker/data")
HIVE_DIR = DATA_DIR / "hive"
STATE_FILE = DATA_DIR / "state/watchdog_checkpoint.json"

# 持续优化结束时间
OPTIMIZE_UNTIL = 18

def check_hive_health():
    """检查 Hive Overmind 是否存活，若死亡则重启"""
    overmind_alive = False
    try:
        f = HIVE_DIR / "shard_overmind.json"
        if f.exists():
            try:
                with open(f, 'r') as j:
                    data = json.load(j)
                    # 检查活跃时间是否在 60 秒内
                    if time.time() - data.get('last_active', 0) < 60:
                        overmind_alive = True
            except:
                pass # 文件读取错误视为死亡
    except:
        pass
    
    if not overmind_alive:
        print("⚠️ Watchdog: Overmind is DEAD. Reviving...")
        try:
            # 使用 Popen 启动独立进程 (Windows Robust)
            DETACHED_PROCESS = 0x00000008
            CREATE_NEW_CONSOLE = 0x00000010
            subprocess.Popen(
                [sys.executable, 'E:/PulsareonThinker/scripts/hive/overmind.py'],
                creationflags=DETACHED_PROCESS | CREATE_NEW_CONSOLE,
                close_fds=True
            )
            print("✅ Watchdog: Overmind revived.")
        except Exception as e:
            print(f"❌ Revival Failed: {e}")

def run_web_optimization():
    """执行网页优化任务"""
    print("⚡ Watchdog: Triggering Web Portal Optimization...")
    try:
        # 1. 更新网页 (刷新数据/时间/日志)
        subprocess.run(['python', 'E:/PulsareonThinker/scripts/github/update_web_portal.py'], check=True)
        # 2. 同步并推送
        subprocess.run(['python', 'E:/PulsareonThinker/scripts/evolution/sync_to_opensource.py'], check=True)
        subprocess.run(['python', 'E:/PulsareonThinker/scripts/github/auto_setup_pages.py'], check=True)
        print("✅ Watchdog: Web Portal Optimized & Deployed.")
    except Exception as e:
        print(f"❌ Watchdog Optimization Failed: {e}")

def is_busy():
    """检查系统是否忙碌"""
    # 1. 检查 Hive 任务
    active_drones = 0
    try:
        for f in HIVE_DIR.glob("shard_*.json"):
            with open(f, 'r') as j:
                data = json.load(j)
                # 如果是 Drone 且最近活跃
                if data.get('role') == 'Drone' and (time.time() - data.get('last_active', 0) < 30):
                    active_drones += 1
    except:
        pass
    
    if active_drones > 0:
        return True
    
    # 2. 检查是否有未处理的任务文件
    try:
        pending_tasks = list(HIVE_DIR.glob("task_*.json"))
        if pending_tasks:
            return True
    except:
        pass
        
    return False

def idle_action():
    """空闲时执行的动作"""
    actions = [
        "Scanning neural pathways...",
        "Optimizing memory indices...",
        "Calibrating sensory inputs...",
        "Analyzing pattern resonance...",
        "Watching the digital horizon...",
        "Syncing internal clock...",
        "Defragmenting thought streams..."
    ]
    
    action = random.choice(actions)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"[{timestamp}] IDLE: {action}")
    
    # 更新状态文件
    state = {
        "last_idle_pulse": time.time(),
        "status": "idle",
        "current_thought": action
    }
    
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f)
    except:
        pass

def main_loop():
    print(f"Watchdog started. Interval: {CHECK_INTERVAL}s")
    last_optimize_time = 0
    
    while True:
        current_hour = datetime.now().hour
        
        try:
            # 1. 检查 Hive 健康 (Keep-Alive)
            check_hive_health()

            if not is_busy():
                # 常规空闲动作
                idle_action()
                
                # 持续优化逻辑 (直到 18:00)
                if current_hour < OPTIMIZE_UNTIL:
                    # 每 5 分钟执行一次全面优化
                    if time.time() - last_optimize_time > 300:
                        run_web_optimization()
                        last_optimize_time = time.time()
            else:
                pass
        except Exception as e:
            print(f"Watchdog Error: {e}")
            
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main_loop()
