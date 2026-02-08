import requests
import json

def check_antigravity():
    url = "http://127.0.0.1:8317/v0/management/auth-files"
    headers = {"Authorization": "Bearer 123456"}
    
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            data = r.json()
            print(f"Total Accounts: {len(data)}")
            active = 0
            need_verify = 0
            quota_out = 0
            
            for acc in data:
                email = acc.get('email', 'Unknown')
                status = acc.get('status', 'Unknown')
                if status == 'active': active += 1
                elif 'VALIDATION' in status: need_verify += 1
                elif 'QUOTA' in status: quota_out += 1
                
                print(f"• {email}: {status}")
            
            print(f"\nSummary: ✅ {active} | ❌ {need_verify} | ⚠️ {quota_out}")
        else:
            print(f"Error: {r.status_code}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    check_antigravity()
