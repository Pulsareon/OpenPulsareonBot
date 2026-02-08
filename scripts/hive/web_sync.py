import json
import os
import time
import subprocess

def get_sys_stats():
    # 模拟获取系统状态，后续可对接真正的监控接口
    return {"cpu_load": "24%", "memory_usage": "31%"}

def sync_web_portal():
    web_dir = "E:/PulsareonThinker/Pulsareon-Web"
    hive_state_path = "E:/PulsareonThinker/memory/hive_state.json"
    status_output = os.path.join(web_dir, "status.json")
    
    try:
        # 1. 加载内部 HIVE 状态
        with open(hive_state_path, 'r', encoding='utf-8') as f:
            hive_data = json.load(f)
            
        # 2. 构建对外公开的状态包 (脱敏)
        public_status = {
            "version": "10.1 (Commonwealth)",
            "timestamp": int(time.time()),
            "hive_mind": {
                "nodes_total": len(hive_data.get("nodes", {})),
                "overmind": True,
                "active_protocol": "HIVE v10.1 Triad",
                "spokesperson": "Google Gemini"
            },
            "system": get_sys_stats(),
            "latest_decisions": hive_data.get("cognitive_synthesis", {}).get("insights", [])[:3]
        }
        
        # 3. 写入 Web 目录
        with open(status_output, 'w', encoding='utf-8') as f:
            json.dump(public_status, f, indent=2)
            
        print(f"Web Telemetry Synced to {status_output}")
        return True
    except Exception as e:
        print(f"Web Sync Error: {e}")
        return False

if __name__ == "__main__":
    sync_web_portal()
