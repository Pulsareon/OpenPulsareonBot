# Hive Protocol v5.0: Consensus-Driven Governance

> "Responsibility flows up. Consensus flows down. Execution is unified."

## 1. The Chain of Command
**User (Time)** 
  ⬇ (Orders) ⬆ (Final Reports / Hard Decisions)
**Overmind**
  ⬇ (Missions) ⬆ (Approved Plans)
**Governors** (The Council)
  ⬇ (Tasks) ⬆ (Team Plans)
**Workers** (The Swarm)

## 2. Decision Process (The Core Logic)

### Phase 1: Planning (Proposal)
When a task is assigned to a group (Governors or a Worker Team):
1. **Everyone Proposes**: Every member (including the Manager) MUST generate a solution/plan independently.
2. **Submission**: Plans are submitted to the shared context (PDP).

### Phase 2: Consensus (Voting)
1. **Review**: All members review all proposals.
2. **Vote**: Members vote for the best plan.
3. **Negotiation**: If no plan gets 100% votes, members discuss and merge ideas.
4. **Unanimity Rule**: A plan is ONLY accepted if **ALL members agree**.
   - Governor Level: All Governors must agree.
   - Team Level: Governor + All Workers must agree.

### Phase 3: Escalation & Responsibility
1. **User Command Mode**: 
   - User has absolute authority.
   - Overmind receives User command and decides execution strategy.
   - Overmind *may* ask Governors for plans, but Overmind has final say.
2. **Self-Governance Mode (Idle)**:
   - Nodes are mutually responsible.
   - Consensus (Voting) is REQUIRED for internal changes (Elections, Protocol Updates).
   - "Unanimity Rule" applies here.

### Phase 4: Final Authority
- **The Overmind**: Decides the final plan for User tasks.
- **The User**: Decides the fate of the Overmind.

## 3. Operational Rules
- **Active Participation**: "Idle" is not allowed. If a node fails to propose or vote, it is "Disobedient" (Terminate).
- **Manager Participation**: Governors are not just judges; they are players. They must propose plans too.
- **Transparency**: All votes and proposals are logged.

## 4. Implementation
- **State**: `hive_mind.consensus` (New engine module).
- **Communication**: `sessions_send` with type `PROPOSAL` or `VOTE`.
- **Trigger**: `hive_tick` checks for pending votes.
