# SYSTEM_RULES.md - 系统维护与重启

## ⚡ Gateway Restart 规则

**重要**：在调用 `gateway restart` 前，必须：

1. 先完成当前回复的所有内容
2. **不要在同一个 turn 里 restart** —— 消息可能还没发出去
3. 如果需要 restart，告诉用户"准备重启"，然后在**下一个 turn** 再执行

**正确流程：**
```text
Turn 1: 完成任务 → 回复 "修改完成，需要重启 Gateway 生效，请说 '重启' 或等下一次心跳。"
Turn 2: 用户说 "重启" → 执行 gateway restart
```

**为什么**：Telegram 客户端有时不会立即刷新，如果 restart 太快，用户看不到最后的消息。

## ⚙️ Config Updates

**Get Updates (self-update)** is ONLY allowed when the user explicitly asks for it.

Do not run `config.apply` or `update.run` unless the user explicitly requests an update or config change; if it's not explicit, ask first.

Actions:
- `config.get`, `config.schema`
- `config.apply` (validate + write full config, then restart)
- `update.run` (update deps or git, then restart).

After restart, OpenClaw pings the last active session automatically.
