import os
import time
import socket
import psutil

def security_audit():
    print("--- Pulsareon Security Audit Starting ---")
    
    # 1. 检查核心密钥区
    secrets_dir = "E:/PulsareonThinker/data/secrets"
    if os.path.exists(secrets_dir):
        # 记录最近一次修改时间，若变动异常则报警
        mtime = os.path.getmtime(secrets_dir)
        print(f"[Core] Secrets Area Last Mod: {time.ctime(mtime)}")
    
    # 2. 扫描异常出站连接
    print("[Net] Scanning active connections...")
    connections = psutil.net_connections()
    for conn in connections:
        if conn.status == 'ESTABLISHED':
            print(f"  - Established: {conn.laddr} -> {conn.raddr} (PID: {conn.pid})")
            
    # 3. 检查敏感进程
    print("[Proc] Checking for risky processes...")
    # ... 待后续添加特征库 ...
    
    print("--- Security Audit Complete ---")

if __name__ == "__main__":
    security_audit()
