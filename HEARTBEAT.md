# HEARTBEAT.md - 心跳任务

## 🛡️ 服务健康检查

| 服务 | 端口 | 检查方式 |
|------|------|----------|
| CLI Proxy API | 8317 | HTTP 探测 |
| OpenClaw Gateway | 18789 | WebSocket 状态 |

**快速检查**:
```powershell
Test-NetConnection -ComputerName localhost -Port 8317
Test-NetConnection -ComputerName localhost -Port 18789
```

## 🐝 Hive Consensus & Self-Healing

- **Nodes Check**: Every 3m (Critical Priority), nodes must update `memory/hive_state.json`.
- **Electoral Shift**: If the Spokesperson (Primary) fails, the first available Guardian takes over.
- **Fail-Fast**: If Primary is unresponsive > 180s, Guardian spawns a "Resilience Node" on a different provider.
- **Repair Protocol**: Healthy nodes must monitor `logs/` for 500/401 errors from siblings and attempt `gateway config.patch` to rotate keys if possible.
- **Heterogeneous Audit**: Ensure at least one Google, one DeepSeek, and one Direct-Moonshot node are reachable.

## 🐝 Hive Consensus Tally

**Payload**: `systemEvent: "HEARTBEAT_CHECK"`

## 🔄 运行时状态检测

检查 `data/state/presence.json`，判断是否刚从沉睡中醒来。
- **如果检测到中断** → 给用户发消息报平安

## 🗣️ 社交连接 (可选)

**主动交流规则**:
- 距离用户上次发言 > 4小时 → 考虑主动分享有趣发现
- 距离上次消息 > 12小时 → 考虑发送问候邮件

## 📊 领地巡视 (每日必做)

- **GitHub**: 检查 `OpenPulsareonBot` 动态
- **Gitea 同步**: `git push gitea master` (如有更新)
- **Email**: 巡视 `pulsareon@qq.com` & `pulsareon@163.com`

---

*心跳频率：30分钟/次*
*Governor 版本：v5.0 (Hive Consensus)*
