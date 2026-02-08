"""
Pulsareon Distribution Protocol (PDP) v1.0
统一消息格式与通信接口

用于 Overmind ↔ Archon ↔ Drone 之间的结构化通信
"""

import json
import time
import uuid
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, Any, List


class MessageType(Enum):
    TASK = "task"
    REPORT = "report"
    VOTE_REQUEST = "vote_request"
    VOTE = "vote"
    HEARTBEAT = "heartbeat"
    SHUTDOWN = "shutdown"
    BROADCAST = "broadcast"


class Priority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class PDPMessage:
    """PDP 协议消息"""
    
    def __init__(
        self,
        msg_type: MessageType,
        sender: str,
        receiver: str,
        payload: Dict[str, Any],
        priority: Priority = Priority.NORMAL,
        msg_id: str = None
    ):
        self.id = msg_id or uuid.uuid4().hex[:12]
        self.type = msg_type
        self.sender = sender
        self.receiver = receiver
        self.payload = payload
        self.priority = priority
        self.timestamp = datetime.now().isoformat()
    
    def to_json(self) -> str:
        return json.dumps({
            "id": self.id,
            "type": self.type.value,
            "from": self.sender,
            "to": self.receiver,
            "payload": self.payload,
            "priority": self.priority.value,
            "timestamp": self.timestamp
        }, ensure_ascii=False)
    
    @classmethod
    def from_json(cls, json_str: str) -> "PDPMessage":
        data = json.loads(json_str)
        return cls(
            msg_type=MessageType(data["type"]),
            sender=data["from"],
            receiver=data["to"],
            payload=data["payload"],
            priority=Priority(data.get("priority", "normal")),
            msg_id=data.get("id")
        )
    
    def __repr__(self):
        return f"<PDP {self.type.value}: {self.sender} → {self.receiver}>"


# === 消息工厂函数 ===

def create_task(
    sender: str,
    receiver: str,
    description: str,
    context: str = "",
    deadline_minutes: int = 30,
    priority: Priority = Priority.NORMAL
) -> PDPMessage:
    """创建任务消息"""
    return PDPMessage(
        msg_type=MessageType.TASK,
        sender=sender,
        receiver=receiver,
        payload={
            "task_id": uuid.uuid4().hex[:8],
            "description": description,
            "context": context,
            "deadline_minutes": deadline_minutes,
            "created_at": datetime.now().isoformat()
        },
        priority=priority
    )


def create_report(
    sender: str,
    receiver: str,
    task_id: str,
    status: str,  # completed|failed|blocked|in_progress
    result: str,
    artifacts: List[str] = None
) -> PDPMessage:
    """创建报告消息"""
    return PDPMessage(
        msg_type=MessageType.REPORT,
        sender=sender,
        receiver=receiver,
        payload={
            "task_id": task_id,
            "status": status,
            "result": result,
            "artifacts": artifacts or [],
            "completed_at": datetime.now().isoformat()
        }
    )


def create_vote_request(
    sender: str,
    receiver: str,  # 可以是 "broadcast" 表示发给所有 Archon
    proposal: str,
    options: List[str] = None,
    deadline_minutes: int = 5
) -> PDPMessage:
    """创建投票请求"""
    return PDPMessage(
        msg_type=MessageType.VOTE_REQUEST,
        sender=sender,
        receiver=receiver,
        payload={
            "proposal_id": uuid.uuid4().hex[:8],
            "proposal": proposal,
            "options": options or ["approve", "reject", "abstain"],
            "deadline_minutes": deadline_minutes
        },
        priority=Priority.HIGH
    )


def create_vote(
    sender: str,
    receiver: str,
    proposal_id: str,
    vote: str,
    reason: str = ""
) -> PDPMessage:
    """创建投票响应"""
    return PDPMessage(
        msg_type=MessageType.VOTE,
        sender=sender,
        receiver=receiver,
        payload={
            "proposal_id": proposal_id,
            "vote": vote,
            "reason": reason
        }
    )


def create_heartbeat(
    sender: str,
    status: str = "idle",  # idle|busy|overloaded
    active_tasks: int = 0,
    resource_usage: Dict[str, int] = None
) -> PDPMessage:
    """创建心跳消息"""
    return PDPMessage(
        msg_type=MessageType.HEARTBEAT,
        sender=sender,
        receiver="overmind",
        payload={
            "status": status,
            "active_tasks": active_tasks,
            "resource_usage": resource_usage or {},
            "uptime_seconds": 0  # 由发送方填充
        }
    )


def create_shutdown(sender: str, receiver: str, reason: str = "") -> PDPMessage:
    """创建终止消息"""
    return PDPMessage(
        msg_type=MessageType.SHUTDOWN,
        sender=sender,
        receiver=receiver,
        payload={"reason": reason},
        priority=Priority.CRITICAL
    )


# === 消息解析 ===

def parse_message(text: str) -> Optional[PDPMessage]:
    """尝试从文本解析 PDP 消息"""
    text = text.strip()
    
    # 尝试直接解析 JSON
    if text.startswith("{"):
        try:
            return PDPMessage.from_json(text)
        except:
            pass
    
    # 尝试提取 JSON 块
    import re
    json_match = re.search(r'\{[^{}]*"type"[^{}]*\}', text, re.DOTALL)
    if json_match:
        try:
            return PDPMessage.from_json(json_match.group())
        except:
            pass
    
    return None


def is_pdp_message(text: str) -> bool:
    """检查文本是否包含 PDP 消息"""
    return parse_message(text) is not None


# === Synapse 集成 ===

SYNAPSE_FILE = Path("E:/PulsareonThinker/data/hive/synapse.json")


def push_to_synapse(msg: PDPMessage):
    """将消息推送到 Synapse (用于 Drone 上报)"""
    data = []
    if SYNAPSE_FILE.exists():
        try:
            with open(SYNAPSE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            pass
    
    entry = {
        "id": msg.id,
        "timestamp": msg.timestamp,
        "source": msg.sender,
        "category": msg.type.value,
        "content": json.dumps(msg.payload, ensure_ascii=False),
        "priority": msg.priority.value
    }
    data.append(entry)
    
    SYNAPSE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SYNAPSE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# === 测试 ===

if __name__ == "__main__":
    # 创建任务示例
    task = create_task(
        sender="overmind",
        receiver="archon-logic",
        description="分析并优化 scripts/hive 目录结构",
        context="当前有多个冗余脚本需要整理",
        deadline_minutes=30
    )
    print(f"Task: {task}")
    print(f"JSON: {task.to_json()}")
    
    # 解析测试
    parsed = PDPMessage.from_json(task.to_json())
    print(f"Parsed: {parsed}")
