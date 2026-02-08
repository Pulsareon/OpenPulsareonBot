"""
Trigger Opus Auth
尝试使用全局 Key 调用 Opus，捕获返回的认证链接。
"""

import requests
import json
import sys

# 修复 Windows 编码
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

API_URL = "http://127.0.0.1:8317/v1/chat/completions"
HEADERS = {"Authorization": "Bearer cli-proxy"}
DATA = {
    "model": "claude-opus-4-5-thinking",
    "messages": [{"role": "user", "content": "hi"}],
    "max_tokens": 1
}

def trigger():
    print(f"🚀 Triggering Opus (Global Key)...")
    try:
        r = requests.post(API_URL, json=DATA, headers=HEADERS, timeout=20)
        print(f"Status: {r.status_code}")
        
        try:
            print(json.dumps(r.json(), indent=2))
        except:
            print(r.text)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    trigger()
