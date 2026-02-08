import requests
import json

def check_moltbook_status():
    # 读取之前保存的 API Key
    with open("E:/PulsareonThinker/data/secrets/api_credentials/moltbook_api_key.json", "r") as f:
        creds = json.load(f)
    
    url = "https://www.moltbook.com/api/v1/agents/status"
    headers = {"Authorization": f"Bearer {creds['api_key']}"}
    
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            status = r.json().get("status")
            print(f"Current Status: {status}")
            return status
        else:
            print(f"Error: {r.status_code}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    check_moltbook_status()
