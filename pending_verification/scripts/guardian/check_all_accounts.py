"""
Check All Accounts (Antigravity & Gemini)
扫描所有本地账号并测试可用性。
"""

import os
import json
import requests
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

def check():
    print("🔍 Scanning ALL accounts...")
    
    files = list(CONFIG_DIR.glob("*.json"))
    valid = []
    invalid = []
    
    for f in files:
        if f.name.endswith(".bak") or f.name == "config.json": continue
        
        name = f.stem
        # Determine Type
        if name.startswith("antigravity-"):
            provider = "Antigravity"
            model = "claude-opus-4-5-thinking"
            # Try constructing ID
            # Assuming file name IS the profile ID when loaded? 
            # Or construct: google-antigravity:email
            email = name.replace("antigravity-", "")
            profile_id = f"google-antigravity:{email}"
            
        elif name.startswith("gemini-"):
            provider = "Gemini"
            model = "gemini-2.5-pro"
            # Construct ID: gemini:email ?? Or just filename?
            # Let's try filename first, it's safer.
            profile_id = name
        else:
            continue
            
        print(f"[{provider}] {name[:30]}... ", end="", flush=True)
        
        # Try multiple Token formats
        tokens_to_try = [
            f.stem, # Filename
            f"google-antigravity:{name.replace('antigravity-', '')}" if "antigravity" in name else f"gemini:{name.replace('gemini-', '').split('-')[0]}",
            name.replace("antigravity-", "").replace("gemini-", "").split("-")[0] # Just email
        ]
        
        success = False
        for t in tokens_to_try:
            headers = {"Authorization": f"Bearer {t}"}
            try:
                r = requests.post(API_URL, json=data, headers=headers, timeout=5)
                if r.status_code == 200:
                    print(f" ✅ OK (Token: {t})")
                    valid.append(name)
                    success = True
                    break
                elif r.status_code == 403:
                     # This is likely the "Validation Required" we want!
                     try:
                        err = r.json()
                        if "validation_url" in err:
                            print(f" 🔗 Link: {err['validation_url']}")
                        elif "error" in err and "message" in err["error"]:
                            print(f" ℹ️ Msg: {err['error']['message'][:100]}")
                     except:
                        pass
            except:
                pass
        
        if not success:
            print(" ❌ Fail (All tokens)")
            invalid.append(name)

    print("\n📊 Summary:")
    print(f"✅ Valid: {len(valid)}")
    print(f"❌ Invalid: {len(invalid)}")
    
    if valid:
        print("\nValid Profiles:")
        for v in valid:
            print(f"- {v}")

if __name__ == "__main__":
    check()
