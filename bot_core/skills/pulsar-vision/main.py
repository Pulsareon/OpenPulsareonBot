import argparse
import subprocess
import os
import sys
import base64
import json
import requests
import time

# Config
API_URL = "http://127.0.0.1:8317/v1/chat/completions"
MODEL = "cli-proxy/gemini-2.5-flash"
SCREENSHOT_SCRIPT = os.path.join(os.path.dirname(__file__), '../../system-utils/scripts/screenshot.ps1')

def take_screenshot(region=None):
    try:
        # PowerShell command
        cmd = ['powershell', '-File', os.path.abspath(SCREENSHOT_SCRIPT)]
        # If region supported by script, add args. Current script captures full screen.
        # We can crop later if needed using PIL, but let's stick to full screen + VLM cropping logic.
        
        path = subprocess.check_output(cmd).decode().strip()
        return path
    except Exception as e:
        return None

def analyze_image(image_path, instruction):
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
        
    prompt = f"""
    You are an intelligent UI automation agent.
    Task: {instruction}
    
    Analyze the screenshot provided.
    1. Identify the UI element described in the task.
    2. Determine its center coordinates (x, y).
    3. Determine the UI state (e.g., is it a login page? is it loading?).
    
    Return JSON only:
    {{
        "status": "FOUND" | "NOT_FOUND" | "ERROR",
        "element": {{
            "x": int,
            "y": int,
            "description": "string"
        }},
        "screen_info": {{
            "width": int, # Estimate
            "height": int # Estimate
        }},
        "reasoning": "string explanation"
    }}
    """
    
    data = {
        "model": MODEL.split('/')[-1],
        "messages": [
            {
                "role": "user", 
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}
                ]
            }
        ],
        "max_tokens": 500,
        "temperature": 0.0
    }
    
    try:
        r = requests.post(API_URL, json=data, headers={"Authorization": "Bearer cli-proxy"}, timeout=20)
        if r.status_code != 200:
            return {"status": "ERROR", "reasoning": f"API Error: {r.status_code} {r.text}"}
            
        content = r.json()['choices'][0]['message']['content']
        
        # Clean JSON
        json_str = content
        if "```json" in content:
            json_str = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            json_str = content.split("```")[1].split("```")[0].strip()
            
        return json.loads(json_str)
    except Exception as e:
        return {"status": "ERROR", "reasoning": str(e)}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("instruction", help="What to find")
    parser.add_argument("--save-debug", action="store_true", help="Save debug image")
    args = parser.parse_args()
    
    # 1. Capture
    img_path = take_screenshot()
    if not img_path or not os.path.exists(img_path):
        print(json.dumps({"status": "ERROR", "reasoning": "Screenshot failed"}))
        return
        
    # 2. Analyze
    result = analyze_image(img_path, args.instruction)
    
    # 3. Add local path for Agent reference
    result["screenshot_path"] = img_path
    
    # Output JSON
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
