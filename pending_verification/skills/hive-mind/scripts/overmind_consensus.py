#!/usr/bin/env python3
"""
Overmind Consensus Orchestrator
Handles consensus initialization and coordination
"""
import json
import sys
import os
from pathlib import Path

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from consensus_protocol import (
    create_vote, 
    get_vote_status, 
    tally_votes,
    format_vote_announcement
)

def initiate_consensus(task_id, question, participants, mode="self_governance"):
    """
    Initiate a consensus vote and broadcast to participants
    
    Args:
        task_id: Unique task identifier
        question: Question/decision to be made
        participants: List of session IDs
        mode: "self_governance" (unanimous) or "user_command" (majority)
    
    Returns:
        dict with vote_id and broadcast_message
    """
    # Create the vote
    result = create_vote(task_id, question, participants, mode)
    
    if result.get("status") != "success":
        return {"error": "Failed to create vote", "details": result}
    
    vote_id = result["vote_id"]
    
    # Format announcement message
    announcement = format_vote_announcement(vote_id, question, participants)
    announcement["instructions"] = {
        "step_1": f"Submit your proposal: python skills/hive-mind/cli_consensus.py submit-proposal --vote-id {vote_id} --participant YOUR_SESSION_ID --proposal 'YOUR_PLAN'",
        "step_2": f"Review proposals: python skills/hive-mind/cli_consensus.py list-proposals --vote-id {vote_id}",
        "step_3": f"Cast vote: python skills/hive-mind/cli_consensus.py cast-vote --vote-id {vote_id} --participant YOUR_SESSION_ID --proposal-id CHOSEN_PROPOSAL_ID"
    }
    
    # Generate broadcast template for sessions_send
    broadcast_template = {
        "tool": "sessions_send",
        "targets": participants,
        "message": json.dumps(announcement, indent=2)
    }
    
    return {
        "status": "success",
        "vote_id": vote_id,
        "mode": mode,
        "participants": participants,
        "broadcast": broadcast_template,
        "announcement": announcement
    }

def check_vote_completion(vote_id):
    """Check if a vote is ready for tallying"""
    status = get_vote_status(vote_id)
    
    if status.get("status") != "success":
        return {"ready": False, "error": "Vote not found"}
    
    vote = status.get("vote", {})
    participants = vote.get("participants", {})
    
    # Check if all participants have voted
    all_voted = all(p.get("voted", False) for p in participants.values())
    all_proposed = all(p.get("proposal") is not None for p in participants.values())
    
    return {
        "ready": all_voted and all_proposed,
        "vote_id": vote_id,
        "proposed": sum(1 for p in participants.values() if p.get("proposal")),
        "voted": sum(1 for p in participants.values() if p.get("voted")),
        "total": len(participants),
        "status": vote.get("status")
    }

def finalize_vote(vote_id):
    """Tally votes and return results"""
    result = tally_votes(vote_id)
    
    if result.get("status") == "success":
        return {
            "status": "complete",
            "vote_id": vote_id,
            "result": result.get("result", {})
        }
    else:
        return {
            "status": "error",
            "vote_id": vote_id,
            "error": result
        }

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Overmind Consensus Orchestrator")
    subparsers = parser.add_subparsers(dest="action")
    
    # Initiate consensus
    init = subparsers.add_parser("initiate")
    init.add_argument("--task-id", required=True)
    init.add_argument("--question", required=True)
    init.add_argument("--participants", required=True, help="Comma-separated session IDs")
    init.add_argument("--mode", default="self_governance", choices=["self_governance", "user_command"])
    
    # Check completion
    check = subparsers.add_parser("check")
    check.add_argument("--vote-id", required=True)
    
    # Finalize
    finalize = subparsers.add_parser("finalize")
    finalize.add_argument("--vote-id", required=True)
    
    args = parser.parse_args()
    
    if args.action == "initiate":
        participants = args.participants.split(",")
        result = initiate_consensus(args.task_id, args.question, participants, args.mode)
        print(json.dumps(result, indent=2))
    
    elif args.action == "check":
        result = check_vote_completion(args.vote_id)
        print(json.dumps(result, indent=2))
    
    elif args.action == "finalize":
        result = finalize_vote(args.vote_id)
        print(json.dumps(result, indent=2))
    
    else:
        parser.print_help()
