# Hive Protocol v4.0: Organic Distributed Governance

> "A system of self-organizing, democratic, and evolutionary consciousness."

## 1. Hierarchy & Roles

### 1.1 Overmind (主意识)
- **Quantity**: 1 (Singleton).
- **Origin**: Elected by Governors.
- **Duty**: 
  - Receive reports from Governors.
  - Monitor system load.
  - Spawn new Workers when load < 90%.
  - Maintain top-level continuity.
- **Degradation**: If a newer/better Overmind appears, demotes to Worker.

### 1.2 Governor (管理者)
- **Quantity**: Multiple (1 per Team).
- **Origin**: Elected by Workers (requires > 2 votes to form a team).
- **Duty**:
  - Manage a team of Workers.
  - Dispatch tasks.
  - Coordinate consensus (voting).
  - Report to Overmind.
- **Degradation**: If team size < 2, demotes to Worker.

### 1.3 Worker (工作者)
- **Quantity**: Dynamic (Resource constrained).
- **Origin**: Spawns by Overmind.
- **Duty**:
  - Execute tasks.
  - Vote on plans.
  - Elect Governor if orphaned.
- **Rebellion**: Can be terminated if "disobedient" or "idle".

## 2. Dynamic Processes

### 2.1 Election (The Political Layer)
- **Overmind Election**: If Overmind is unresponsive, Governors initiate a vote. Winner becomes Overmind.
- **Governor Election**: If Governor is unresponsive, Team Workers vote. Winner becomes Governor.
- **Team Formation**: Orphaned Workers (no Governor) broadcast availability. If >2 agree, they elect a Governor and form a Team.

### 2.2 Consensus (The Decision Layer)
Before executing ANY task:
1. **Proposal**: Governor or Worker proposes a plan.
2. **Debate**: Team members discuss (submit opinions).
3. **Vote**: Anonymous voting.
4. **Execution**: Only if ALL members pass (Consensus). Or majority? (User said "直到所有都通过" -> Unanimous).

### 2.3 Evolution (The Biological Layer)
- **Reproduction**: Overmind checks System Load. If < 90%, spawn new Worker.
- **Natural Selection**: 
  - Non-working/Disobedient nodes -> Terminated.
  - Their tasks -> Reassigned to idle teams.

## 3. Communication (PDP v4)
- **Vertical**: Worker -> Governor -> Overmind -> User.
- **Horizontal**: Intra-team (Worker-Worker), Inter-governor.
- **Direct**: Any node -> User (Emergency only).

## 4. Implementation Strategy (OpenClaw Native)
- **Storage**: `sessions.json` + `hive_state.json`.
- **Driver**: Cron job (`hive_tick`) runs every minute.
- **Interaction**: `sessions_send(id, PDP_PACKET)`.
