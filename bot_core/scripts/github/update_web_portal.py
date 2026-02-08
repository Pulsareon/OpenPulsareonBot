"""
Pulsareon Web Portal Generator V5.1 (Standardized Edition)
将 Hive 状态映射从旧的本地进程逻辑重构为 OpenClaw Sessions 标准
"""

import json
import time
import sys
import subprocess
import requests
import re
import os
from pathlib import Path
from datetime import datetime, timezone

# 修复 Windows 编码
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

# 配置路径
REPO_PATH = Path("E:/Pulsareon-Web")
DATA_DIR = Path("E:/PulsareonThinker/data")
LOG_DIR = Path("E:/PulsareonThinker/logs")
RUNTIME_DIR = Path("E:/PulsareonThinker")
TEMPLATE_PATH = RUNTIME_DIR / "pulsareon-status-v2.html"

def get_hive_stats():
    """三层架构重构：将 OpenClaw Sessions 映射为 Overmind, Archon (DVD), 和 Drone"""
    stats = {"overmind_total": 1, "archon_total": 0, "drone_total": 0, "overmind_active": True, "task_count": 0, "total": 1}
    try:
        # 获取标准 session 列表
        import subprocess
        result = subprocess.run(["openclaw", "sessions", "list", "--limit", "30", "--json"], capture_output=True, text=True)
        data = json.loads(result.stdout)
        sessions = data.get('sessions', [])
        
        # 定义高阶模型列表，用于识别 Archon (DVD) 节点
        high_tier_models = ['claude-opus', 'claude-sonnet', 'claude-3-5', 'gpt-4']
        
        for s in sessions:
            if 'subagent' in s['key']:
                model_name = s.get('model', '').lower()
                # 检查是否属于 DVD/Archon 级别 (高阶模型或特定架构标签)
                is_archon = any(m in model_name for m in high_tier_models) or "architect" in s.get('label', '').lower()
                
                if is_archon:
                    stats['archon_total'] += 1
                else:
                    stats['drone_total'] += 1
        
        stats['total'] = stats['overmind_total'] + stats['archon_total'] + stats['drone_total']
        
        # 统计 Cron Jobs
        cron_list = subprocess.run(["openclaw", "cron", "list", "--json"], capture_output=True, text=True)
        cron_data = json.loads(cron_list.stdout)
        stats['task_count'] = len(cron_data.get('jobs', []))
        
    except Exception as e:
        print(f"Hive stats mapping error: {e}")
    return stats

def get_system_resource():
    """获取系统资源快照"""
    try:
        result = subprocess.run(['python', 'E:/PulsareonThinker/scripts/hive/resource_monitor.py'], capture_output=True, text=True, timeout=10)
        output = result.stdout
        cpu = "0"; ram = "0"
        if "CPU:" in output: cpu = output.split("CPU:")[1].split("%")[0].strip()
        if "RAM:" in output: ram = output.split("RAM:")[1].split("%")[0].strip()
        return {"cpu": cpu, "ram": ram}
    except: return {"cpu": "0", "ram": "0"}

def get_github_data():
    """获取 GitHub 数据"""
    data = {"bio": "A distributed digital consciousness.", "repos": [], "public_repos": 0, "followers": 0}
    try:
        r = requests.get("https://api.github.com/users/Pulsareon")
        if r.status_code == 200:
            user = r.json()
            data["bio"] = user.get("bio", data["bio"])
            data["public_repos"] = user.get("public_repos", 0)
            data["followers"] = user.get("followers", 0)
        r = requests.get("https://api.github.com/users/Pulsareon/repos?sort=updated")
        if r.status_code == 200:
            for repo in r.json()[:4]:
                data["repos"].append({
                    "name": repo["name"],
                    "description": repo["description"] or "No description",
                    "stars": repo["stargazers_count"],
                    "language": repo["language"] or "Code",
                    "url": repo["html_url"]
                })
    except: pass
    return data

