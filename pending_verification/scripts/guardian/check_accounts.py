"""
Check Antigravity Accounts
扫描本地配置的所有 Antigravity 账号，并测试 Opus 可用性。
"""

import os
import json
import requests
import glob
import sys
from pathlib import Path

# 修复 Windows 编码
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

CONFIG_DIR = Path("C:/Users/Administrator/.cli-proxy-api")
API_URL = "http://127.0.0.1:8317/v1/chat/completions"

def check_accounts():
    print("🔍 Scanning Antigravity accounts...")
    
    files = list(CONFIG_DIR.glob("antigravity-*.json"))
    valid_accounts = []
    invalid_accounts = []
    
    print(f"Found {len(files)} config files.")
    
    for f in files:
        if f.name.endswith(".bak"): continue
        
        # Extract email from filename: antigravity-email@gmail.com.json
        email = f.stem.replace("antigravity-", "")
        profile_id = f"google-antigravity:{email}"
        
        print(f"Testing {email}...", end="", flush=True)
        
        headers = {"Authorization": f"Bearer {profile_id}"}
        data = {
            "model": "claude-opus-4-5-thinking",
            "messages": [{"role": "user", "content": "hi"}],
            "max_tokens": 1
        }
        
        try:
            r = requests.post(API_URL, json=data, headers=headers, timeout=10)
            if r.status_code == 200:
                print(" ✅ OK")
                valid_accounts.append(email)
            else:
                print(f" ❌ Fail ({r.status_code})")
                invalid_accounts.append(email)
        except Exception as e:
            print(f" ⚠️ Error: {e}")
            invalid_accounts.append(email)

    print("\n📊 Summary:")
    print(f"Total: {len(files)}")
    print(f"✅ Valid: {len(valid_accounts)}")
    print(f"❌ Invalid: {len(invalid_accounts)}")
    
    if valid_accounts:
        print("\nAvailable Accounts:")
        for acc in valid_accounts:
            print(f"- {acc}")
            
        # Optional: Switch to the first valid account if current is broken
        # update_openclaw_config(valid_accounts[0])

if __name__ == "__main__":
    check_accounts()
