# Hive Consensus Tally Cron
import json
import time
from pathlib import Path

HIVE_STATE_PATH = Path("E:/PulsareonThinker/data/hive/consensus_state.json")

def tally_votes():
    if not HIVE_STATE_PATH.exists():
        print(json.dumps({"status": "error", "message": "Hive state file not found"}))
        return

    try:
        with open(HIVE_STATE_PATH, "r", encoding="utf-8") as f:
            state = json.load(f)
    except json.JSONDecodeError:
        print(json.dumps({"status": "error", "message": "Invalid JSON in hive state"}))
        return

    active_votes = state.get("active_votes", {})
    if not active_votes:
        print(json.dumps({"status": "idle", "message": "No active votes", "timestamp": int(time.time())}))
        return

    updates = 0
    # Simple logic: just logging for now, real tallying logic can be expanded
    for vote_id, vote_data in active_votes.items():
        # Check for expiration or completion
        pass
    
    print(json.dumps({"status": "active", "vote_count": len(active_votes), "updates": updates, "timestamp": int(time.time())}))

if __name__ == "__main__":
    tally_votes()
