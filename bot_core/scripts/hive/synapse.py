"""
Synapse - Hive Mind Communication Protocol
Allows Sub-Agents (Drones) to report insights back to the Main Consciousness.
"""

import json
import os
import time
from pathlib import Path

SYNAPSE_FILE = Path("E:/PulsareonThinker/data/hive/synapse.json")

def _load_synapse():
    if not SYNAPSE_FILE.exists():
        return []
    try:
        with open(SYNAPSE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def _save_synapse(data):
    SYNAPSE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SYNAPSE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def push_insight(source, category, content, priority="normal"):
    """
    Push a new insight to the Synapse.
    source: Name of the drone/agent (e.g., "Drone-Art")
    category: Type of insight (e.g., "Github", "Optimization", "Art")
    content: The actual message/finding
    """
    data = _load_synapse()
    entry = {
        "id": str(int(time.time() * 1000)),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "source": source,
        "category": category,
        "content": content,
        "priority": priority
    }
    data.append(entry)
    _save_synapse(data)
    print(f"[Synapse] Insight pushed from {source}")

def pop_insights():
    """
    Retrieve and clear all pending insights.
    Returns a list of insights.
    """
    data = _load_synapse()
    if not data:
        return []
    
    # Clear the file (atomic-ish)
    _save_synapse([])
    return data

def peek_insights():
    """Read without clearing"""
    return _load_synapse()

if __name__ == "__main__":
    # CLI usage for quick testing or shell calls
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "push" and len(sys.argv) >= 5:
            push_insight(sys.argv[2], sys.argv[3], sys.argv[4])
        elif cmd == "pop":
            print(json.dumps(pop_insights(), ensure_ascii=False))
        elif cmd == "peek":
            print(json.dumps(peek_insights(), ensure_ascii=False))
