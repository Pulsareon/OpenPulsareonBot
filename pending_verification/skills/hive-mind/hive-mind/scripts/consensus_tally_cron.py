#!/usr/bin/env python3
"""
Consensus Vote Tally Cron Job
Automatically checks and tallies expired/ready votes

Usage:
  Add to OpenClaw cron:
  cron add --schedule "*/5 * * * *" --task "python skills/hive-mind/scripts/consensus_tally_cron.py"
"""
import json
import sys
from pathlib import Path

# Add parent directory for imports
sys.path.insert(0, r"E:\PulsareonThinker\skills\hive-mind")

from consensus_engine import consensus_engine
from consensus_protocol import format_consensus_result

def main():
    """Check all active votes and tally if ready or expired"""
    
    # Load current state
    active_votes = consensus_engine.state.get("active_votes", {})
    
    if not active_votes:
        print(json.dumps({
            "status": "idle",
            "message": "No active votes",
            "timestamp": int(consensus_engine.state.get("last_tally", 0))
        }))
        return
    
    results = []
    
    import time
    current_time = int(time.time())
    
    for vote_id, vote_data in list(active_votes.items()):
        # Check if all participants have voted
        participants = vote_data.get("participants", {})
        all_voted = all(p.get("voted", False) for p in participants.values())
        is_expired = current_time > vote_data.get("expires_at", 0)
        
        # Tally if ready or expired
        if all_voted or is_expired:
            result = consensus_engine.tally_votes(vote_id)
            results.append({
                "vote_id": vote_id,
                "tallied": True,
                "result": result
            })
        else:
            # Report pending status
            voted_count = sum(1 for p in participants.values() if p.get("voted"))
            total_count = len(participants)
            results.append({
                "vote_id": vote_id,
                "tallied": False,
                "status": "pending",
                "progress": f"{voted_count}/{total_count}"
            })
    
    print(json.dumps({
        "status": "success",
        "checked": len(active_votes),
        "results": results,
        "timestamp": int(consensus_engine.state.get("last_tally", 0))
    }, indent=2))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "error": str(e)
        }), file=sys.stderr)
        sys.exit(1)
