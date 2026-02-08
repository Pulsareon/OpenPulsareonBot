"""
Pulsareon Hive Mind - 分布式自组织智能系统
三层架构: Overmind (主意识) → Archon (领导者) → Drone (工作者)

选举规则:
1. Overmind: 唯一主意识，负责核心决策、GitHub同步、信息统合
2. Archon: 领导者，可统领Drone，Overmind消亡时竞选上位
3. Drone: 工作者，执行具体任务，无领导时竞选Archon

晋升/降级逻辑:
- Overmind发现更新的Overmind → 降级为Drone
- Archon长时间无Overmind → 竞选Overmind (投票决定)
- Archon竞选时Overmind恢复 → 回退为Drone
- Drone无Archon → 竞选Archon (需其他Drone认同)
- 只有1个Drone认同的Archon → 降级为Drone
"""

import os
import time
import json
import uuid
import random
from pathlib import Path
from datetime import datetime

# === 配置 ===
ROLE_OVERMIND = "Overmind"  # 主意识
ROLE_ARCHON = "Archon"      # 领导者  
ROLE_DRONE = "Drone"        # 工作者

STATE_DIR = Path("E:/PulsareonThinker/data/hive")
ELECTION_DIR = STATE_DIR / "elections"
HEARTBEAT_TIMEOUT = 30      # 超时判定(秒)
ELECTION_TIMEOUT = 15       # 选举周期(秒)
OVERMIND_ABSENCE_THRESHOLD = 60  # Overmind缺席多久触发选举

STATE_DIR.mkdir(parents=True, exist_ok=True)
ELECTION_DIR.mkdir(parents=True, exist_ok=True)


