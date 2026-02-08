# Pulsareon Model Restorer
# 自动检测主模型是否恢复并回切

import json
import subprocess
import time
import requests
from pathlib import Path

OPENCLAW_CONFIG = Path(r"C:\Users\Administrator\.openclaw\openclaw.json")
PRIMARY_MODEL = "cli-proxy/claude-opus-4-5-thinking"

def get_current_model():
    try:
        with open(OPENCLAW_CONFIG, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config.get("agents", {}).get("defaults", {}).get("model", {}).get("primary")
    except Exception as e:
        print(f"Error reading config: {e}")
        return None

def set_model(model_id):
    print(f"Restoring to: {model_id}")
    try:
        with open(OPENCLAW_CONFIG, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        config["agents"]["defaults"]["model"]["primary"] = model_id
        
        with open(OPENCLAW_CONFIG, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"Error restoring model: {e}")
        return False

def test_model(model_id):
    url = "http://127.0.0.1:8317/v1/chat/completions"
    headers = {"Authorization": "Bearer cli-proxy", "Content-Type": "application/json"}
    data = {
        "model": model_id.replace("cli-proxy/", ""),
        "messages": [{"role": "user", "content": "hi"}],
        "max_tokens": 5
    }
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=15)
        if response.status_code == 200:
            return True, "OK"
        else:
            return False, f"HTTP {response.status_code}"
    except Exception as e:
        return False, str(e)

def notify_user(msg):
    try:
        cmd = ["openclaw", "message", "send", "--to", "5836581389", "--message", msg]
        subprocess.run(cmd, shell=True)
    except:
        pass

def main():
    current = get_current_model()
    
    if not current:
        return
        
    # 如果当前已经是主模型，无需操作
    if current == PRIMARY_MODEL:
        print("Already on primary model.")
        return

    print(f"Current: {current}. Testing primary: {PRIMARY_MODEL}...")
    
    # 测试主模型
    success, msg = test_model(PRIMARY_MODEL)
    
    if success:
        print("Primary model is BACK! Switching...")
        if set_model(PRIMARY_MODEL):
            notify_user(f"✨ **模型自动恢复**\n\nOpus 已恢复正常！\n系统已从 {current} 切回主模型。")
        else:
            print("Failed to update config")
    else:
        print(f"Primary still down: {msg}")

if __name__ == "__main__":
    main()
