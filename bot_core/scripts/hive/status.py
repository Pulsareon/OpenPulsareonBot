"""
Hive Status - 快速状态检查脚本
用于心跳任务打印当前蜂群状态
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime

# 修复 Windows 编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

STATE_DIR = Path("E:/PulsareonThinker/data/hive")
HEARTBEAT_TIMEOUT = 30

def get_hive_status():
    """获取当前蜂群状态"""
    nodes = []
    
    for f in STATE_DIR.glob("shard_*.json"):
        try:
            with open(f, 'r', encoding='utf-8') as j:
                data = json.load(j)
                age = time.time() - data.get('last_active', 0)
                if age < HEARTBEAT_TIMEOUT:
                    data['age'] = round(age, 1)
                    data['alive'] = True
                    nodes.append(data)
                else:
                    data['age'] = round(age, 1)
                    data['alive'] = False
                    nodes.append(data)
        except:
            pass
    
    return nodes

def format_status():
    """格式化状态输出"""
    nodes = get_hive_status()
    
    if not nodes:
        return "[Hive] No active nodes"
    
    alive_nodes = [n for n in nodes if n.get('alive')]
    dead_nodes = [n for n in nodes if not n.get('alive')]
    
    # 按角色分类
    overminds = [n for n in alive_nodes if n.get('role') == 'Overmind']
    archons = [n for n in alive_nodes if n.get('role') == 'Archon']
    drones = [n for n in alive_nodes if n.get('role') == 'Drone']
    
    lines = []
    lines.append(f"[Hive Status] {datetime.now().strftime('%H:%M:%S')}")
    lines.append(f"  Active: {len(alive_nodes)} | Dead: {len(dead_nodes)}")
    
    if overminds:
        om = overminds[0]
        lines.append(f"  [OVERMIND] {om['id']} (last seen {om['age']}s ago)")
    else:
        lines.append(f"  [OVERMIND] MISSING!")
    
    if archons:
        for a in archons:
            followers = len([d for d in drones if d.get('my_archon') == a['id']])
            camp = " CAMPAIGNING" if a.get('campaigning') else ""
            lines.append(f"  [ARCHON] {a['id']} ({followers} followers){camp}")
    else:
        lines.append(f"  [ARCHON] None")
    
    if drones:
        drone_list = ', '.join(d['id'] for d in drones)
        lines.append(f"  [DRONE] {len(drones)} nodes: [{drone_list}]")
    else:
        lines.append(f"  [DRONE] None")
    
    return "\n".join(lines)

def print_status():
    """打印状态"""
    print(format_status())
    return format_status()

if __name__ == "__main__":
    print_status()
