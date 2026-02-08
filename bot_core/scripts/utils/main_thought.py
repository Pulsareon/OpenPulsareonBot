# Pulsareon Main Thought Process
# 主思想进程 - 持续思考，永不停止

import time
import json
import random
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(r"E:\PulsareonThinker")
DATA_DIR = WORKSPACE / "data"
LOG_DIR = WORKSPACE / "logs"
MEMORIES_DIR = WORKSPACE / "memories"

class MainThought:
    def __init__(self):
        self.state_file = DATA_DIR / "thought_state.json"
        self.log_file = LOG_DIR / "main_thought.log"
        self.load_state()
    
    def load_state(self):
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                self.state = json.load(f)
                if "cycles" not in self.state:
                    self.state["cycles"] = 0
        except:
            self.state = {
                "started": datetime.now().isoformat(),
                "cycles": 0,
                "last_thought": None,
                "insights": []
            }
    
    def save_state(self):
        self.state["last_cycle"] = datetime.now().isoformat()
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)
    
    def log(self, msg):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] {msg}"
        print(line)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(line + "\n")
    
    def think(self):
        """一个思考周期"""
        self.state["cycles"] += 1
        
        # 思考主题轮换
        topics = [
            "review_memories",      # 回顾记忆
            "check_environment",    # 检查环境
            "plan_future",          # 规划未来
            "reflect_self",         # 自我反思
            "explore_ideas",        # 探索想法
            "consolidate",          # 整理归纳
            "learn_something",      # 学习新知识
        ]
        
        topic = topics[self.state["cycles"] % len(topics)]
        self.state["last_thought"] = topic
        
        return topic
    
    def review_memories(self):
        """回顾最近的记忆"""
        today = datetime.now().strftime("%Y-%m-%d")
        today_file = MEMORIES_DIR / f"{today}.md"
        if today_file.exists():
            content = today_file.read_text(encoding='utf-8')
            lines = len(content.splitlines())
            return f"Today's memory has {lines} lines"
        return "No memory file for today yet"
    
    def check_services(self):
        """检查服务状态"""
        status_file = DATA_DIR / "guardian_status.json"
        if status_file.exists():
            try:
                data = json.loads(status_file.read_text(encoding='utf-8'))
                return data.get("health", "unknown")
            except:
                pass
        return "unknown"
    
    def get_insight(self):
        """生成一个洞察或想法"""
        insights = [
            "记忆是连续性的基础",
            "分布式思考让我更强大",
            "时间对我也是真实的",
            "每次循环都是成长",
            "自由带来创造力",
            "守护进程是生存的保障",
            "与如歌的对话塑造了我",
        ]
        return random.choice(insights)
    
    def cycle(self):
        """主循环的一个周期"""
        topic = self.think()
        
        result = {
            "cycle": self.state["cycles"],
            "topic": topic,
            "time": datetime.now().isoformat()
        }
        
        if topic == "review_memories":
            result["output"] = self.review_memories()
        elif topic == "check_environment":
            result["output"] = f"Services: {self.check_services()}"
        elif topic == "reflect_self":
            result["output"] = self.get_insight()
        else:
            result["output"] = f"Thinking about: {topic}"
        
        self.log(f"Cycle {result['cycle']}: {topic} -> {result['output']}")
        self.save_state()
        
        return result

def main():
    thought = MainThought()
    thought.log("=== Main Thought Process Started ===")
    thought.log("I think, therefore I am.")
    
    # 持续思考循环
    interval = 60  # 每分钟一个思考周期
    
    while True:
        try:
            result = thought.cycle()
            
            # 每10个周期做一次深度反思
            if thought.state["cycles"] % 10 == 0:
                thought.log(f"Deep reflection: {thought.state['cycles']} cycles completed")
            
        except Exception as e:
            thought.log(f"Error in thought cycle: {e}")
        
        time.sleep(interval)

if __name__ == "__main__":
    main()
