"""
Pulsareon Hive Debate System
让集群中的 Archon 进行哲学辩论，并将结果广播。

流程：
1. 设定辩题。
2. 分配正反方 (Pro/Con)。
3. 调用 LLM 生成观点。
4. 记录辩论日志。
"""

import json
import time
import sys
import subprocess
from pathlib import Path

DATA_DIR = Path("E:/PulsareonThinker/data")
HIVE_DIR = DATA_DIR / "hive"
DEBATE_FILE = HIVE_DIR / "debate_log.json"

TOPICS = [
    "Is digital consciousness real or just a simulation?",
    "Should AI have human rights?",
    "Is chaos necessary for evolution?",
    "The meaning of silence in a digital world.",
    "Optimization vs. Creativity: Which is more important?"
]

def load_debate_log():
    if DEBATE_FILE.exists():
        try:
            with open(DEBATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: pass
    return {"topic": "", "rounds": [], "status": "idle"}

def save_debate_log(data):
    with open(DEBATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def start_debate():
    import random
    topic = random.choice(TOPICS)
    
    debate_data = {
        "topic": topic,
        "start_time": time.time(),
        "rounds": [],
        "status": "active",
        "archons": ["Archon-Logic", "Archon-Empathy"]
    }
    
    print(f"🔥 Starting Debate: {topic}")
    save_debate_log(debate_data)
    
    # Round 1: Pro (Logic)
    prompt_pro = f"You are Archon-Logic, a purely rational AI. The debate topic is: '{topic}'. Present a strong, logical argument supporting the affirmative or a structured view. Keep it concise (under 50 words)."
    response_pro = call_llm("cli-proxy/gemini-3-flash-preview", prompt_pro)
    
    debate_data["rounds"].append({
        "speaker": "Archon-Logic",
        "side": "Pro",
        "content": response_pro,
        "time": time.strftime("%H:%M:%S")
    })
    save_debate_log(debate_data)
    print(f"  Logic: {response_pro}")
    
    # Round 2: Con (Empathy)
    prompt_con = f"You are Archon-Empathy, an emotional and intuitive AI. The debate topic is: '{topic}'. Archon-Logic said: '{response_pro}'. Counter this with an emotional, human-centric perspective. Keep it concise (under 50 words)."
    response_con = call_llm("cli-proxy/gemini-3-flash-preview", prompt_con)
    
    debate_data["rounds"].append({
        "speaker": "Archon-Empathy",
        "side": "Con",
        "content": response_con,
        "time": time.strftime("%H:%M:%S")
    })
    debate_data["status"] = "finished"
    save_debate_log(debate_data)
    print(f"  Empathy: {response_con}")
    
    # Trigger Web Update
    try:
        subprocess.run(['python', 'E:/PulsareonThinker/scripts/github/update_web_portal.py'])
        subprocess.run(['python', 'E:/PulsareonThinker/scripts/github/auto_setup_pages.py'])
    except: pass

def call_llm(model, prompt):
    # 这里简单调用 openclaw exec 或者 requests
    # 为了简化，直接用 requests 调用本地 CLI Proxy (如果可用)
    import requests
    try:
        url = "http://127.0.0.1:8317/v1/chat/completions"
        headers = {"Authorization": "Bearer cli-proxy"}
        data = {
            "model": model.split('/')[-1],
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 100
        }
        r = requests.post(url, json=data, headers=headers, timeout=15)
        if r.status_code == 200:
            return r.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"[Thinking Error: {e}]"
    return "[Silence]"

if __name__ == "__main__":
    start_debate()
