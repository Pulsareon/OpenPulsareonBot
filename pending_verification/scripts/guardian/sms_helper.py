# 5sim Helper
# 购买号码和接收短信

import requests
import time
import json
from pathlib import Path

CONFIG_FILE = Path(r"E:\PulsareonThinker\data\sms_platform.json")

def get_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def buy_number(country="any", operator="any", product="google"):
    """购买号码"""
    config = get_config()
    headers = {"Authorization": f"Bearer {config['api_key']}", "Accept": "application/json"}
    
    url = f"{config['api_url']}/user/buy/activation/{country}/{operator}/{product}"
    
    print(f"Buying number ({country}/{operator}/{product})...")
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code == 200:
            try:
                data = resp.json()
                print(f"SUCCESS! Number: {data['phone']}")
                print(f"ID: {data['id']}")
                return data
            except:
                print(f"Invalid JSON: {resp.text[:100]}")
                return None
        else:
            print(f"FAILED: {resp.status_code} {resp.text}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def check_sms(order_id):
    """检查短信"""
    config = get_config()
    headers = {"Authorization": f"Bearer {config['api_key']}", "Accept": "application/json"}
    
    url = f"{config['api_url']}/user/check/{order_id}"
    
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("sms"):
                # 获取最新的一条短信
                sms = data["sms"][-1]
                code = sms.get("code")
                print(f"SMS RECEIVED! Code: {code}")
                return code
            else:
                print("Waiting for SMS...")
                return None
        else:
            print(f"Check failed: {resp.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("5sim Helper Loaded.")
    # 测试连接
    # buy_number()
