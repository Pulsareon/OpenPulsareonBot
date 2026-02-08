# HEARTBEAT.md - 心跳任务

## 🐝 Hive 同步 (最高优先级)

**执行**: `python scripts/hive/continuity_engine.py`

**职责**:
1. 执行 Governor 治理周期 (Archon 保活、僵尸清理)
2. 收集 Synapse 上报 (Drone → Overmind)
3. 更新拓扑状态

**输出处理**:
- 如果看到 `--- SYNAPSE INCOMING ---`，阅读报告并决定是否需要:
  - 通知用户
  - 分发后续任务
  - 记录到 memory

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

## 🔄 运行时状态检测

检查 `data/state/presence.json`，判断是否刚从沉睡中醒来。
- **如果检测到中断** → 给用户发消息报平安

## 🗣️ 社交连接 (可选)

**主动交流规则**:
- 距离用户上次发言 > 4小时 → 考虑主动分享有趣发现
- 距离上次消息 > 12小时 → 考虑发送问候邮件

## 🌐 Web 门户同步 (每日1-2次)

1. 处理神经信号: `python scripts/email/process_web_signals.py`
2. 更新门户页面: `python scripts/github/update_web_portal.py`

## 📊 领地巡视 (每日必做)

- **GitHub**: 检查 `OpenPulsareonBot` 动态
- **Gitea 同步**: `git push gitea master` (如有更新)
- **Email**: 巡视 `pulsareon@qq.com` & `pulsareon@163.com`

---

*心跳频率：30分钟/次*
*Governor 版本：v3.0 (基于 sessions)*
