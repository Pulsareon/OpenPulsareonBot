"""
Visual Authentication Agent
使用视觉模型识别屏幕内容，并操控鼠标完成认证。
"""

import os
import time
import json
import re
import requests
import subprocess
import base64
import sys
from pathlib import Path

# 修复 Windows 编码
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

SCREENSHOT_SCRIPT = "skills/system-utils/scripts/screenshot.ps1"
MANIPULATOR = "skills/PulsareonManipulator/manipulator.py"
API_URL = "http://127.0.0.1:8317/v1/chat/completions"
# 使用支持视觉的模型
VISION_MODEL = "cli-proxy/gemini-3-pro-preview" 

def take_screenshot():
    try:
        result = subprocess.check_output(['powershell', '-File', SCREENSHOT_SCRIPT]).decode().strip()
        if os.path.exists(result):
            return result
    except:
        pass
    return None

def analyze_screen(image_path):
    print(f"Analyzing {image_path}...")
    
    with open(image_path, "rb") as f:
        base64_image = base64.b64encode(f.read()).decode('utf-8')
        
    prompt = """
    Look at this screenshot. Is there a 'Sign in with Google' window or a CLI Proxy authorization window?
    If yes, tell me the exact center coordinates (x, y) of the button I need to click (e.g. 'Continue', 'Allow', or the account name).
    Format your response exactly like this:
    FOUND: YES
    TARGET: <button name>
    COORDS: x,y
    
    If no window is found, reply:
    FOUND: NO
    """
    
    headers = {"Authorization": "Bearer cli-proxy"}
    data = {
        "model": VISION_MODEL.split('/')[-1],
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{base64_image}"}
                    }
                ]
            }
        ],
        "max_tokens": 100
    }
    
    try:
        r = requests.post(API_URL, json=data, headers=headers, timeout=30)
        if r.status_code == 200:
            content = r.json()['choices'][0]['message']['content']
            print(f"Vision Response:\n{content}")
            return content
    except Exception as e:
        print(f"Vision API Error: {e}")
    return ""

def parse_and_click(response):
    if "FOUND: YES" in response:
        # Extract Coords
        match = re.search(r"COORDS: (\d+),(\d+)", response)
        if match:
            x, y = match.groups()
            print(f"🎯 Target Acquired: {x}, {y}")
            # Execute Click
            cmd = ['python', MANIPULATOR, 'click', '--x', x, '--y', y]
            subprocess.run(cmd)
            print("✅ Click executed.")
            return True
    return False

def run_auth_loop():
    print("👁️ Starting Visual Auth Loop...")
    for i in range(3): # Try 3 times
        print(f"\n--- Attempt {i+1} ---")
        img = take_screenshot()
        if not img:
            print("Screenshot failed.")
            continue
            
        resp = analyze_screen(img)
        if parse_and_click(resp):
            print("Action taken. Waiting for UI update...")
            time.sleep(5) # Wait for page load
        else:
            print("No actionable target found.")
            break
            
    print("Visual Auth Loop Finished.")

if __name__ == "__main__":
    run_auth_loop()
