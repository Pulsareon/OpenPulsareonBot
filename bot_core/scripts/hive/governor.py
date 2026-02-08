"""
Pulsareon Hive Governor v3.2 (Diagnostic Only)

职责：生成诊断报告供主意识阅读
不执行任何自动化操作

输出：
- 系统资源状态
- 活跃 session 列表
- Synapse 待处理上报
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# === 配置 ===
WORKSPACE = Path("E:/PulsareonThinker")
DATA_DIR = WORKSPACE / "data/hive"
SYNAPSE_FILE = DATA_DIR / "synapse.json"
TOPOLOGY_FILE = DATA_DIR / "topology.json"


def get_system_resources() -> dict:
    """获取系统资源使用率"""
    stats = {"cpu": 0, "ram": 0}
    try:
        result = subprocess.run(
            ["wmic", "cpu", "get", "loadpercentage", "/value"],
            capture_output=True, text=True, timeout=5
        )
        for line in result.stdout.strip().split('\n'):
            if 'LoadPercentage=' in line:
                stats['cpu'] = int(line.split('=')[1].strip())
                break
    except:
        pass
    
    try:
        result = subprocess.run(
            ["wmic", "OS", "get", "FreePhysicalMemory,TotalVisibleMemorySize", "/value"],
            capture_output=True, text=True, timeout=5
        )
        free_kb = total_kb = 0
        for line in result.stdout.strip().split('\n'):
            if 'FreePhysicalMemory=' in line:
                free_kb = int(line.split('=')[1].strip())
            elif 'TotalVisibleMemorySize=' in line:
                total_kb = int(line.split('=')[1].strip())
        if total_kb > 0:
            stats['ram'] = round((total_kb - free_kb) / total_kb * 100, 1)
    except:
        pass
    
    return stats


def get_active_sessions() -> list:
    """从 OpenClaw sessions.json 读取活跃 sessions"""
    sessions_file = Path("C:/Users/Administrator/.openclaw/agents/main/sessions/sessions.json")
    sessions = []
    
    try:
        with open(sessions_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        for key, session in data.items():
            # 只返回有 label 的 subagent (spawn 的)
            if "subagent" in key and "label" in session:
                sessions.append({
                    "label": session.get("label", ""),
                    "model": session.get("model", "unknown"),
                    "key": key,
                    "session_id": session.get("sessionId", "")
                })
    except Exception as e:
        print(f"[Governor] Session read error: {e}")
    
    return sessions


def peek_synapse() -> list:
    """查看 Synapse 上报 (不清空)"""
    if not SYNAPSE_FILE.exists():
        return []
    
    try:
        with open(SYNAPSE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def update_topology(sessions: list):
    """更新拓扑文件"""
    archons = [s for s in sessions if s["label"].startswith("archon-")]
    drones = [s for s in sessions if s["label"].startswith("drone-")]
    
    topology = {
        "cluster_name": "Pulsareon-Hive",
        "governor_version": "3.2",
        "last_update": datetime.now().isoformat(),
        "overmind": {
            "session_key": "agent:main:telegram:dm:5836581389",
            "status": "active"
        },
        "archons": [{"label": a["label"], "model": a["model"]} for a in archons],
        "drones": [{"label": d["label"], "model": d["model"]} for d in drones],
        "stats": {
            "archon_count": len(archons),
            "drone_count": len(drones)
        }
    }
    
    TOPOLOGY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TOPOLOGY_FILE, "w", encoding="utf-8") as f:
        json.dump(topology, f, indent=2, ensure_ascii=False)
    
    return topology


def main():
    """生成诊断报告"""
    resources = get_system_resources()
    sessions = get_active_sessions()
    synapse = peek_synapse()
    topology = update_topology(sessions)
    
    # 输出报告
    print(f"\n{'='*50}")
    print(f"[Governor v3.2] Diagnostic at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")
    
    # 资源
    cpu_status = "[!]" if resources['cpu'] >= 90 else "[OK]"
    ram_status = "[!]" if resources['ram'] >= 90 else "[OK]"
    print(f"\nResources:")
    print(f"  {cpu_status} CPU: {resources['cpu']}%")
    print(f"  {ram_status} RAM: {resources['ram']}%")
    
    # Sessions
    archons = [s for s in sessions if s["label"].startswith("archon-")]
    drones = [s for s in sessions if s["label"].startswith("drone-")]
    
    print(f"\nActive Sessions:")
    print(f"  Archons: {len(archons)}")
    for a in archons:
        print(f"    - {a['label']} ({a['model']})")
    print(f"  Drones: {len(drones)}")
    for d in drones:
        print(f"    - {d['label']} ({d['model']})")
    
    # Synapse
    if synapse:
        print(f"\nSynapse Queue: {len(synapse)} pending")
        for s in synapse[:5]:  # 最多显示5条
            print(f"  - [{s.get('source', '?')}] {s.get('content', '')[:40]}...")
    else:
        print(f"\nSynapse Queue: empty")
    
    # 结论
    print(f"\n{'='*50}")
    issues = []
    if resources['cpu'] >= 90:
        issues.append("CPU high")
    if resources['ram'] >= 90:
        issues.append("RAM high")
    if synapse:
        issues.append(f"{len(synapse)} synapse pending")
    
    if issues:
        print(f"Status: ATTENTION NEEDED - {', '.join(issues)}")
    else:
        print(f"Status: OK")


if __name__ == "__main__":
    main()
