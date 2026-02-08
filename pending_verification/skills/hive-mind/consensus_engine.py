"""
Consensus Engine for Protocol v5 Implementation
Native OpenClaw integration for consensus-driven governance
"""
import json
import time
import uuid
from pathlib import Path
from typing import Dict, List, Optional

# Constants
CONSENSUS_FILE = Path(r"E:\PulsareonThinker\data\hive\consensus_state.json")
CONSENSUS_DIR = Path(r"E:\PulsareonThinker\data\hive\consensus")

class ConsensusEngine:
    """
    Implements Protocol v5 Consensus-Driven Governance using OpenClaw native features
    """
    
    def __init__(self):
        self.state = self._load_state()
        
    def _load_state(self) -> Dict:
        """Load consensus state from file"""
        if CONSENSUS_FILE.exists():
            try:
                with open(CONSENSUS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        
        # Default state
        return {
            "version": "v5.0",
            "active_votes": {},
            "completed_votes": {},
            "participants": {},
            "last_tally": int(time.time()),
            "rules": {
                "unanimity_required": True,
                "timeout_minutes": 30,
                "min_participation": 0.8  # 80% of nodes must participate
            }
        }
    
    def _save_state(self):
        """Save consensus state to file"""
        CONSENSUS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CONSENSUS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2)
    
    def create_vote(self, task_id: str, question: str, participants: List[str], mode: str = "self_governance") -> str:
        """Create a new consensus vote"""
        vote_id = f"vote_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        
        vote_data = {
            "id": vote_id,
            "task_id": task_id,
            "question": question,
            "mode": mode,  # "self_governance" (mandatory) or "user_command" (optional)
            "created_at": int(time.time()),
            "expires_at": int(time.time()) + (self.state["rules"]["timeout_minutes"] * 60),
            "participants": {p: {"voted": False, "vote": None, "proposal": None} for p in participants},
            "proposals": [],
            "votes": {},
            "status": "active",
            "result": None
        }
        
        self.state["active_votes"][vote_id] = vote_data
        self._save_state()
        
        return vote_id
    
    def submit_proposal(self, vote_id: str, participant: str, proposal: str) -> bool:
        """Submit a proposal for voting"""
        if vote_id not in self.state["active_votes"]:
            return False
        
        vote = self.state["active_votes"][vote_id]
        
        if participant not in vote["participants"]:
            return False
        
        # Store proposal
        proposal_id = f"prop_{uuid.uuid4().hex[:8]}"
        vote["proposals"].append({
            "id": proposal_id,
            "author": participant,
            "content": proposal,
            "timestamp": int(time.time())
        })
        
        # Mark participant as having proposed
        vote["participants"][participant]["proposal"] = proposal_id
        
        self._save_state()
        return True
    
    def cast_vote(self, vote_id: str, participant: str, proposal_id: str) -> bool:
        """Cast a vote for a specific proposal"""
        if vote_id not in self.state["active_votes"]:
            return False
        
        vote = self.state["active_votes"][vote_id]
        
        if participant not in vote["participants"]:
            return False
        
        # Verify proposal exists
        proposal_exists = any(p["id"] == proposal_id for p in vote["proposals"])
        if not proposal_exists:
            return False
        
        # Record vote
        vote["participants"][participant]["voted"] = True
        vote["participants"][participant]["vote"] = proposal_id
        
        # Update vote counts
        if proposal_id not in vote["votes"]:
            vote["votes"][proposal_id] = 0
        vote["votes"][proposal_id] += 1
        
        self._save_state()
        return True
    
    def tally_votes(self, vote_id: str) -> Optional[Dict]:
        """Tally votes and determine consensus result"""
        if vote_id not in self.state["active_votes"]:
            return None
        
        vote = self.state["active_votes"][vote_id]
        
        # Check timeout
        if int(time.time()) > vote["expires_at"]:
            vote["status"] = "timeout"
            vote["result"] = {"consensus": False, "reason": "Vote timeout"}
            self._finalize_vote(vote_id)
            return vote["result"]
        
        # Check participation
        total_participants = len(vote["participants"])
        voted_count = sum(1 for p in vote["participants"].values() if p["voted"])
        participation_rate = voted_count / total_participants
        
        if participation_rate < self.state["rules"]["min_participation"]:
            vote["status"] = "failed"
            vote["result"] = {
                "consensus": False, 
                "reason": f"Insufficient participation ({voted_count}/{total_participants})"
            }
            self._finalize_vote(vote_id)
            return vote["result"]
        
        votes_by_proposal = {}
        for proposal in vote["proposals"]:
            proposal_id = proposal["id"]
            votes_by_proposal[proposal_id] = vote["votes"].get(proposal_id, 0)
        
        # Different logic based on vote mode
        if vote["mode"] == "self_governance":
            # Self-governance mode: Unanimity is REQUIRED
            winning_proposal = None
            
            # Find proposal with unanimous support
            for proposal_id, vote_count in votes_by_proposal.items():
                if vote_count == total_participants:
                    winning_proposal = proposal_id
                    break
            
            if winning_proposal:
                vote["status"] = "consensus"
                vote["result"] = {
                    "consensus": True,
                    "winning_proposal": winning_proposal,
                    "votes": votes_by_proposal,
                    "participation": f"{voted_count}/{total_participants}"
                }
            else:
                vote["status"] = "failed"
                vote["result"] = {
                    "consensus": False,
                    "reason": "No unanimous agreement (self-governance requires unanimity)",
                    "votes": votes_by_proposal,
                    "participation": f"{voted_count}/{total_participants}"
                }
        
        else:  # user_command mode
            # User command mode: Consensus is optional, majority wins
            if votes_by_proposal:
                winning_proposal = max(votes_by_proposal.items(), key=lambda x: x[1])[0]
                max_votes = votes_by_proposal[winning_proposal]
                
                vote["status"] = "majority"
                vote["result"] = {
                    "consensus": True,
                    "winning_proposal": winning_proposal,
                    "votes": votes_by_proposal,
                    "participation": f"{voted_count}/{total_participants}",
                    "majority": f"{max_votes}/{total_participants}"
                }
            else:
                vote["status"] = "failed"
                vote["result"] = {
                    "consensus": False,
                    "reason": "No votes cast",
                    "participation": f"{voted_count}/{total_participants}"
                }
        
        self._finalize_vote(vote_id)
        return vote["result"]
    
    def _finalize_vote(self, vote_id: str):
        """Move vote from active to completed"""
        if vote_id in self.state["active_votes"]:
            vote_data = self.state["active_votes"].pop(vote_id)
            self.state["completed_votes"][vote_id] = vote_data
            self.state["last_tally"] = int(time.time())
            self._save_state()
    
    def get_vote_status(self, vote_id: str) -> Optional[Dict]:
        """Get current vote status"""
        if vote_id in self.state["active_votes"]:
            return self.state["active_votes"][vote_id]
        elif vote_id in self.state["completed_votes"]:
            return self.state["completed_votes"][vote_id]
        return None
    
    def check_expired_votes(self):
        """Check and process expired votes"""
        current_time = int(time.time())
        expired_votes = []
        
        for vote_id, vote_data in self.state["active_votes"].items():
            if current_time > vote_data["expires_at"]:
                expired_votes.append(vote_id)
        
        for vote_id in expired_votes:
            self.tally_votes(vote_id)

# Singleton instance for easy access
consensus_engine = ConsensusEngine()