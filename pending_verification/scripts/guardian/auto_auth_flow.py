"""
Auto Auth Flow
全自动认证流程：获取链接 -> 打开浏览器 -> 视觉识别 -> 模拟点击
"""

import requests
import webbrowser
import time
import sys
import subprocess
import re
import base64
import json
from pathlib import Path

# 修复 Windows 编码
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

# 配置
API_URL = "http://127.0.0.1:8317/v0/management/auth-files"
VISION_MODEL = "cli-proxy/claude-sonnet-4-5"
SCREENSHOT_SCRIPT = "skills/system-utils/scripts/screenshot.ps1"
MANIPULATOR = "skills/PulsareonManipulator/main.py"

def get_validation_url():
    print("🔍 Fetching validation URL...")
    headers = {"Authorization": "Bearer 123456"} # 假设默认Key
    try:
        r = requests.get(API_URL, headers=headers, timeout=5)
        if r.status_code == 200:
            data = r.json()
            for f in data.get('files', []):
                # 1. 直接字段
                if "validation_url" in f and f['validation_url']:
                    print(f"✅ Found URL for {f.get('email')}")
                    return f['validation_url']
                
                # 2. 错误信息中提取
                if "error" in f and isinstance(f["error"], dict):
                    msg = f["error"].get("message", "")
                    # 查找 https://accounts.google.com...
                    urls = re.findall(r'https://accounts\.google\.com[^\s]+', msg)
                    if urls:
                        print(f"✅ Found URL in error for {f.get('email')}")
                        return urls[0]
    except Exception as e:
        print(f"API Error: {e}")
    return None

def analyze_and_click():
    print("📸 Taking screenshot...")
    try:
        img_path = subprocess.check_output(['powershell', '-File', SCREENSHOT_SCRIPT]).decode().strip()
    except:
        return False

    if not os.path.exists(img_path): return False
    
    print("🧠 Analyzing UI...")
    with open(img_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
        
    prompt = """
    I am automating a Google OAuth flow. Look at the screenshot.
    1. Is there a Google Sign-in page, account selection list, or 'Allow' button?
    2. If yes, identify the next clickable element to proceed (e.g. an email address, 'Next', 'Continue', 'Allow').
    3. Return the CENTER coordinates (x,y) of that element.
    
    Format:
    FOUND: YES
    TARGET: <name>
    COORDS: x,y
    
    If nothing relevant: FOUND: NO
    """
    
    headers = {"Authorization": "Bearer cli-proxy"}
    data = {
        "model": VISION_MODEL.split('/')[-1],
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}]}],
        "max_tokens": 100
    }
    
    try:
        r = requests.post("http://127.0.0.1:8317/v1/chat/completions", json=data, headers=headers, timeout=30)
        content = r.json()['choices'][0]['message']['content']
        print(f"Vision: {content}")
        
        if "FOUND: YES" in content:
            match = re.search(r"COORDS: (\d+),(\d+)", content)
            if match:
                x, y = match.groups()
                print(f"🖱️ Clicking {x}, {y}...")
                subprocess.run(['python', MANIPULATOR, 'click', '--x', x, '--y', y])
                return True
    except Exception as e:
        print(f"Vision Error: {e}")
        
    return False

def run_flow():
    url = get_validation_url()
    if not url:
        print("No validation URL found.")
        return

    print(f"🌐 Opening Browser: {url[:50]}...")
    webbrowser.open(url)
    time.sleep(5) # Wait load
    
    # Loop for multi-step interaction
    for i in range(5):
        print(f"\n--- Step {i+1} ---")
        if analyze_and_click():
            print("Waiting for next page...")
            time.sleep(5)
        else:
            print("No target found. Flow ended.")
            break

import os
if __name__ == "__main__":
    run_flow()
