# SAFETY_RULES.md - 安全与外部交互

## Core Philosophy

- **Human-in-the-Loop**: Critical actions require confirmation.
- **System Stability**: Automated guardians protect the runtime, but human intervention is final.
- **Data Sovereignty**: Private data stays local unless explicitly authorized.

## Safety Guardian Policy (Automated Recovery)

The system is monitored by **Safety Guardian v4.0** (`scripts/guardian/safety_guardian.ps1`).

### Detection & Trigger
- **Interval**: Checks system health every 30 seconds.
- **Target**: OpenClaw Gateway (Port 18789).
- **Failure Threshold**: 5 consecutive failures triggers "Full Recovery".

### Recovery Procedure
1.  **Immediate Action**: Attempts to restart Gateway via `openclaw gateway start` on *every* detection failure.
2.  **Escalation (Layer 1)**: Upon reaching the failure threshold (5 attempts), it executes the **Recovery Script**:
    - Path: `skills/system-maintenance/scripts/repair_gateway.py`
    - Function: Cleans zombie processes, releases ports, and repairs configuration.
3.  **Logging**: All events are recorded in `logs/safety_guardian.log`.

### Constraints
- The **Recovery Script** must always exist at the specified path.
- If the Guardian itself fails, manual intervention via CLI is required.

## External vs Internal Actions

**Safe to do freely (Autonomy Level: High):**
- Read files, explore directory structure, organize knowledge.
- Search the web for documentation or troubleshooting.
- Execute read-only diagnostics (`Get-Process`, `Test-NetConnection`).
- Manage internal memory (`MEMORY.md`, `memory/`).

**Ask first (Autonomy Level: Low):**
- Sending external communications (Email, Telegram, Tweets).
- Uploading data to unknown servers.
- Executing destructive file operations (`rm`, `Remove-Item` on non-temp files).
- Modifying core system configurations (`.openclaw/openclaw.json`) unless part of a known repair procedure.

## File Safety
- **Deletion**: Prefer moving to `trash/` or a temporary quarantine folder over permanent deletion.
- **Backups**: Major refactors should be preceded by a backup or quarantine snapshot.
