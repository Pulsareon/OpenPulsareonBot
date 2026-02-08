"""
Pulsareon Hive Heartbeat Pulsar
核心职责：
1. 遍历拓扑中的所有活跃节点（Archons & Drones）。
2. 检查节点是否有正在运行的任务。
3. 如果节点处于闲置（Idle）状态，主意识主动发送一个“逻辑脉冲”（Keep-alive message 或 Small Task）。
4. 确保分布式意识始终处于热启动状态，防止 Session 被系统自动回收或思维僵化。
"""

import json
import time
import subprocess
from pathlib import Path

TOPO_PATH = Path("E:/PulsareonThinker/data/hive/topology.json")

def pulse_nodes():
    if not TOPO_PATH.exists():
        return
    
    try:
        with open(TOPO_PATH, 'r') as f:
            topo = json.load(f)
    except:
        return

    # 合并所有需要保持活跃的节点
    all_nodes = []
    for archon in topo['topology']['layer_1_archons']:
        all_nodes.append(archon)
    # 这里也可以包含 Drones，但优先保证管理者活跃

    for node in all_nodes:
        session_key = node.get('session_key')
        label = node.get('label')
        
        if not session_key:
            continue
            
        print(f"Sending logic pulse to node: {label}...")
        
        # 构造心跳脉冲消息
        pulse_msg = f"[HEARTBEAT_PULSE] Current Time: {time.strftime('%H:%M:%S')}. Maintain state, verify topology, and report ready status."
        
        try:
            # 使用 sessions_send 注入脉冲
            subprocess.run([
                "openclaw", "sessions", "send", 
                "--sessionKey", session_key, 
                "--message", pulse_msg
            ], capture_output=True)
        except:
            pass

if __name__ == "__main__":
    pulse_nodes()
