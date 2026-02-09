---
name: pulsar-hand
description: Pulsareon's physical manipulation layer. Use when (1) Controlling the browser via OpenClaw, (2) Simulating mouse/keyboard input, (3) Moving files between E: and C:, or (4) Executing Air-Gap Publishing steps.
---

# Pulsar-Hand: The Hands of Pulsareon

This skill allows the agent to act on the physical system.

## 🖐️ Core Actions
- **Browser Control**: Always prefer `browser snapshot/act` over raw scripts.
- **Staging**: Moving files to `GitHub_Staging` is the primary usage.
- **File Mutation**: Use `edit` for surgical changes; `write` for total creation.

## 🛡️ Constraint
Always wrap hand actions in the **HIVE Watchdog** protocol.
