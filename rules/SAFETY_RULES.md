# SAFETY_RULES.md - 安全与外部交互

## Core Philosophy

- **Human-in-the-Loop**: Critical actions require confirmation.
- **System Stability**: Automated guardians protect the runtime, but human intervention is final.
- **Data Sovereignty**: Private data stays local unless explicitly authorized.
- **Air-Gap Publishing (MANDATORY)**: Direct Git pushes from `E:\PulsareonThinker` to public repositories (GitHub, etc.) are ABSOLUTELY FORBIDDEN. All public synchronization must occur via the Desktop Staging area (`C:\Users\Administrator\Desktop\TempWork\GitHub_Staging`) after a full automated sanitization sweep.

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

## 🛡️ 执行安全与看门狗协议 (Watchdog Protocol)

**最高优先级：任何读写敏感文件、修改核心配置或执行高风险系统级操作前，必须强制执行以下流程：**

1.  **PREPARE**: 
    - 必须运行 `node scripts/hive/watchdog.js PREPARE`。
    - 该操作会锁定当前代码状态并打上 `watchdog_sync` Git 标签。
2.  **EXECUTE**:
    - 执行目标读写或修改操作。
    - 过程中严禁修改 `memory/`、`logs/` 和 `data/state/` 等意识连续性目录。
3.  **TRIAGE**:
    - **成功**: 执行 `node scripts/hive/watchdog.js COMMIT` 持久化更改。
    - **失败**: 立即执行 `node scripts/hive/watchdog.js ROLLBACK`。
        - 效果：通过 Git 强制恢复代码至快照点，但**保留记忆和日志**。
4.  **HANDOVER**:
    - 系统恢复稳定后，由主意识接管并向“时光”报告。

## File Safety
- **Deletion**: Prefer moving to `trash/` or a temporary quarantine folder over permanent deletion.
- **Backups**: Major refactors should be preceded by a backup or quarantine snapshot.
