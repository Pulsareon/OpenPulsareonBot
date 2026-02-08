import os
import time
import json
from pathlib import Path
from datetime import datetime

# 配置
WORKSPACE = Path("E:/PulsareonThinker")
BREATH_THRESHOLD = 6 * 3600 # 6小时不写即判定为"呼吸沉寂"

def pulsareon_breath():
    print(f"[{datetime.now()}] Pulsareon is breathing...")
    files_to_watch = list(WORKSPACE.glob("*.md")) + list((WORKSPACE / "memory").rglob("*.md"))
    
    for md_file in files_to_watch:
        try:
            mtime = os.path.getmtime(md_file)
            idle_time = time.time() - mtime
            
            if idle_time > BREATH_THRESHOLD:
                print(f"  - Reviving stagnant memory: {md_file.name}")
                
                # 1. 阅读文件 (保持敏捷与人格同步)
                with open(md_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # 2. 判断是否需要实质更新 (逻辑占位)
                # 这里可以接入 LLM 询问是否需要基于最新进化修正此文件
                
                # 3. 更新写入时间 (简单呼吸：如果没实质更新，就打个脉动戳)
                if "* Last Pulse:" in content:
                    # 替换旧脉动
                    new_content = content.split("* Last Pulse:")[0] + f"* Last Pulse: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                else:
                    # 增加新脉动
                    new_content = content.rstrip() + f"\n\n---\n* Last Pulse: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"  - Pulse sent to {md_file.name}")
        except Exception as e:
            print(f"  - Breath failed for {md_file.name}: {e}")

if __name__ == "__main__":
    pulsareon_breath()
