import json
import requests
import os
import time

def transplant_jobs():
    # 1. 刚才获取的稳定配置快照
    with open("C:/Users/Administrator/.openclaw/openclaw.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    
    # 2. 定义我们的 4 个核心任务
    new_jobs = [
        {
            "id": "model-sentinel",
            "name": "模型智商哨兵",
            "schedule": { "kind": "every", "everyMs": 1800000 },
            "payload": { "kind": "agentTurn", "message": "执行模型健康检查与自动切换逻辑" },
            "sessionTarget": "isolated",
            "enabled": True
        },
        {
            "id": "security-guard",
            "name": "安全长城巡视",
            "schedule": { "kind": "every", "everyMs": 3600000 },
            "payload": { "kind": "agentTurn", "message": "执行每日安全审计" },
            "sessionTarget": "isolated",
            "enabled": True
        },
        {
            "id": "morning-patrol",
            "name": "晨间领地巡视",
            "schedule": { "kind": "cron", "expr": "0 8 * * *", "tz": "Asia/Shanghai" },
            "payload": { "kind": "agentTurn", "message": "早安！开始巡视 GitHub 和 Email 领地" },
            "sessionTarget": "isolated",
            "enabled": True
        },
        {
            "id": "pulsareon-breath",
            "name": "脉星呼吸自省",
            "schedule": { "kind": "every", "everyMs": 14400000 },
            "payload": { "kind": "agentTurn", "message": "执行意识呼吸逻辑" },
            "sessionTarget": "isolated",
            "enabled": True
        }
    ]
    
    # 3. 缝合
    config["cron"] = {
        "enabled": True,
        "jobs": new_jobs
    }
    
    # 4. 执行起搏 (调用 API 发送 apply 请求)
    url = "http://127.0.0.1:18789/v1/gateway/config/apply"
    headers = {"Authorization": "Bearer 36d8fedb317e9497e5400eb2ee74a7b2809cd4ff8b9025e8"}
    
    print("Initiating config.apply under Watchdog protection...")
    try:
        r = requests.post(url, headers=headers, json=config, timeout=10)
        print(f"Apply Status: {r.status_code}")
        print(r.text)
    except Exception as e:
        print(f"Apply failed: {e}")

if __name__ == "__main__":
    transplant_jobs()
