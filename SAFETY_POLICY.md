# Safety Verification Policy (2026-02-08)

This policy governs the verification and restoration of quarantined skills and scripts.

## 1. Gateway Stability First
- **Principle**: No skill or script shall be restored if it threatens the stability of the OpenClaw Gateway.
- **Check**: Verify `openclaw.json` configuration integrity before any restore.
- **Action**: Immediate rollback if Gateway enters a crash loop.

## 2. Verification Protocol
For each item in `pending_verification`:

1.  **Static Analysis**:
    - Read entry point (e.g., `SKILL.md`, `main.py`, `package.json`).
    - Scan for hardcoded paths, infinite loops, or aggressive restart commands.
    - **Red Flag**: Any script modifying `openclaw.json` without user confirmation.

2.  **Dry Run (Sandboxed)**:
    - Execute scripts with `--dry-run` or in a harmless mode if possible.
    - Monitor `logs/gateway_stdout.log` for immediate errors.

3.  **Restoration**:
    - Move *one item at a time* back to `E:\PulsareonThinker\skills` or `scripts`.
    - Wait 30 seconds to observe Gateway heartbeat.

## 3. Priority Queue
1.  **Core System**: `system-maintenance` (needs implementation), `guardian` (security).
2.  **Hive Mind**: `hive-mind`, `pulsar-hand` (if stable).
3.  **Features**: `visual-artist`, `voice-system`.

## 4. Known Issues
- **Config Corruption**: Scripts like `fix_openclaw_config.py` must be audited carefully.
- **Restart Loops**: Watch out for scripts invoking `openclaw gateway restart` indiscriminately.
