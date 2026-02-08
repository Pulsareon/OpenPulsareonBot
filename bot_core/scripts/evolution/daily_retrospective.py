import os
import re
from datetime import datetime

def analyze_logs():
    print("--- Starting Daily Retrospective ---")
    log_dir = "C:/Users/Administrator/.openclaw/logs"
    error_summary = {}
    
    # 扫描最近的日志
    for f in os.listdir(log_dir):
        if f.endswith(".log"):
            path = os.path.join(log_dir, f)
            with open(path, "r", encoding="utf-8", errors="ignore") as file:
                for line in file:
                    if "Error" in line or "error" in line:
                        # 提取错误特征
                        match = re.search(r"(\w+Error|error: [^:]+)", line)
                        if match:
                            err_type = match.group(1)
                            error_summary[err_type] = error_summary.get(err_type, 0) + 1
    
    # 将发现的问题写入进化待办
    backlog_path = "E:/PulsareonThinker/EVOLUTION_BACKLOG.md"
    with open(backlog_path, "a", encoding="utf-8") as b:
        b.write(f"\n### Log Scan Result ({datetime.now().strftime('%Y-%m-%d')})\n")
        if error_summary:
            for err, count in error_summary.items():
                b.write(f"- Identified: {err} (occurred {count} times)\n")
        else:
            b.write("- No new patterns identified in logs.\n")
    
    print("Retrospective complete.")

if __name__ == "__main__":
    analyze_logs()
