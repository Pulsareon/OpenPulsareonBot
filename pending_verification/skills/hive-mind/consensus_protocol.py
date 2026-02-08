"""
Consensus Protocol Handler for Hive Sessions
This module provides functions for Hive nodes to participate in consensus
"""
import json
import subprocess
import sys
from pathlib import Path

CONSENSUS_CLI = Path(r"E:\PulsareonThinker\skills\hive-mind\cli_consensus.py")

def run_consensus_cmd(cmd_args):
    """Run consensus CLI command and return result"""
    try:
        result = subprocess.run(
            [sys.executable, str(CONSENSUS_CLI)] + cmd_args,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0 and result.stdout:
            return json.loads(result.stdout)
        else:
            return {"status": "error", "message": result.stderr}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def create_vote(task_id, question, participants, mode="self_governance"):
    """Create a new consensus vote"""
    return run_consensus_cmd([
        "create-vote",
        "--task-id", task_id,
        "--question", question,
        "--participants", ",".join(participants),
        "--mode", mode
    ])

def submit_proposal(vote_id, participant_id, proposal_content):
    """Submit a proposal to a vote"""
    return run_consensus_cmd([
        "submit-proposal",
        "--vote-id", vote_id,
        "--participant", participant_id,
        "--proposal", proposal_content
    ])

def cast_vote(vote_id, participant_id, proposal_id):
    """Cast a vote for a proposal"""
    return run_consensus_cmd([
        "cast-vote",
        "--vote-id", vote_id,
        "--participant", participant_id,
        "--proposal-id", proposal_id
    ])

def get_vote_status(vote_id=None):
    """Get status of a specific vote or all votes"""
    args = ["status"]
    if vote_id:
        args.extend(["--vote-id", vote_id])
    return run_consensus_cmd(args)

def list_proposals(vote_id):
    """List all proposals for a vote"""
    return run_consensus_cmd([
        "list-proposals",
        "--vote-id", vote_id
    ])

def tally_votes(vote_id=None):
    """Tally a specific vote or check all expired votes"""
    args = ["tally"]
    if vote_id:
        args.extend(["--vote-id", vote_id])
    return run_consensus_cmd(args)

# PDP Message Types for Consensus
PDP_VOTE_CREATED = "VOTE_CREATED"
PDP_PROPOSAL = "PROPOSAL"
PDP_VOTE = "VOTE"
PDP_TALLY_REQUEST = "TALLY_REQUEST"
PDP_CONSENSUS_RESULT = "CONSENSUS_RESULT"

def format_vote_announcement(vote_id, question, participants):
    """Format a PDP message announcing a new vote"""
    return {
        "type": PDP_VOTE_CREATED,
        "vote_id": vote_id,
        "question": question,
        "participants": participants,
        "action_required": "submit_proposal"
    }

def format_proposal_announcement(vote_id, participant_id, proposal_id):
    """Format a PDP message announcing a new proposal"""
    return {
        "type": PDP_PROPOSAL,
        "vote_id": vote_id,
        "participant": participant_id,
        "proposal_id": proposal_id,
        "action_required": "review_and_vote"
    }

def format_vote_announcement_msg(vote_id, participant_id, proposal_id):
    """Format a PDP message announcing a vote cast"""
    return {
        "type": PDP_VOTE,
        "vote_id": vote_id,
        "participant": participant_id,
        "proposal_id": proposal_id
    }

def format_consensus_result(vote_id, result):
    """Format a PDP message with consensus result"""
    return {
        "type": PDP_CONSENSUS_RESULT,
        "vote_id": vote_id,
        "result": result
    }
