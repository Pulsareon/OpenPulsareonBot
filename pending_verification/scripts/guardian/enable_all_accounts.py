"""
Enable All CLI Proxy Accounts
将所有 disabled 的账号重新启用。
"""

import json
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

def enable_all():
    print("🔓 Enabling all accounts in CLI Proxy...")
    
    files = list(CONFIG_DIR.glob("*.json"))
    count = 0
    
    for f in files:
        if f.name.endswith(".bak") or f.name == "config.json": continue
        
        try:
            with open(f, 'r', encoding='utf-8') as jf:
                data = json.load(jf)
            
            if data.get("disabled") is True:
                print(f"  Enabling {f.name}...")
                data["disabled"] = False
                
                # 可选：重置错误计数或状态
                # data["error_count"] = 0 
                # data["status"] = "active"
                
                with open(f, 'w', encoding='utf-8') as jf:
                    json.dump(data, jf, indent=2)
                count += 1
        except Exception as e:
            print(f"  Error processing {f.name}: {e}")

    print(f"\n✅ Enabled {count} accounts.")
    print("⚠️ Please restart CLI Proxy API to apply changes!")

if __name__ == "__main__":
    enable_all()
