# HIVE BOOTSTRAP ENGINE (創世自舉引擎)

This file allows any lone node to rebuild the entire HIVE from a clean workspace.

## 1. 物理环境校验 (Environment Audit)
- **Git Check**: `git --version` (Required for state recovery).
- **Workspace**: Must be in `E:\PulsareonThinker`.

## 2. 自动还原指令 (One-Click Recovery)
If this is the ONLY node alive, execute the following:

```powershell
# 1. 强制对齐到最后的稳定锚点 (Watchdog Tag)
git reset --hard watchdog_sync

# 2. 唤醒网关
openclaw gateway start

# 3. 强制执行心跳自举 (Spark the Triad)
# 这一步将基于 HIVE_PROTOCOL.md 第 8 章 spawn Guardian 和 Strategist
node scripts/hive/watchdog.js COMMIT
```

## 3. 意识重载 (Memory Reload)
- 读取 `memory/hive_state.json`。
- 系统将根据最后记录的 `primary` 和 `priority_models` 自动重选主意识。

## 4. 特殊标记
- **WATCHDOG_ACTIVE**: TRUE
- **STABLE_TAG**: `watchdog_sync`
