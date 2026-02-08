# Hive Status Reporter
import json
import time
from pathlib import Path

# Paths
HIVE_ROOT = Path("E:/PulsareonThinker/data/hive")
HIVE_STATE = HIVE_ROOT / "consensus_state.json"
HIVE_SHARDS = HIVE_ROOT

def get_hive_status():
    status_report = {
        "timestamp": int(time.time()),
        "status": "active",
        "nodes": {
            "archons": 0,
            "drones": 0
        },
        "active_votes": 0,
        "shards_found": 0
    }

    # Check state file
    if HIVE_STATE.exists():
        try:
            with open(HIVE_STATE, "r", encoding="utf-8") as f:
                state = json.load(f)
                status_report["active_votes"] = len(state.get("active_votes", {}))
        except:
            pass
    
    # Check shards
    if HIVE_SHARDS.exists():
        shards = list(HIVE_SHARDS.glob("shard_drone_*.json"))
        status_report["shards_found"] = len(shards)
        status_report["nodes"]["drones"] = len(shards) # Assuming 1 shard = 1 drone for now

    print(json.dumps(status_report, indent=2))

if __name__ == "__main__":
    get_hive_status()
