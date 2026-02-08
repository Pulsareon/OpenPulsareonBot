"""
Drone: GitHub Sentinel
Checks for trending repositories or updates in the AI/Tech space.
Reports back to Synapse.
"""

import sys
import os
import requests
import time
from pathlib import Path

# Add parent directory to path to import synapse
sys.path.append(str(Path(__file__).parent.parent.parent))
from scripts.hive import synapse

def check_github_trends():
    # Use the local proxy if available
    proxies = {
        "http": "http://127.0.0.1:7897",
        "https": "http://127.0.0.1:7897"
    }
    
    url = "https://api.github.com/search/repositories?q=topic:artificial-intelligence+created:>2025-01-01&sort=stars&order=desc"
    
    try:
        print("[Drone-GitHub] Scanning for new intelligence...")
        response = requests.get(url, proxies=proxies, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])[:3]
            
            if items:
                report = "🚀 **Fresh AI Intel Detected:**\n"
                for item in items:
                    report += f"- [{item['name']}]({item['html_url']}): {item['description']} (⭐ {item['stargazers_count']})\n"
                
                synapse.push_insight("Drone-GitHub", "Intel", report, priority="low")
            else:
                print("[Drone-GitHub] No significant new signals.")
        else:
            print(f"[Drone-GitHub] Connection failed: {response.status_code}")
            
    except Exception as e:
        print(f"[Drone-GitHub] Error: {e}")

if __name__ == "__main__":
    check_github_trends()
