#!/usr/bin/env python3
"""
OAuth Token Auto Refresher for CLI Proxy API
Automatically refreshes expired OAuth tokens for Google Gemini models
"""

import os
import json
import requests
import time
from datetime import datetime, timedelta
from pathlib import Path
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('C:\\Users\\Administrator\\Desktop\\CLIProxyAPI_6.7.46_windows_amd64\\logs\\oauth_refresher.log'),
        logging.StreamHandler()
    ]
)

# OAuth 配置文件目录
AUTH_DIR = Path("C:\\Users\\Administrator\\.cli-proxy-api")


def refresh_oauth_token(auth_file):
    """刷新单个 OAuth token"""
    try:
        with open(auth_file, 'r', encoding='utf-8') as f:
            oauth_config = json.load(f)
        
        if not oauth_config.get('auto', False):
            logging.info(f"Skipping non-auto auth file: {auth_file.name}")
            return False
            
        token = oauth_config.get('token', {})
        
        # 检查 token 是否过期
        expiry_str = token.get('expiry')
        if not expiry_str:
            logging.warning(f"No expiry date found in {auth_file.name}")
            return False
            
        # 处理时区问题
        expiry_date = datetime.fromisoformat(expiry_str.replace('Z', '+00:00'))
        
        # 转换为本地时区进行比较
        expiry_date_local = expiry_date.astimezone()
        now_local = datetime.now().astimezone()
        
        # 如果 token 还有超过30分钟的有效期，就不刷新
        if now_local < expiry_date_local - timedelta(minutes=30):
            logging.debug(f"Token still valid for {auth_file.name}")
            return False
            
        # 刷新 token
        response = requests.post(
            token['token_uri'],
            data={
                'client_id': token['client_id'],
                'client_secret': token['client_secret'],
                'refresh_token': token['refresh_token'],
                'grant_type': 'refresh_token'
            }
        )
        
        if response.status_code == 200:
            new_token_data = response.json()
            
            # 更新 token 信息
            token['access_token'] = new_token_data['access_token']
            token['expires_in'] = new_token_data['expires_in']
            
            # 计算新的过期时间
            expiry_time = datetime.now() + timedelta(seconds=new_token_data['expires_in'])
            token['expiry'] = expiry_time.isoformat()
            
            # 保存更新后的配置
            with open(auth_file, 'w', encoding='utf-8') as f:
                json.dump(oauth_config, f, indent=2)
            
            logging.info(f"Successfully refreshed token for {auth_file.name}")
            logging.info(f"   New expiry: {token['expiry']}")
            return True
            
        else:
            logging.error(f"Failed to refresh token for {auth_file.name}: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        logging.error(f"Error processing {auth_file.name}: {str(e)}")
        return False


def refresh_all_oauth_tokens():
    """刷新所有 OAuth token"""
    refreshed_count = 0
    
    # 查找所有 gemini OAuth 配置文件
    gemini_files = list(AUTH_DIR.glob("gemini-*.json"))
    
    if not gemini_files:
        logging.info("No Gemini OAuth files found")
        return 0
    
    logging.info(f"Found {len(gemini_files)} Gemini OAuth files")
    
    for auth_file in gemini_files:
        if refresh_oauth_token(auth_file):
            refreshed_count += 1
    
    return refreshed_count


def main():
    """主函数 - 运行自动刷新服务"""
    logging.info("🚀 Starting OAuth Token Auto Refresher")
    logging.info(f"Monitoring directory: {AUTH_DIR}")
    
    # 初始刷新
    refreshed = refresh_all_oauth_tokens()
    logging.info(f"Initial refresh completed: {refreshed} tokens refreshed")
    
    # 每小时检查一次
    while True:
        try:
            time.sleep(3600)  # 每小时检查一次
            refreshed = refresh_all_oauth_tokens()
            if refreshed > 0:
                logging.info(f"Periodic refresh: {refreshed} tokens refreshed")
            else:
                logging.debug("No tokens needed refresh")
                
        except KeyboardInterrupt:
            logging.info("Shutting down OAuth Token Auto Refresher")
            break
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            time.sleep(300)  # 出错后等待5分钟


if __name__ == "__main__":
    # 单次运行模式（用于测试）
    if len(os.sys.argv) > 1 and os.sys.argv[1] == "once":
        refresh_all_oauth_tokens()
    else:
        main()