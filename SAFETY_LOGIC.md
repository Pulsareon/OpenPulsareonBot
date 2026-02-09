# Safety Mechanism Logic (2026-02-08)

This document defines the multi-layer safety and recovery logic for OpenClaw Gateway.
These protocols are implemented in `scripts/guardian/safety_guardian.ps1` and `skills/system-maintenance/scripts/repair_gateway.py`.
If scripts are lost or corrupted, reimplement them strictly following this logic.

## Layer 1: Configuration & Process Health (Python)
**Trigger**: Called by Layer 2 upon repeated failures.
**Logic**:
1.  **Config Integrity**:
    - Check `C:\Users\Administrator\.openclaw\openclaw.json`.
    - Ensure `gateway.mode` == `local`.
    - Ensure `gateway.port` == `18789`.
    - **Backup First**: Before ANY write, copy config to `backups/config/`.
2.  **Zombie Cleanup**:
    - Scan for stale `openclaw.exe` or `node.exe` processes holding resources.
    - Kill them gracefully, then forcefully if needed.
3.  **Port Conflict**:
    - Check if port 18789 is occupied by a non-OpenClaw process.
    - Log critical alert if conflict found.

## Layer 2: Real-time Guardian (PowerShell)
**Trigger**: Continuous loop (Interval: 30s).
**Logic**:
1.  **Monitor**: `Test-NetConnection localhost -Port 18789`.
2.  **Failure Handling**:
    - **Count Failures**: Increment `$failGw`.
    - **Threshold**: If `$failGw >= 5` (approx 2.5 mins down):
        - **Execute Layer 1**: Run `repair_gateway.py`.
        - **Reset Counter**: Set `$failGw = 0`.
    - **Restart Attempt**: `Start-Process openclaw gateway start`.
3.  **Recovery**:
    - If port check succeeds, reset `$failGw`.
    - Log success.

## Layer 3: Persistence (Scheduled Task)
**Trigger**: Hourly.
**Logic**:
1.  Check if `safety_guardian.ps1` process is running.
2.  If not, start it.

## Critical Constraints
- **Backup Mandatory**: No config modification without backup.
- **Fail-Safe**: If Layer 1 fails, do NOT loop restart (prevent log spam/CPU spike).
- **Notification**: Log all recoveries to `logs/safety_guardian.log`.
