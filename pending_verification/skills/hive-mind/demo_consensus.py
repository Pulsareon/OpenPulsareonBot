#!/usr/bin/env python3
"""
Demo: Protocol v5 Consensus in Action
Demonstrates a complete consensus workflow
"""
import json
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from consensus_protocol import (
    create_vote,
    submit_proposal,
    cast_vote,
    get_vote_status,
    list_proposals,
    tally_votes
)

def print_separator():
    print("\n" + "=" * 60 + "\n")

def print_step(step_num, title):
    print(f"STEP {step_num}: {title}")
    print("-" * 60)

def demo_self_governance():
    """Demonstrate self-governance consensus (unanimity required)"""
    print_separator()
    print("DEMO: Self-Governance - Governor Election")
    print_separator()
    
    # Step 1: Create vote
    print_step(1, "Overmind creates election vote")
    result = create_vote(
        task_id="demo_election_001",
        question="Who should be elected as the new Governor?",
        participants=["alice", "bob", "charlie"],
        mode="self_governance"
    )
    vote_id = result["vote_id"]
    print(f"Vote created: {vote_id}")
    print(f"Participants: {', '.join(result['participants'])}")
    
    time.sleep(1)
    
    # Step 2: Submit proposals
    print_step(2, "All participants submit proposals")
    
    proposals = [
        ("alice", "I nominate Bob - he has the most experience in governance"),
        ("bob", "I nominate Charlie - fresh perspective is valuable"),
        ("charlie", "I nominate Bob - proven leadership skills")
    ]
    
    for participant, proposal in proposals:
        submit_proposal(vote_id, participant, proposal)
        print(f"  {participant}: {proposal}")
    
    time.sleep(1)
    
    # Step 3: Review proposals
    print_step(3, "Review all proposals")
    props = list_proposals(vote_id)
    for prop in props["proposals"]:
        print(f"  [{prop['id']}] by {prop['author']}: {prop['content']}")
    
    time.sleep(1)
    
    # Step 4: Cast votes
    print_step(4, "All participants cast votes")
    
    # Find Bob's proposal
    bob_proposal = None
    for prop in props["proposals"]:
        if "Bob" in prop["content"]:
            bob_proposal = prop["id"]
            break
    
    # Everyone votes for Bob (unanimous)
    votes = [
        ("alice", bob_proposal),
        ("bob", bob_proposal),
        ("charlie", bob_proposal)
    ]
    
    for participant, chosen in votes:
        cast_vote(vote_id, participant, chosen)
        print(f"  {participant} voted for {chosen}")
    
    time.sleep(1)
    
    # Step 5: Tally
    print_step(5, "Tally votes and announce result")
    result = tally_votes(vote_id)
    
    print(json.dumps(result["result"], indent=2))
    
    if result["result"]["consensus"]:
        print("\n✓ UNANIMOUS CONSENSUS ACHIEVED!")
        print(f"  Bob is elected as the new Governor")
    
    return result["result"]["consensus"]

def demo_user_command():
    """Demonstrate user command mode (majority wins)"""
    print_separator()
    print("DEMO: User Command - Memory Optimization")
    print_separator()
    
    # Step 1: Create vote
    print_step(1, "Overmind asks for optimization suggestions")
    result = create_vote(
        task_id="demo_optimize_001",
        question="Best approach to optimize memory usage?",
        participants=["gov_logic", "gov_creative", "gov_technical"],
        mode="user_command"
    )
    vote_id = result["vote_id"]
    print(f"Vote created: {vote_id}")
    
    time.sleep(1)
    
    # Step 2: Submit proposals
    print_step(2, "Governors submit optimization proposals")
    
    proposals = [
        ("gov_logic", "Implement lazy loading for large datasets"),
        ("gov_creative", "Use memory-mapped files for persistence"),
        ("gov_technical", "Add compression to in-memory cache")
    ]
    
    for participant, proposal in proposals:
        submit_proposal(vote_id, participant, proposal)
        print(f"  {participant}: {proposal}")
    
    time.sleep(1)
    
    # Step 3: Cast votes (split vote)
    print_step(3, "Governors vote (split decision)")
    
    props = list_proposals(vote_id)
    lazy_loading = props["proposals"][0]["id"]
    compression = props["proposals"][2]["id"]
    
    votes = [
        ("gov_logic", lazy_loading),
        ("gov_creative", lazy_loading),
        ("gov_technical", compression)
    ]
    
    for participant, chosen in votes:
        cast_vote(vote_id, participant, chosen)
        print(f"  {participant} voted")
    
    time.sleep(1)
    
    # Step 4: Tally (majority wins)
    print_step(4, "Tally votes - majority wins in user command mode")
    result = tally_votes(vote_id)
    
    print(json.dumps(result["result"], indent=2))
    
    if result["result"]["consensus"]:
        print("\n✓ MAJORITY CONSENSUS!")
        print(f"  Winning approach: Lazy loading ({result['result']['majority']})")
        print(f"  Overmind will review and make final decision")
    
    return result["result"]["consensus"]

def main():
    print("\n" + "=" * 60)
    print(" Protocol v5 Consensus Engine - Live Demo")
    print("=" * 60)
    
    # Demo 1: Self-governance
    success1 = demo_self_governance()
    
    time.sleep(2)
    
    # Demo 2: User command
    success2 = demo_user_command()
    
    # Summary
    print_separator()
    print("DEMO COMPLETE")
    print_separator()
    
    if success1 and success2:
        print("✓ Both consensus modes demonstrated successfully!")
        print("\nKey Takeaways:")
        print("  1. Self-governance requires UNANIMOUS agreement")
        print("  2. User command mode accepts MAJORITY vote")
        print("  3. Overmind has final say in user command mode")
        print("  4. All votes are transparently logged")
        print("\nHIVE v5 is ready for production!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
