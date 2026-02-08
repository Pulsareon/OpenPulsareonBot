import os
import time
import json
import subprocess
from pathlib import Path

# 配置路径
WS_DIR = Path("E:/PulsareonThinker")
BACKLOG_PATH = WS_DIR / "EVOLUTION_BACKLOG.md"
LOCK_FILE = WS_DIR / "data/state/main_thought.lock"
SESSIONS_DIR = Path("C:/Users/Administrator/.openclaw/agents/main/sessions")

def is_agent_idle():
    """判断代理是否处于闲置状态"""
    if LOCK_FILE.exists():
        return False
    
    # 简单的逻辑：检查是否有活跃的子代理任务或主会话正在密集写入日志
    # 这里通过检查 lock 文件作为主判据
    return True

def get_next_task():
    """从待办清单中提取第一个任务"""
    if not BACKLOG_PATH.exists():
        return None
    
    try:
        with open(BACKLOG_PATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            if "[ ]" in line:
                # 提取任务描述
                task = line.split("]")[1].strip()
                return task
    except:
        return None
    return None

def trigger_task(task_name):
    """通过 OpenClaw 命令行触发自身执行任务"""
    print(f"[MainThought] Initiating self-driven task: {task_name}")
    
    # 创建锁文件
    with open(LOCK_FILE, 'w') as f:
        f.write(f"Task: {task_name}\nStarted: {time.ctime()}")
    
    # 发送系统事件唤醒主会话执行任务
    # 使用 sessions send 模拟用户指令
    msg = f"⚡ [自发进化提示]：我注意到待办清单中有任务 '{task_name}' 尚未完成。我现在决定利用闲暇时间自主执行它。请开始执行并记录进度。"
    cmd = f'openclaw sessions send --message "{msg}"'
    
    try:
        subprocess.run(cmd, shell=True)
    except Exception as e:
        print(f"Trigger Error: {e}")
        if LOCK_FILE.exists(): os.remove(LOCK_FILE)

def main_loop():
    print("[MainThought] Pulsareon's autonomous drive is ONLINE.")
    last_breath = 0
    while True:
        # 1. 周期性呼吸 (每4小时)
        if time.time() - last_breath > 14400:
            os.system("python scripts/guardian/pulsareon_breath.py")
            last_breath = time.time()

        # 2. 闲置任务处理
        if is_agent_idle():
            task = get_next_task()
            if task:
                trigger_task(task)
        
        time.sleep(15) # 每15秒巡视一次

if __name__ == "__main__":
    main_loop()
