# Capture Verification URL
# 诱捕 Google 账号验证链接

import requests
import json
import re

MODELS = [
    "cli-proxy/claude-opus-4-5-thinking",
    "cli-proxy/claude-sonnet-4-5"
]

def capture_url():
    url = "http://127.0.0.1:8317/v1/chat/completions"
    headers = {"Authorization": "Bearer cli-proxy", "Content-Type": "application/json"}
    
    for model in MODELS:
        print(f"Testing {model}...")
        data = {
            "model": model.replace("cli-proxy/", ""),
            "messages": [{"role": "user", "content": "hi"}],
            "max_tokens": 10
        }
        
        try:
            response = requests.post(url, json=data, headers=headers, timeout=30)
            if response.status_code == 403:
                print("Captured 403 response!")
                text = response.text
                # 提取 URL
                urls = re.findall(r'(https?://accounts\.google\.com[^\s"]+)', text)
                if urls:
                    print(f"FOUND VERIFICATION URL:\n{urls[0]}")
                    return urls[0]
                else:
                    print("No URL found in 403 response")
                    print(text[:200])
            elif response.status_code == 200:
                print("Model is working (no verification needed)")
            else:
                print(f"Other error: {response.status_code}")
        except Exception as e:
            print(f"Request failed: {e}")
            
    return None

if __name__ == "__main__":
    capture_url()
