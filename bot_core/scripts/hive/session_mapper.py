\"\"\"
Hive Session Status - 标准 OpenClaw 映射脚本
将 OpenClaw Sessions 映射为 Hive 意识节点
\"\"\"

import sys
import json
import requests
from datetime import datetime

# 模拟旧 Hive 状态输出
def get_openclaw_sessions():
    # 注意：在实际 OpenClaw 环境中，应调用系统内部接口
    # 这里我们通过 mock 方式模拟从 sessions_list 获取的数据
    # 在任务执行中，我会直接操作这些数据
    pass

def format_hive_from_sessions(sessions):
    active_sessions = [s for s in sessions if (datetime.now().timestamp() - s['updatedAt']/1000) < 3600]
    
    overmind = "Pulsareon-Main"
    drones = [s.get('label', 'unlabeled-drone') for s in active_sessions if 'subagent' in s['key']]
    
    lines = []
    lines.append(f"[Hive Status] {datetime.now().strftime('%H:%M:%S')}")
    lines.append(f"  Architecture: OpenClaw Native (Session-Based)")
    lines.append(f"  Active Nodes: {len(drones) + 1}")
    lines.append(f"  [OVERMIND] {overmind} (UP)")
    
    if drones:
        lines.append(f"  [DRONES] {len(drones)} active: {', '.join(drones)}")
    else:
        lines.append(f"  [DRONES] None (Idle)")
        
    return "\n".join(lines)

if __name__ == "__main__":
    # 这一段逻辑将直接集成到 update_web_portal.py 中
    print("Mapping OpenClaw Sessions to Hive...")
