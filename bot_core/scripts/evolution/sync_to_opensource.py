"""
Pulsareon Sync Manager
将 E:/PulsareonThinker (Runtime) 同步到 Desktop/TempWork (Open Source Repos)

目标仓库：
1. OpenPulsareonBot (Core)
2. Pulsareon-Web (Portal)
"""

import os
import sys
import shutil
from pathlib import Path

# 修复 Windows 编码
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

RUNTIME_DIR = Path("E:/PulsareonThinker")
TEMP_WORK = Path("C:/Users/Administrator/Desktop/TempWork")
REPO_CORE = TEMP_WORK / "OpenPulsareonBot"
REPO_WEB = TEMP_WORK / "Pulsareon-Web"

# 忽略列表 (不应同步到开源仓库的文件)
# 包含：运行时数据、隐私配置、特定环境脚本
IGNORE_CORE = shutil.ignore_patterns(
    # System
    "__pycache__", ".git", ".vs", "*.pyc",
    
    # Runtime Data
    "captures", "logs", "temp", "voice_chat",
    "data", "memory", "gallery",
    "*.lock", "*.tmp", "*.bak", "*.log",
    
    # Secrets & Private Docs
    "secrets", "SECRETS*.md", "EVOLUTION_BACKLOG.md",
    
    # Specific Sensitive Scripts
    "refresh_token.py",
    "update_oauth.py",
    "temp_*.py", "test_*.py",
    
    # Email Scripts (Private addresses)
    "process_web_signals.py",
    
    # Guardian Scripts (Account management)
    "check_accounts.py",
    "check_all_accounts.py",
    "enable_all_accounts.py",
    "auto_auth_flow.py",
    "visual_auth.py",
    "capture_verify_url.py"
)

def sync_core():
    print(f"🔄 Syncing Core to {REPO_CORE}...")
    if not REPO_CORE.exists():
        print(f"❌ Target repo not found: {REPO_CORE}")
        return

    # 关键目录/文件列表
    targets = [
        "scripts",
        "skills",
        "docs",
        "README.md",
        "LICENSE",
        "HEARTBEAT.md",
        "SOUL.md",
        "USER.md",
        "IDENTITY.md",
        "pulsareon-status.html"
    ]

    for item in targets:
        src = RUNTIME_DIR / item
        dst = REPO_CORE / item
        
        if src.exists():
            if src.is_dir():
                # 目录：先删除目标(清理旧文件)，再复制
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(src, dst, ignore=IGNORE_CORE)
                print(f"   ✅ Copied dir: {item}")
            else:
                # 文件：直接复制
                shutil.copy2(src, dst)
                print(f"   ✅ Copied file: {item}")
        else:
            print(f"   ⚠️ Source missing: {item}")

def sync_web():
    print(f"🔄 Syncing Web to {REPO_WEB}...")
    if not REPO_WEB.exists():
        print(f"❌ Target repo not found: {REPO_WEB}")
        return

    # 重新生成最新的 HTML
    try:
        sys.path.insert(0, str(RUNTIME_DIR / "scripts/github"))
        import update_web_portal
        html = update_web_portal.generate_html()
        
        with open(REPO_WEB / "index.html", "w", encoding="utf-8") as f:
            f.write(html)
        print(f"   ✅ index.html updated.")
    except Exception as e:
        print(f"   ❌ Web sync failed: {e}")

if __name__ == "__main__":
    sync_core()
    sync_web()
    print("\n✅ Sync Complete. Please manually commit and push from Desktop/TempWork.")
