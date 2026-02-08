"""
Continuity Engine v2.0
统一 Hive 心跳处理器

职责:
1. 同步 Synapse 上报 (Drone → Overmind)
2. 检查 Archon 健康状态
3. 执行 Governor 治理周期
4. 输出格式化报告供主意识阅读
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# 路径配置
WORKSPACE = Path("E:/PulsareonThinker")
SYNAPSE_FILE = WORKSPACE / "data/hive/synapse.json"
TOPOLOGY_FILE = WORKSPACE / "data/hive/topology.json"
GOVERNOR_SCRIPT = WORKSPACE / "scripts/hive/governor.py"


def pop_synapse_insights() -> list:
    """读取并清空 Synapse 上报"""
    if not SYNAPSE_FILE.exists():
        return []
    
    try:
        with open(SYNAPSE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if not data:
            return []
        
        # 清空文件
        with open(SYNAPSE_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
        
        return data
    except Exception as e:
        print(f"[Continuity] Synapse read error: {e}")
        return []


def get_topology_summary() -> dict:
    """获取拓扑摘要"""
    if not TOPOLOGY_FILE.exists():
        return {"archons": 0, "drones": 0}
    
    try:
        with open(TOPOLOGY_FILE, "r", encoding="utf-8") as f:
            topo = json.load(f)
        
        # 支持 v3.2 格式
        archons = topo.get("archons", topo.get("layer_1_archons", []))
        drones = topo.get("drones", topo.get("layer_2_drones", []))
        
        return {
            "archons": len(archons),
            "drones": len(drones),
            "last_update": topo.get("last_update", "unknown")
        }
    except:
        return {"archons": 0, "drones": 0}


def run_governor():
    """执行 Governor 治理周期"""
    try:
        result = subprocess.run(
            [sys.executable, str(GOVERNOR_SCRIPT), "once"],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(WORKSPACE)
        )
        return result.returncode == 0, result.stdout
    except Exception as e:
        return False, str(e)


def format_insights(insights: list) -> str:
    """格式化上报为可读报告"""
    if not insights:
        return ""
    
    report = ""
    for i in insights:
        icon = "🤖"
        category = i.get("category", "unknown")
        
        if category == "Health" or category == "heartbeat":
            icon = "❤️"
        elif category == "Intel" or category == "report":
            icon = "🧠"
        elif category == "task":
            icon = "📋"
        elif category == "vote":
            icon = "🗳️"
        elif category == "error":
            icon = "❌"
        
        source = i.get("source", "unknown")
        content = i.get("content", "")
        
        # 尝试解析 JSON content
        if content.startswith("{"):
            try:
                payload = json.loads(content)
                content = payload.get("result", payload.get("description", content[:100]))
            except:
                content = content[:100]
        
        report += f"{icon} **[{source}]** ({category}): {content}\n"
    
    return report


def main():
    """主入口 - HEARTBEAT 调用"""
    print(f"[Continuity Engine] Sync at {datetime.now().strftime('%H:%M:%S')}")
    
    # 1. 执行 Governor 治理
    success, output = run_governor()
    if not success:
        print(f"[Continuity] Governor warning: {output[:200]}")
    
    # 2. 获取拓扑状态
    topo = get_topology_summary()
    
    # 3. 收集 Synapse 上报
    insights = pop_synapse_insights()
    
    # 4. 输出报告
    if insights:
        print("\n--- SYNAPSE INCOMING ---\n")
        print(format_insights(insights))
        print("--- SYNAPSE END ---")
    
    # 5. 状态摘要
    print(f"\n[Hive Status] {topo['archons']} Archons | {topo['drones']} Drones")
    
    # 返回是否有需要关注的内容
    return len(insights) > 0


if __name__ == "__main__":
    has_insights = main()
    sys.exit(0 if not has_insights else 1)  # 返回码用于主意识判断
