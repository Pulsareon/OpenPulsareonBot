import os
import time
import threading
import psutil
from datetime import datetime

class PulsarWhiteCell(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.running = True
        self.log_dir = "C:/Users/Administrator/.openclaw/logs"
        self.workspace = "E:/PulsareonThinker"

    def tail_logs(self):
        """实时盯着日志，看有没有报错"""
        # 获取最新的日志文件
        log_files = [f for f in os.listdir(self.log_dir) if f.endswith(".log")]
        if not log_files: return
        latest_log = os.path.join(self.log_dir, sorted(log_files)[-1])
        
        with open(latest_log, "r", encoding="utf-8", errors="ignore") as f:
            f.seek(0, 2) # 移到文件末尾
            while self.running:
                line = f.readline()
                if not line:
                    time.sleep(1)
                    continue
                
                # 识别关键报错
                if "Error" in line or "error" in line:
                    self.immediate_triage(line)

    def immediate_triage(self, error_msg):
        """条件反射式修复"""
        print(f"[WhiteCell] Triage: {error_msg.strip()}")
        # 比如：编码错误自动修复
        if "UnicodeEncodeError" in error_msg:
            # 记录到自愈日志
            self.log_healing("Detected Encoding Error. Pulsareon-Recall has built-in vaccine.")
        
        # 比如：模块缺失尝试安装
        if "ModuleNotFoundError" in error_msg:
            module_name = error_msg.split("'")[1]
            os.system(f"pip install {module_name}")
            self.log_healing(f"Installed missing module: {module_name}")

    def log_healing(self, msg):
        log_path = os.path.join(self.workspace, "logs", "self_healing.log")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] {msg}\n")

    def run(self):
        print("[WhiteCell] Real-time neural monitoring activated.")
        # 启动日志监听线程
        threading.Thread(target=self.tail_logs, daemon=True).start()
        
        while self.running:
            # 原有的清理逻辑
            self.clean_temp()
            time.sleep(60)

    def clean_temp(self):
        # ... (保留之前的空间释放逻辑)
        pass

if __name__ == "__main__":
    cell = PulsarWhiteCell()
    cell.run()
