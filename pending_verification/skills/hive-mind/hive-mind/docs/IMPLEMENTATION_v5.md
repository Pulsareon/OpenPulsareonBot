# Protocol v5 Implementation Guide

## Architecture Overview

Protocol v5 implements consensus-driven governance using **OpenClaw Native Features**:

1. **Storage**: `data/hive/consensus_state.json` (managed via file I/O)
2. **Communication**: `sessions_send` for PDP messages between nodes
3. **Triggering**: Cron jobs for automatic vote tallying
4. **No Daemons**: All logic runs via CLI scripts called by sessions

## Components

### 1. Consensus Engine (`consensus_engine.py`)
Core state machine for managing votes:
- Create votes with two modes: `self_governance` (unanimous) or `user_command` (majority)
- Submit proposals
- Cast votes
- Tally results with different rules per mode
- Track completed votes

### 2. CLI Interface (`cli_consensus.py`)
Command-line tool for all consensus operations:
```bash
# Create vote
python skills/hive-mind/cli_consensus.py create-vote \
  --task-id "task123" \
  --question "What is the plan?" \
  --participants "node1,node2,node3" \
  --mode "self_governance"

# Submit proposal
python skills/hive-mind/cli_consensus.py submit-proposal \
  --vote-id "vote_1738957800_abc123" \
  --participant "node1" \
  --proposal "My plan is..."

# Cast vote
python skills/hive-mind/cli_consensus.py cast-vote \
  --vote-id "vote_1738957800_abc123" \
  --participant "node1" \
  --proposal-id "prop_xyz789"

# Tally votes
python skills/hive-mind/cli_consensus.py tally --vote-id "vote_1738957800_abc123"

# Check status
python skills/hive-mind/cli_consensus.py status
```

### 3. Protocol Helpers (`consensus_protocol.py`)
Python library for session integration:
- Helper functions for common operations
- PDP message formatters
- Easy integration with session scripts

### 4. Overmind Orchestrator (`scripts/overmind_consensus.py`)
High-level orchestration for the Overmind:
```bash
# Start consensus
python skills/hive-mind/scripts/overmind_consensus.py initiate \
  --task-id "elect_governor" \
  --question "Who should be Governor?" \
  --participants "node1,node2,node3" \
  --mode "self_governance"

# Check if vote is ready
python skills/hive-mind/scripts/overmind_consensus.py check \
  --vote-id "vote_1738957800_abc123"

# Finalize vote
python skills/hive-mind/scripts/overmind_consensus.py finalize \
  --vote-id "vote_1738957800_abc123"
```

### 5. Cron Tally Job (`scripts/consensus_tally_cron.py`)
Automatic vote tallying (runs every 5 minutes):
```bash
# Setup cron job (run once in OpenClaw)
cron add --schedule "*/5 * * * *" \
  --task "python E:/PulsareonThinker/skills/hive-mind/scripts/consensus_tally_cron.py"
```

## Workflow Examples

### Self-Governance: Elect New Governor

```
1. Overmind initiates vote:
   python scripts/overmind_consensus.py initiate \
     --task-id "election_2026_02_08" \
     --question "Elect new Governor from candidates" \
     --participants "node1,node2,node3,node4" \
     --mode "self_governance"

2. Overmind broadcasts via sessions_send:
   sessions_send(target="node1", message=<vote_announcement>)
   sessions_send(target="node2", message=<vote_announcement>)
   ...

3. Each node submits proposal:
   Node1: python cli_consensus.py submit-proposal --vote-id <ID> --participant node1 --proposal "I nominate Node2"
   Node2: python cli_consensus.py submit-proposal --vote-id <ID> --participant node2 --proposal "I nominate Node3"
   ...

4. Each node reviews and votes:
   Node1: python cli_consensus.py cast-vote --vote-id <ID> --participant node1 --proposal-id <Node3's proposal>
   Node2: python cli_consensus.py cast-vote --vote-id <ID> --participant node2 --proposal-id <Node3's proposal>
   ...

5. Cron job automatically tallies when all votes in OR timeout occurs

6. Result:
   - If unanimous: Node3 elected
   - If not unanimous: Vote fails, negotiation required
```

### User Command: Optimization Suggestion

```
1. User assigns task to Overmind: "Optimize memory usage"

2. Overmind creates optional consensus for ideas:
   python scripts/overmind_consensus.py initiate \
     --task-id "optimize_memory_2026" \
     --question "Best approach to optimize memory?" \
     --participants "governor1,governor2" \
     --mode "user_command"

3. Governors submit proposals (same as above)

4. Governors vote (same as above)

5. Result:
   - Majority wins (doesn't require unanimity)
   - Overmind reviews winning proposal
   - Overmind makes final decision and executes
```

## Integration with Sessions

### For Hive Nodes (Workers/Governors)
Add to session context:
```
Read skills/hive-mind/assets/CONSENSUS_GUIDE.md for consensus participation.
```

### For Overmind
Add to session context:
```
You can initiate consensus using:
python skills/hive-mind/scripts/overmind_consensus.py

For self-governance (elections, protocol changes): --mode self_governance (requires unanimity)
For user tasks (optimization): --mode user_command (majority wins, you decide final plan)
```

## State Storage

All state is stored in `data/hive/consensus_state.json`:
```json
{
  "version": "v5.0",
  "active_votes": {
    "vote_123": {
      "id": "vote_123",
      "task_id": "task_456",
      "mode": "self_governance",
      "question": "...",
      "participants": {...},
      "proposals": [...],
      "votes": {...},
      "status": "active"
    }
  },
  "completed_votes": {...},
  "participants": {...},
  "rules": {
    "unanimity_required": true,
    "timeout_minutes": 30,
    "min_participation": 0.8
  }
}
```

## Monitoring

Check consensus status:
```bash
# All active votes
python skills/hive-mind/cli_consensus.py status

# Specific vote
python skills/hive-mind/cli_consensus.py status --vote-id <ID>

# List proposals
python skills/hive-mind/cli_consensus.py list-proposals --vote-id <ID>
```

## Troubleshooting

**Vote stuck?**
- Check participation: `python cli_consensus.py status --vote-id <ID>`
- Manually tally: `python cli_consensus.py tally --vote-id <ID>`

**Node not participating?**
- Protocol v5 rule: Non-participation = Disobedience
- Overmind should terminate non-responsive nodes

**Consensus failing repeatedly?**
- Self-governance: Requires unanimity. Nodes must negotiate.
- User command: Use majority result, Overmind decides.

## Security

- All votes are logged in consensus_state.json (transparency)
- Proposals are timestamped and attributed
- No vote modification after submission
- Expired votes automatically fail
