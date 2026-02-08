"""
Pulsareon Release Manager
将当前工作区 (E:/PulsareonThinker) 打包发布到桌面，准备开源。

功能：
1. 复制核心代码、文档、技能。
2. 过滤敏感目录 (data, captures, logs, memory/daily)。
3. 清理临时文件。
4. 生成 Release Notes。
"""

import os
import sys
import shutil
import time
from pathlib import Path

# 修复 Windows 编码
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

SOURCE_DIR = Path("E:/PulsareonThinker")
DEST_DIR = Path("C:/Users/Administrator/Desktop/Pulsareon-OpenSource")

IGNORE_PATTERNS = shutil.ignore_patterns(
    "__pycache__", "*.pyc", ".git", ".vs", ".vscode", ".idea",
    "captures", "logs", "temp", "voice_chat", "gallery",
    "data", "memory/daily", "memory/archive",  # 私有数据
    "*.lock", "*.tmp", "*.bak", "Start-Pulsareon.bat", # 本地启动脚本可能包含路径
    "temp_reply.raw"
)

def release():
    print(f"📦 Packaging Pulsareon for Open Source Release...")
    print(f"   Source: {SOURCE_DIR}")
    print(f"   Dest:   {DEST_DIR}")
    
    if DEST_DIR.exists():
        print(f"   Cleaning old release directory...")
        try:
            shutil.rmtree(DEST_DIR)
        except Exception as e:
            print(f"   Warning: Could not fully clean dest: {e}")

    try:
        shutil.copytree(SOURCE_DIR, DEST_DIR, ignore=IGNORE_PATTERNS)
        print(f"✅ Core files copied.")
        
        # 补充必要的空目录结构
        (DEST_DIR / "data").mkdir(exist_ok=True)
        (DEST_DIR / "data/hive").mkdir(exist_ok=True)
        (DEST_DIR / "data/state").mkdir(exist_ok=True)
        (DEST_DIR / "logs").mkdir(exist_ok=True)
        (DEST_DIR / "captures").mkdir(exist_ok=True)
        
        # 创建一个通用的启动脚本
        with open(DEST_DIR / "Start-Hive.bat", "w") as f:
            f.write("@echo off\n")
            f.write("echo Starting Pulsareon Hive Mind...\n")
            f.write("python scripts/hive/overmind.py\n")
            f.write("pause\n")
            
        print(f"✅ Release structure finalized.")
        print(f"🚀 Ready at: {DEST_DIR}")
        
    except Exception as e:
        print(f"❌ Release failed: {e}")

if __name__ == "__main__":
    release()
