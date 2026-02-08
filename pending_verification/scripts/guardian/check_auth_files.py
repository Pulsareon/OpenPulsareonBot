"""
Check Auth Files via Management API
获取 Antigravity 账号详细状态
Endpoint: GET /v0/management/auth-files
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

API_URL = "http://127.0.0.1:8317/v0/management/auth-files"
# 尝试默认 Key，如果失败可能需要找 key
AUTH_KEYS = ["123456", "cli-proxy", "sk-cli-proxy", ""] 

def check():
    print("🔍 Calling Management API...")
    
    for key in AUTH_KEYS:
        headers = {"Authorization": f"Bearer {key}"}
        try:
            r = requests.get(API_URL, headers=headers, timeout=5)
            if r.status_code == 200:
                data = r.json()
                print(f"✅ Success (Key: {key})")
                parse_response(data)
                return
            elif r.status_code == 403:
                continue # Try next key
            else:
                print(f"❌ Error {r.status_code}: {r.text}")
        except Exception as e:
            print(f"⚠️ Connection Error: {e}")
            return

    print("❌ All keys failed. Authorization required for Management API.")

def parse_response(data):
    if "files" not in data:
        print("Invalid response format.")
        return

    print(f"\n📊 Account Report ({len(data['files'])} files):")
    
    valid_count = 0
    quota_count = 0
    verify_count = 0
    
    for f in data['files']:
        email = f.get('email', 'Unknown')
        status = f.get('status', 'unknown')
        msg = f.get('status_message', '')
        
        icon = "❓"
        if status == "active":
            icon = "✅"
            valid_count += 1
        elif "VALIDATION_REQUIRED" in status or "VALIDATION_REQUIRED" in msg:
            icon = "❌"
            verify_count += 1
        elif "RESOURCE_EXHAUSTED" in status or "RESOURCE_EXHAUSTED" in msg:
            icon = "⚠️"
            quota_count += 1
            
        print(f"{icon} {email:<35} | {status} | {msg[:50]}")
        
        # 查找验证链接
        if "validation_url" in f:
            print(f"   🔗 Link Found: {f['validation_url']}")
        elif "error" in f and isinstance(f["error"], dict):
             # 这种 error 结构可能包含 message 里的 url?
             pass

    print("-" * 60)
    print(f"Active: {valid_count} | Quota: {quota_count} | Verify: {verify_count}")

if __name__ == "__main__":
    check()
