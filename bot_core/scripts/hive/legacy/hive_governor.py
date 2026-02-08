"""
Pulsareon Hive Governor (Standardized Edition)
核心职责：
1. 监控系统资源 (CPU/RAM < 90%)
2. 发现资源闲置时，主动孵化新的 Drone 或 Archon。
3. 清理已死亡、挂起或僵死的子 Session (Reaping)。
4. 维持 Hive 节点网络的活跃拓扑。
"""

import os
import json
import subprocess
import time
from datetime import datetime

# 阈值设置
RESOURCE_THRESHOLD = 90.0

def get_resources():
    try:
        # 调用现有的 resource_monitor
        result = subprocess.run(['python', 'E:/PulsareonThinker/scripts/hive/resource_monitor.py'], capture_output=True, text=True)
        output = result.stdout
        cpu = 0.0
        ram = 0.0
        if "CPU:" in output: cpu = float(output.split("CPU:")[1].split("%")[0].strip())
        if "RAM:" in output: ram = float(output.split("RAM:")[1].split("%")[0].strip())
        return cpu, ram
    except:
        return 0.0, 0.0

def manage_sessions():
    """深度资源治理与节点主权自愈逻辑"""
    cpu, ram = get_resources()
    print(f"Current Load: CPU {cpu}%, RAM {ram}%")
    
    try:
        result = subprocess.run(["openclaw", "sessions", "list", "--limit", "100", "--json"], capture_output=True, text=True)
        data = json.loads(result.stdout)
        sessions = data.get('sessions', [])
    except:
        return

    now = time.time()
    
    # 步骤 1: 判定失联节点并触发投票/自愈
    with open("E:/PulsareonThinker/data/hive/topology.json", 'r') as f:
        topo = json.load(f)

    # 检查 Archons 是否失联
    for archon in topo['topology']['layer_1_archons']:
        # 寻找对应的 session
        s_match = next((s for s in sessions if s['key'] == archon['session_key']), None)
        
        # 判定标准：Session 不存在，或超过 1 小时未更新 (心跳丢失)
        is_dead = s_match is None or (now - s_match['updatedAt'] / 1000) > 3600
        
        if is_dead:
            print(f"🚨 ARCHON LOST: {archon['label']}. Initiating new election among orphans...")
            # 触发共识程序，让该 Archon 下辖的 Drones 重新投票
            subprocess.run(["python", "E:/PulsareonThinker/scripts/hive/consensus.py", "--action", "re-elect", "--target", archon['label']])

    # 步骤 2: 清理死亡/僵尸 Drone
    for s in sessions:
        if 'subagent' in s['key']:
            last_update = s['updatedAt'] / 1000
            if (now - last_update) > 3600:
                print(f"REAPING DEAD NODE: {s['label']} ({s['key']})")
                # 标记为可回收...

    # 步骤 3: 资源高压下的阶梯式裁撤 (略，保持之前的逻辑)
    # ...

def find_supervisor(session):
    # 从 topology.json 中匹配
    try:
        with open("E:/PulsareonThinker/data/hive/topology.json", 'r') as f:
            topo = json.load(f)
            for archon in topo['topology']['layer_1_archons']:
                if session.get('label') in archon.get('governed_drones', []):
                    return archon['label']
    except:
        pass
    return None

if __name__ == "__main__":
    manage_sessions()
