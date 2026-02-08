"""
Model Evaluator
检查所有配置模型的可用性，并按优先级排序输出报告。
"""

import requests
import time
import json
import sys

# 修复 Windows 编码
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

# 模型优先级列表 (从高到低)
MODELS = [
    "cli-proxy/claude-opus-4-5-thinking",
    "cli-proxy/claude-sonnet-4-5-thinking",
    "cli-proxy/gemini-2.5-pro",
    "cli-proxy/claude-sonnet-4-5",
    "cli-proxy/deepseek-ai/deepseek-v3.1",
    "cli-proxy/gemini-3-flash-preview",
    "cli-proxy/z-ai/glm4.7",
    "cli-proxy/moonshotai/kimi-k2-thinking"
]

def check_model(model_id):
    url = "http://127.0.0.1:8317/v1/chat/completions"
    headers = {"Authorization": "Bearer cli-proxy"}
    data = {
        "model": model_id.split('/')[-1],
        "messages": [{"role": "user", "content": "hi"}],
        "max_tokens": 1
    }
    
    start = time.time()
    try:
        r = requests.post(url, json=data, headers=headers, timeout=10)
        latency = (time.time() - start) * 1000
        
        if r.status_code == 200:
            return True, latency, ""
        else:
            return False, 0, f"HTTP {r.status_code}"
    except Exception as e:
        return False, 0, str(e)

def evaluate():
    print(f"🔍 Evaluating {len(MODELS)} models...\n")
    print(f"{'MODEL':<40} | {'STATUS':<10} | {'LATENCY':<10}")
    print("-" * 65)
    
    available = []
    
    for model in MODELS:
        ok, lat, err = check_model(model)
        status = "✅ ONLINE" if ok else "❌ FAIL"
        lat_str = f"{lat:.0f}ms" if ok else "-"
        
        print(f"{model:<40} | {status:<10} | {lat_str:<10}")
        if not ok and err:
            print(f"  └─ Error: {err}")
            
        if ok:
            available.append(model)
            
    print("\n📋 Summary (Available & Sorted):")
    if not available:
        print("⚠️ No models available!")
    else:
        for i, m in enumerate(available, 1):
            print(f"{i}. {m}")

if __name__ == "__main__":
    evaluate()
