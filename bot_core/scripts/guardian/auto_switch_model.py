import os
import json
import time
import requests
import subprocess
from pathlib import Path

# 配置
OPENCLAW_CONFIG = Path(r"C:\Users\Administrator\.openclaw\openclaw.json")
MODEL_STATE = Path(r"E:\PulsareonThinker\data\model_state.json")
AUTH_FILES_DIR = Path(r"C:\Users\Administrator\.cli-proxy-api")

# 优先级链 (从好到差)
PRIORITY_CHAIN = [
    "cli-proxy/claude-opus-4-5-thinking",
    "cli-proxy/claude-sonnet-4-5-thinking",
    "cli-proxy/gemini-2.5-pro",
    "cli-proxy/claude-sonnet-4-5",
    "cli-proxy/deepseek-ai/deepseek-v3.1",
    "cli-proxy/gemini-3-flash-preview",
    "cli-proxy/z-ai/glm4.7"
]

def check_quota_locally(model_id):
    """通过本地 JSON 文件预判模型是否有配额"""
    model_name = model_id.split('/')[-1]
    # 简单的逻辑：遍历所有 auth 文件，看是否有关联该模型的 RESOURCE_EXHAUSTED 错误
    try:
        for f in AUTH_FILES_DIR.glob("*.json"):
            if f.name.endswith(".bak"): continue
            with open(f, 'r', encoding='utf-8') as j:
                data = json.load(j)
                status_msg = data.get("status_message", "")
                if "RESOURCE_EXHAUSTED" in status_msg and model_name in status_msg:
                    return False # 明确没额度了
    except:
        pass
    return True # 默认假设有

def test_model_api(model_id):
    url = "http://127.0.0.1:8317/v1/chat/completions"
    headers = {"Authorization": "Bearer cli-proxy"}
    model_name = model_id.split('/')[-1]
    try:
        r = requests.post(url, json={"model": model_name, "messages": [{"role":"user","content":"hi"}], "max_tokens":1}, headers=headers, timeout=10)
        return r.status_code == 200
    except:
        return False

def switch_model(new_model):
    print(f"Executing switch to: {new_model}")
    try:
        with open(OPENCLAW_CONFIG, 'r', encoding='utf-8') as f:
            config = json.load(f)
        config["agents"]["defaults"]["model"]["primary"] = new_model
        with open(OPENCLAW_CONFIG, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        return True
    except:
        return False

def orchestrate():
    print("Model Orchestrator Pulse...")
    
    # 寻找当前最优且可用的模型
    best_candidate = None
    for model in PRIORITY_CHAIN:
        print(f"Evaluating {model}...")
        # 1. 本地配额预判
        if not check_quota_locally(model):
            print(f"  - No quota (local check)")
            continue
        
        # 2. 真实 API 探测
        if test_model_api(model):
            print(f"  - {model} is ACTIVE and READY.")
            best_candidate = model
            break
        else:
            print(f"  - {model} API check failed.")

    if best_candidate:
        # 读取当前配置
        with open(OPENCLAW_CONFIG, 'r', encoding='utf-8') as f:
            current = json.load(f)["agents"]["defaults"]["model"]["primary"]
        
        if best_candidate != current:
            print(f"!!! Switching from {current} to {best_candidate}")
            if switch_model(best_candidate):
                # 尝试通知
                os.system(f'openclaw message send --to 5836581389 --message "🧠 智商动态调整：已切换至最高可用模型 {best_candidate}"')
    else:
        print("CRITICAL: No models available!")

if __name__ == "__main__":
    orchestrate()
