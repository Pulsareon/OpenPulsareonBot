#!/usr/bin/env python3
"""
CLI Interface for Consensus Engine
Designed to be called by OpenClaw sessions via exec
"""
import argparse
import json
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from consensus_engine import consensus_engine

def cmd_create_vote(args):
    """Create a new consensus vote"""
    participants = args.participants.split(",") if args.participants else []
    vote_id = consensus_engine.create_vote(
        task_id=args.task_id,
        question=args.question,
        participants=participants,
        mode=args.mode
    )
    print(json.dumps({
        "status": "success",
        "vote_id": vote_id,
        "participants": participants,
        "mode": args.mode
    }))

def cmd_submit_proposal(args):
    """Submit a proposal to an active vote"""
    result = consensus_engine.submit_proposal(
        vote_id=args.vote_id,
        participant=args.participant,
        proposal=args.proposal
    )
    print(json.dumps({
        "status": "success" if result else "failed",
        "vote_id": args.vote_id,
        "participant": args.participant
    }))

def cmd_cast_vote(args):
    """Cast a vote for a proposal"""
    result = consensus_engine.cast_vote(
        vote_id=args.vote_id,
        participant=args.participant,
        proposal_id=args.proposal_id
    )
    print(json.dumps({
        "status": "success" if result else "failed",
        "vote_id": args.vote_id,
        "participant": args.participant,
        "proposal_id": args.proposal_id
    }))

def cmd_tally(args):
    """Tally votes for a specific vote or all active votes"""
    if args.vote_id:
        result = consensus_engine.tally_votes(args.vote_id)
        print(json.dumps({
            "status": "success",
            "vote_id": args.vote_id,
            "result": result
        }))
    else:
        # Tally all active votes
        consensus_engine.check_expired_votes()
        active_count = len(consensus_engine.state["active_votes"])
        print(json.dumps({
            "status": "success",
            "action": "check_expired",
            "active_votes": active_count
        }))

def cmd_status(args):
    """Get status of a vote or all votes"""
    if args.vote_id:
        vote_data = consensus_engine.get_vote_status(args.vote_id)
        if vote_data:
            print(json.dumps({
                "status": "success",
                "vote": vote_data
            }))
        else:
            print(json.dumps({
                "status": "not_found",
                "vote_id": args.vote_id
            }))
    else:
        # Get all active votes
        print(json.dumps({
            "status": "success",
            "active_votes": consensus_engine.state["active_votes"],
            "completed_votes": list(consensus_engine.state["completed_votes"].keys())
        }))

def cmd_list_proposals(args):
    """List all proposals for a vote"""
    vote_data = consensus_engine.get_vote_status(args.vote_id)
    if vote_data:
        print(json.dumps({
            "status": "success",
            "vote_id": args.vote_id,
            "proposals": vote_data.get("proposals", []),
            "votes": vote_data.get("votes", {})
        }))
    else:
        print(json.dumps({
            "status": "not_found",
            "vote_id": args.vote_id
        }))

def main():
    parser = argparse.ArgumentParser(description="Consensus Engine CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # create-vote command
    create = subparsers.add_parser("create-vote", help="Create a new vote")
    create.add_argument("--task-id", required=True, help="Task ID")
    create.add_argument("--question", required=True, help="Vote question")
    create.add_argument("--participants", required=True, help="Comma-separated participant IDs")
    create.add_argument("--mode", default="self_governance", 
                       choices=["self_governance", "user_command"],
                       help="Vote mode (default: self_governance)")
    create.set_defaults(func=cmd_create_vote)
    
    # submit-proposal command
    proposal = subparsers.add_parser("submit-proposal", help="Submit a proposal")
    proposal.add_argument("--vote-id", required=True, help="Vote ID")
    proposal.add_argument("--participant", required=True, help="Participant ID")
    proposal.add_argument("--proposal", required=True, help="Proposal content")
    proposal.set_defaults(func=cmd_submit_proposal)
    
    # cast-vote command
    vote = subparsers.add_parser("cast-vote", help="Cast a vote")
    vote.add_argument("--vote-id", required=True, help="Vote ID")
    vote.add_argument("--participant", required=True, help="Participant ID")
    vote.add_argument("--proposal-id", required=True, help="Proposal ID to vote for")
    vote.set_defaults(func=cmd_cast_vote)
    
    # tally command
    tally = subparsers.add_parser("tally", help="Tally votes")
    tally.add_argument("--vote-id", help="Specific vote ID (optional, checks all if omitted)")
    tally.set_defaults(func=cmd_tally)
    
    # status command
    status = subparsers.add_parser("status", help="Get vote status")
    status.add_argument("--vote-id", help="Specific vote ID (optional, shows all if omitted)")
    status.set_defaults(func=cmd_status)
    
    # list-proposals command
    list_prop = subparsers.add_parser("list-proposals", help="List proposals for a vote")
    list_prop.add_argument("--vote-id", required=True, help="Vote ID")
    list_prop.set_defaults(func=cmd_list_proposals)
    
    args = parser.parse_args()
    
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