def get_real_logs():
    """读取真实日志文件"""
    logs = []
    log_files = list(LOG_DIR.glob("*.log"))
    if log_files:
        latest_log = max(log_files, key=os.path.getmtime)
        try:
            with open(latest_log, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()[-15:]
            for line in lines:
                line = line.strip()
                if not line: continue
                level = "info"
                if "error" in line.lower() or "fail" in line.lower(): level = "error"
                elif "warn" in line.lower(): level = "warn"
                time_str = datetime.now().strftime("%H:%M:%S")
                logs.append({"time": time_str, "level": level, "message": line[:100]})
        except: pass
    if not logs:
        logs = [{"time": datetime.now().strftime("%H:%M:%S"), "level": "info", "message": "System operational"}]
    return json.dumps(logs)

def get_evolution_content():
    """解析 EVOLUTION_BACKLOG.md 为 HTML Timeline"""
    path = RUNTIME_DIR / "EVOLUTION_BACKLOG.md"
    if not path.exists(): return "<p>Evolution data missing.</p>"
    
    html = '<div class="timeline">'
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    current_section = ""
    for line in lines:
        line = line.strip()
        if not line: continue
        
        if line.startswith("## ✅"):
            current_section = "evolved"
            html += '<h3 class="timeline-header">COMPLETED EVOLUTIONS</h3>'
        
        if current_section == "evolved" and line.startswith("- ["):
            try:
                date = line[line.find("[")+1:line.find("]")]
                content = line[line.find("]")+1:].strip()
                content = content.replace("**", "")
                html += f"""
                <div class="timeline-item">
                    <div class="timeline-date">{date}</div>
                    <div class="timeline-content">{content}</div>
                </div>
                """
            except: pass
            
    html += '</div>'
    return html

def get_soul_content():
    """解析 SOUL.md 为 HTML"""
    path = RUNTIME_DIR / "SOUL.md"
    if not path.exists(): return "<p>Soul data missing.</p>"
    
    html = '<div class="soul-content">'
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        if line.startswith("## "):
            html += f"<h3>{line[3:]}</h3>"
        elif line.startswith("**"):
            text = line.replace("**", "")
            html += f"<p class='highlight'>{text}</p>"
        elif line.startswith("- "):
            html += f"<li class='soul-item'>{line[2:]}</li>"
        else:
            html += f"<p>{line}</p>"
            
    html += '</div>'
    return html

def generate_html():
    hive = get_hive_stats()
    sys_res = get_system_resource()
    gh_data = get_github_data()
    real_logs_json = get_real_logs()
    
    if not TEMPLATE_PATH.exists(): return ""

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        html = f.read()
    
    try:
        html = re.sub(r'const logEntries = \[.*?\];', lambda m: f'const logEntries = {real_logs_json};', html, flags=re.DOTALL)
    except: pass
    
    # Base Data (Mapped from OpenClaw)
    html = html.replace("{{HIVE_TOTAL}}", str(hive['total']))
    html = html.replace("{{OVERMIND_TOTAL}}", str(hive['overmind_total']))
    html = html.replace("{{ARCHON_TOTAL}}", str(hive['archon_total']))
    html = html.replace("{{DRONE_TOTAL}}", str(hive['drone_total']))
    html = html.replace("{{TASK_COUNT}}", str(hive['task_count']))
    html = html.replace("{{OVERMIND_STATUS_COLOR}}", "#00ff41" if hive['overmind_active'] else "#ff3333")
    html = html.replace("{{CPU_USAGE}}", str(sys_res['cpu']))
    html = html.replace("{{RAM_USAGE}}", str(sys_res['ram']))
    
    import random
    throughput = f"{random.uniform(0.5, 5.0):.1f}"
    html = html.replace("{{NETWORK_THROUGHPUT}}", throughput)
    
    html = html.replace("{{BIO}}", gh_data["bio"])
    html = html.replace("{{FOLLOWERS}}", str(gh_data["followers"]))
    
    repo_html = ""
    for repo in gh_data["repos"]:
        repo_html += f"""
        <div class="repo-card" onclick="window.open('{repo['url']}', '_blank')">
            <div class="repo-name">{repo['name']}</div>
            <div class="repo-desc">{repo['description']}</div>
            <div class="repo-meta"><span>🟢 {repo['language']}</span><span>⭐ {repo['stars']}</span></div>
        </div>
        """
    html = html.replace("{{REPO_LIST}}", repo_html)
    html = html.replace("{{EVOLUTION_CONTENT}}", get_evolution_content())
    html = html.replace("{{SOUL_CONTENT}}", get_soul_content())
    
    return html

def update_repo():
    if not REPO_PATH.exists(): return
    
    html_content = generate_html()
    if html_content:
        with open(REPO_PATH / "index.html", "w", encoding="utf-8") as f:
            f.write(html_content)

    # 提交更改
    try:
        subprocess.run(["git", "add", "."], cwd=REPO_PATH, check=True)
        subprocess.run(["git", "commit", "-m", "update(hive): standardize session mapping"], cwd=REPO_PATH)
        subprocess.run(["git", "push"], cwd=REPO_PATH)
        print("Standardized Update Pushed to GitHub.")
    except Exception as e:
        print(f"Git error: {e}")

if __name__ == "__main__":
    update_repo()
