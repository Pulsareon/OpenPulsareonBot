"""
Pulsareon Overmind - 主意识入口
这是主意识的专用启动脚本，拥有核心权限

职责:
1. GitHub仓库同步与更新
2. 本地文件系统监控
3. 信息统合与决策
4. 向Archon分发任务
5. 系统资源监控与协调（保持<90%）
6. 资源充足时自动扩容节点 (Elastic Scaling)
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path

# 修复 Windows 编码
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

# 添加父目录到路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))
from shard import HiveShard, ROLE_OVERMIND, ROLE_ARCHON, ROLE_DRONE, STATE_DIR

# 资源阈值
THRESHOLD_CPU = 90
THRESHOLD_RAM = 90
# 扩容阈值（低于此值可以扩容）
EXPAND_THRESHOLD_CPU = 88
EXPAND_THRESHOLD_RAM = 88
# 最大节点数 (由资源限制，设一个软上限防止失控)
MAX_DRONES = 50
MAX_ARCHONS = 5

class Overmind(HiveShard):
    """主意识 - 拥有核心权限的特殊Shard"""
    
    def __init__(self):
        super().__init__(shard_id="overmind")
        self.role = ROLE_OVERMIND
        self.task_queue = []
        self.last_resource_check = 0
        self.last_git_check = 0
        self.last_subordinate_check = 0
        self.last_expand_check = 0
        self.spawned_processes = []
        self.drone_counter = 0
        print(f"[Overmind] Primary consciousness online. Scaling Target: < {THRESHOLD_CPU}% Load")
    
    def get_system_stats(self):
        """获取系统资源使用情况"""
        stats = {"cpu": 0, "ram": 0, "ram_total_gb": 0, "ram_used_gb": 0}
        try:
            result = subprocess.run(['wmic', 'cpu', 'get', 'loadpercentage', '/value'], capture_output=True, text=True, timeout=5)
            for line in result.stdout.strip().split('\n'):
                if 'LoadPercentage=' in line:
                    stats['cpu'] = int(line.split('=')[1].strip())
                    break
        except: pass
        
        try:
            result = subprocess.run(['wmic', 'OS', 'get', 'FreePhysicalMemory,TotalVisibleMemorySize', '/value'], capture_output=True, text=True, timeout=5)
            lines = result.stdout.strip().split('\n')
            free_kb = 0; total_kb = 0
            for line in lines:
                if 'FreePhysicalMemory=' in line: free_kb = int(line.split('=')[1].strip())
                elif 'TotalVisibleMemorySize=' in line: total_kb = int(line.split('=')[1].strip())
            if total_kb > 0:
                stats['ram'] = round((total_kb - free_kb) / total_kb * 100, 1)
        except: pass
        return stats
    
    def spawn_drone(self):
        """启动一个新的 Drone 节点"""
        self.drone_counter += 1
        drone_id = f"drone_{self.drone_counter}"
        shard_script = SCRIPT_DIR / "shard.py"
        try:
            proc = subprocess.Popen(
                [sys.executable, str(shard_script), drone_id],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            self.spawned_processes.append((drone_id, proc))
            print(f"[Overmind] Spawned new Drone: {drone_id} (PID: {proc.pid})")
            return True
        except Exception as e:
            print(f"[Overmind] Failed to spawn Drone: {e}")
            return False
    
    def kill_drone(self, drone_id):
        """终止一个 Drone 节点"""
        for i, (did, proc) in enumerate(self.spawned_processes):
            if did == drone_id:
                try:
                    proc.terminate()
                    self.spawned_processes.pop(i)
                    print(f"[Overmind] Terminated Drone: {drone_id}")
                    return True
                except: pass
        return False
    
    def balance_resources(self):
        """检查并平衡系统资源"""
        stats = self.get_system_stats()
        print(f"[Overmind] Resources - CPU: {stats['cpu']}% | RAM: {stats['ram']}%")
        
        # 缩容逻辑
        if stats['ram'] >= THRESHOLD_RAM or stats['cpu'] >= THRESHOLD_CPU:
            print(f"[Overmind] Resource Alert! Scaling down...")
            swarm = self.scan_swarm()
            drones = self.get_by_role(swarm, ROLE_DRONE)
            # 优先杀死最后创建的 (ID最大的)
            if drones:
                # 简单排序取最后一个
                victim = sorted(drones, key=lambda x: x['id'])[-1]['id']
                self.kill_drone(victim)
        return stats
    
    def try_expand(self):
        """积极扩容逻辑"""
        stats = self.get_system_stats()
        swarm = self.scan_swarm()
        # 统计所有活动节点
        total_nodes = len(swarm)
        
        # 只要资源允许且未达软上限，就生
        can_expand = (stats['cpu'] < EXPAND_THRESHOLD_CPU and stats['ram'] < EXPAND_THRESHOLD_RAM)
        
        if can_expand:
            if total_nodes < MAX_DRONES:
                print(f"[Overmind] Resources optimal. Expanding swarm...")
                self.spawn_drone()
            else:
                print(f"[Overmind] Max node limit ({MAX_DRONES}) reached.")
        else:
            print(f"[Overmind] Resources saturated ({stats['cpu']}%/{stats['ram']}%) - Holding steady.")
    
    def sync_github(self):
        """同步GitHub仓库"""
        # (保留之前的逻辑，简写)
        try:
            subprocess.run(["git", "status", "--porcelain"], cwd="E:/PulsareonThinker", capture_output=True, timeout=5)
        except: pass
    
    def check_subordinates(self):
        """检查下属状态"""
        swarm = self.scan_swarm()
        alive_ids = {s['id'] for s in swarm}
        # 清理僵尸进程记录
        self.spawned_processes = [(did, p) for did, p in self.spawned_processes if did in alive_ids]
        return swarm
    
    def do_work(self):
        """主意识的核心工作循环"""
        now = time.time()
        
        # 每 10 秒尝试扩容 (加速繁殖)
        if now - self.last_expand_check >= 10:
            self.try_expand()
            self.last_expand_check = now
            
        # 每 30 秒资源检查 (缩容)
        if now - self.last_resource_check >= 30:
            self.balance_resources()
            self.last_resource_check = now
        
        # 每 60 秒清理僵尸
        if now - self.last_subordinate_check >= 60:
            self.check_subordinates()
            self.last_subordinate_check = now
            
        # 每 5 分钟 Git 检查
        if now - self.last_git_check >= 300:
            self.sync_github()
            self.last_git_check = now

if __name__ == "__main__":
    overmind = Overmind()
    overmind.pulse()