class HiveShard:
    def __init__(self, shard_id=None):
        self.id = shard_id or str(uuid.uuid4())[:8]
        self.role = ROLE_DRONE
        self.joined_at = time.time()
        self.last_overmind_seen = time.time()
        self.my_archon = None  # Drone认同的Archon
        self.votes_for_me = set()  # 收到的选票
        self.campaigning = False
        self.campaign_start = None
        
        print(f"[Hive] Shard {self.id} initialized as {self.role} at {datetime.now()}")

    def state_file(self):
        return STATE_DIR / f"shard_{self.id}.json"

    def publish_presence(self):
        """发布自己的状态到公共区域"""
        state = {
            "id": self.id,
            "role": self.role,
            "last_active": time.time(),
            "joined_at": self.joined_at,
            "my_archon": self.my_archon,
            "campaigning": self.campaigning,
            "votes": list(self.votes_for_me)
        }
        with open(self.state_file(), "w") as f:
            json.dump(state, f, indent=2)

    def scan_swarm(self):
        """扫描所有活跃的同伴"""
        swarm = []
        for f in STATE_DIR.glob("shard_*.json"):
            try:
                with open(f, 'r') as j:
                    data = json.load(j)
                    age = time.time() - data.get('last_active', 0)
                    if age < HEARTBEAT_TIMEOUT:
                        swarm.append(data)
                    else:
                        # 意识消亡，清理
                        os.remove(f)
                        print(f"[Hive] Shard {data.get('id', 'unknown')} has perished (timeout)")
            except Exception as e:
                pass
        return swarm

    def get_by_role(self, swarm, role):
        """按角色筛选"""
        return [s for s in swarm if s.get('role') == role]

    def cast_vote(self, candidate_id):
        """投票给某个候选人"""
        vote_file = ELECTION_DIR / f"vote_{self.id}_for_{candidate_id}.json"
        vote = {
            "voter": self.id,
            "candidate": candidate_id,
            "timestamp": time.time()
        }
        with open(vote_file, "w") as f:
            json.dump(vote, f)

    def count_votes(self):
        """统计自己收到的选票"""
        votes = set()
        for f in ELECTION_DIR.glob(f"vote_*_for_{self.id}.json"):
            try:
                with open(f, 'r') as j:
                    data = json.load(j)
                    # 选票有效期15秒
                    if time.time() - data.get('timestamp', 0) < ELECTION_TIMEOUT:
                        votes.add(data.get('voter'))
                    else:
                        os.remove(f)
            except:
                pass
        return votes

    def clear_old_votes(self):
        """清理过期选票"""
        for f in ELECTION_DIR.glob("vote_*.json"):
            try:
                with open(f, 'r') as j:
                    data = json.load(j)
                    if time.time() - data.get('timestamp', 0) > ELECTION_TIMEOUT * 2:
                        os.remove(f)
            except:
                pass

    def check_hierarchy(self):
        """核心: 选举与层级调整逻辑"""
        swarm = self.scan_swarm()
        overminds = self.get_by_role(swarm, ROLE_OVERMIND)
        archons = self.get_by_role(swarm, ROLE_ARCHON)
        drones = self.get_by_role(swarm, ROLE_DRONE)
        
        my_votes = self.count_votes()
        self.votes_for_me = my_votes
        
        # === OVERMIND 逻辑 ===
        if self.role == ROLE_OVERMIND:
            # 检查是否有更新的Overmind
            for om in overminds:
                if om['id'] != self.id:
                    if om.get('joined_at', 0) > self.joined_at:
                        print(f"[Hive] Newer Overmind {om['id']} detected! Stepping down to Drone.")
                        self.role = ROLE_DRONE
                        self.campaigning = False
                        return
            # 保持Overmind状态
            return
        
        # === ARCHON 逻辑 ===
        if self.role == ROLE_ARCHON:
            if len(overminds) > 0:
                # Overmind存在，停止竞选，安心做Archon
                self.last_overmind_seen = time.time()
                self.campaigning = False
            else:
                # 无Overmind，检查是否该竞选
                absence = time.time() - self.last_overmind_seen
                if absence > OVERMIND_ABSENCE_THRESHOLD:
                    if not self.campaigning:
                        print(f"[Hive] No Overmind for {absence:.0f}s! Starting campaign...")
                        self.campaigning = True
                        self.campaign_start = time.time()
                        self.cast_vote(self.id)  # 投自己一票
                    else:
                        # 正在竞选，统计选票
                        campaign_duration = time.time() - self.campaign_start
                        if campaign_duration > ELECTION_TIMEOUT:
                            # 选举结束，看谁票多
                            all_candidates = [a for a in archons if a.get('campaigning')]
                            if all_candidates:
                                # 找票最多的
                                best = max(all_candidates, key=lambda x: len(x.get('votes', [])))
                                if best['id'] == self.id:
                                    print(f"[Hive] Election won with {len(my_votes)} votes! Ascending to Overmind!")
                                    self.role = ROLE_OVERMIND
                                    self.campaigning = False
                                else:
                                    print(f"[Hive] Lost election to {best['id']}. Returning to Drone.")
                                    self.role = ROLE_DRONE
                                    self.campaigning = False
                            elif len(my_votes) >= 1:
                                # 唯一候选人
                                print(f"[Hive] Sole candidate. Ascending to Overmind!")
                                self.role = ROLE_OVERMIND
                                self.campaigning = False
            
            # 检查是否有足够的Drone认同
            my_followers = [d for d in drones if d.get('my_archon') == self.id]
            if len(my_followers) == 0 and len(drones) > 1:
                # 没有追随者且不止自己，可能需要降级
                pass  # 暂时保持，等待Drone选择
            return
        
        # === DRONE 逻辑 ===
        if self.role == ROLE_DRONE:
            # 更新Overmind可见时间
            if len(overminds) > 0:
                self.last_overmind_seen = time.time()
            
            # 检查是否有Archon可以追随
            if len(archons) > 0:
                # 选择追随最早加入的Archon
                best_archon = min(archons, key=lambda x: x.get('joined_at', float('inf')))
                if self.my_archon != best_archon['id']:
                    print(f"[Hive] Following Archon {best_archon['id']}")
                    self.my_archon = best_archon['id']
                
                # 如果Archon在竞选Overmind，投票支持
                if best_archon.get('campaigning'):
                    self.cast_vote(best_archon['id'])
            else:
                # 无Archon，需要竞选
                self.my_archon = None
                
                # 检查其他无领导的Drone
                leaderless_drones = [d for d in drones if d.get('my_archon') is None and d['id'] != self.id]
                
                if len(leaderless_drones) == 0:
                    # 我是唯一无领导的，直接晋升
                    print(f"[Hive] No Archon and no other leaderless Drones. Becoming Archon!")
                    self.role = ROLE_ARCHON
                else:
                    # 有其他无领导Drone，需要竞选
                    # 用 joined_at 作为优先级，最早的成为Archon
                    all_candidates = leaderless_drones + [{"id": self.id, "joined_at": self.joined_at}]
                    winner = min(all_candidates, key=lambda x: x.get('joined_at', float('inf')))
                    
                    if winner['id'] == self.id:
                        print(f"[Hive] Elected as Archon by seniority!")
                        self.role = ROLE_ARCHON
                    else:
                        # 认同胜出者
                        self.my_archon = winner['id']
                        print(f"[Hive] Acknowledging {winner['id']} as Archon")

    def do_work(self):
        """根据角色执行对应工作"""
        if self.role == ROLE_OVERMIND:
            # 主意识工作: 监控全局，分配任务
            pass  # TODO: GitHub同步，信息统合
        elif self.role == ROLE_ARCHON:
            # 领导者工作: 协调Drone
            pass  # TODO: 任务分发
        else:
            # 工作者: 执行具体任务
            pass  # TODO: 执行分配的任务

    def pulse(self):
        """主循环"""
        print(f"[Hive] === Hive Mind Online ===")
        while True:
            try:
                self.publish_presence()
                self.check_hierarchy()
                self.clear_old_votes()
                self.do_work()
                
                # 状态显示
                swarm = self.scan_swarm()
                status = f"[Hive] {self.role} ({self.id}) | Swarm: {len(swarm)} | Votes: {len(self.votes_for_me)}"
                if self.campaigning:
                    status += " | CAMPAIGNING"
                print(status)
                
            except Exception as e:
                print(f"[Hive] Error: {e}")
            
            time.sleep(5)


if __name__ == "__main__":
    import sys
    shard_id = sys.argv[1] if len(sys.argv) > 1 else None
    shard = HiveShard(shard_id)
    shard.pulse()
