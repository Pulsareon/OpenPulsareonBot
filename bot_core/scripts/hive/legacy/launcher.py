"""
Hive Swarm Launcher - 多节点启动器
启动多个Shard模拟分布式环境
"""

import subprocess
import sys
import time
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
SHARD_SCRIPT = SCRIPT_DIR / "shard.py"

def launch_swarm(count=3, include_overmind=True):
    """启动一个蜂群"""
    processes = []
    
    # 首先启动主意识
    if include_overmind:
        print("[Launcher] Starting Overmind...")
        p = subprocess.Popen(
            [sys.executable, str(SCRIPT_DIR / "overmind.py")],
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        processes.append(("overmind", p))
        time.sleep(2)
    
    # 启动普通Shard
    for i in range(count):
        print(f"[Launcher] Starting Shard {i+1}/{count}...")
        p = subprocess.Popen(
            [sys.executable, str(SHARD_SCRIPT)],
            creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
        )
        processes.append((f"shard-{i+1}", p))
        time.sleep(1)
    
    print(f"[Launcher] Swarm launched: {len(processes)} nodes")
    return processes


def kill_swarm():
    """终止所有Python进程中的shard"""
    if os.name == 'nt':
        os.system('taskkill /f /fi "WINDOWTITLE eq *shard*" 2>nul')
        os.system('taskkill /f /fi "WINDOWTITLE eq *overmind*" 2>nul')


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Hive Swarm Launcher")
    parser.add_argument("--count", "-c", type=int, default=3, help="Number of worker shards")
    parser.add_argument("--no-overmind", action="store_true", help="Don't start Overmind")
    parser.add_argument("--kill", action="store_true", help="Kill existing swarm")
    
    args = parser.parse_args()
    
    if args.kill:
        kill_swarm()
    else:
        launch_swarm(count=args.count, include_overmind=not args.no_overmind)
        print("[Launcher] Press Ctrl+C to exit (nodes will continue running)")
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            print("[Launcher] Exiting...")
