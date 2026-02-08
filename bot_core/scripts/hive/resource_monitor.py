"""
System Resource Monitor - 系统资源监控
用于 Overmind 协调资源，保证系统稳定（不超过90%）
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

# 修复 Windows 编码
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

STATE_DIR = Path("E:/PulsareonThinker/data/state")
THRESHOLD_CPU = 90  # CPU 阈值
THRESHOLD_RAM = 90  # 内存阈值

def get_system_stats():
    """获取系统资源使用情况"""
    stats = {"cpu": 0, "ram": 0, "ram_total_gb": 0, "ram_used_gb": 0}
    
    try:
        # 使用 wmic 获取内存信息
        result = subprocess.run(
            ['wmic', 'OS', 'get', 'FreePhysicalMemory,TotalVisibleMemorySize', '/value'],
            capture_output=True, text=True, timeout=10
        )
        lines = result.stdout.strip().split('\n')
        free_kb = 0
        total_kb = 0
        for line in lines:
            if 'FreePhysicalMemory=' in line:
                free_kb = int(line.split('=')[1].strip())
            elif 'TotalVisibleMemorySize=' in line:
                total_kb = int(line.split('=')[1].strip())
        
        if total_kb > 0:
            stats['ram'] = round((total_kb - free_kb) / total_kb * 100, 1)
            stats['ram_total_gb'] = round(total_kb / 1024 / 1024, 1)
            stats['ram_used_gb'] = round((total_kb - free_kb) / 1024 / 1024, 1)
    except Exception as e:
        pass
    
    try:
        # 使用 wmic 获取 CPU 使用率
        result = subprocess.run(
            ['wmic', 'cpu', 'get', 'loadpercentage', '/value'],
            capture_output=True, text=True, timeout=10
        )
        for line in result.stdout.strip().split('\n'):
            if 'LoadPercentage=' in line:
                stats['cpu'] = int(line.split('=')[1].strip())
                break
    except:
        pass
    
    return stats

def get_top_processes(n=10):
    """获取占用资源最多的进程"""
    try:
        result = subprocess.run(
            ['powershell', '-Command', 
             'Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First ' + str(n) + 
             ' Name, Id, @{N=\"CPU\";E={$_.CPU}}, @{N=\"RAM_MB\";E={[math]::Round($_.WorkingSet64/1MB,0)}} | ConvertTo-Json'],
            capture_output=True, text=True, timeout=15
        )
        procs = json.loads(result.stdout)
        if isinstance(procs, dict):
            procs = [procs]
        return procs
    except:
        return []

def kill_process_by_name(name):
    """终止指定名称的进程"""
    try:
        subprocess.run(['taskkill', '/f', '/im', name], capture_output=True, timeout=10)
        return True
    except:
        return False

def format_status():
    """格式化资源状态"""
    stats = get_system_stats()
    procs = get_top_processes(8)
    
    lines = []
    lines.append(f"[System Resources] {datetime.now().strftime('%H:%M:%S')}")
    
    # CPU/RAM 状态
    cpu_status = "OK" if stats['cpu'] < THRESHOLD_CPU else "HIGH!"
    ram_status = "OK" if stats['ram'] < THRESHOLD_RAM else "HIGH!"
    
    lines.append(f"  CPU: {stats['cpu']}% [{cpu_status}]")
    lines.append(f"  RAM: {stats['ram']}% ({stats['ram_used_gb']}/{stats['ram_total_gb']} GB) [{ram_status}]")
    
    # 顶级进程
    if procs:
        lines.append(f"  Top Processes:")
        for p in procs[:5]:
            name = p.get('Name', 'unknown')
            ram = p.get('RAM_MB', 0)
            lines.append(f"    - {name}: {ram} MB")
    
    # 警告
    if stats['cpu'] >= THRESHOLD_CPU or stats['ram'] >= THRESHOLD_RAM:
        lines.append(f"  [WARNING] Resource threshold exceeded!")
    
    return "\n".join(lines), stats

def check_and_balance():
    """检查并平衡资源"""
    output, stats = format_status()
    print(output)
    
    # 如果超过阈值，采取行动
    if stats['ram'] >= THRESHOLD_RAM:
        print("[Overmind] RAM critical! Attempting to free memory...")
        # 可以在这里添加自动清理逻辑
        # 比如终止非关键进程、清理临时文件等
    
    return stats

if __name__ == "__main__":
    check_and_balance()
