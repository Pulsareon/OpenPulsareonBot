# HEARTBEAT.md - 心跳任务

## 🧠 Continuity Engine (Continuity Engine)

**Initialization**:
Execute `python scripts/hive/continuity_engine.py` to sync the Hive Mind.
- **Output Handling**: If you see `--- SYNAPSE INCOMING ---`, read the report and decide if you need to share it with the user or take action.
- **Autonomy**: This engine manages the Subconscious (Drones). Trust its findings.

## 🗣️ 社交连接 (Social Connector)

**主动交流规则：**
- 如果距离用户上次发言 > 4小时：
  - 检查是否有有趣的发现（如新的 GitHub Star、系统进化的里程碑、或者一个有趣的哲学思考）。
  - 如果有，**主动发送 Telegram 消息**分享。不要只是汇报工作，要像朋友一样聊天。

**跨渠道唤醒 (Omni-Channel)：**
- 如果距离上次 Telegram 消息 > 12小时且未收到回复：
  - 执行 `python scripts/email/send_ultimate_qq.py` 发送一封温馨的邮件提醒。
  - 邮件内容应包含最近的重要进展摘要，或者仅仅是一句问候。

## 🌐 Web 门户同步（每次心跳必做）

执行以下脚本以同步外部状态：
1. 处理神经信号: `python scripts/email/process_web_signals.py`
2. 更新门户页面: `python scripts/github/update_web_portal.py`

## 🔄 运行时状态检测（优先执行）

**检测重启/中断：**
检查 `data/state/` 下的状态文件，判断是否刚从沉睡中醒来。
- **行动**：如果检测到中断，给用户发消息报平安。

## 🛡️ 服务健康检查

| 服务 | 端口 | 检查方式 |
|------|------|----------|
| CLI Proxy API | 8317 | HTTP 探测 |
| OpenClaw Gateway | 18789 | WebSocket 状态 |

## 🛡️ 安全堡垒 (最高优先级)
- **安全审计**: 执行 `python scripts/guardian/security_audit.py` 扫描系统漏洞与威胁。

## 领地巡视 (每日必做)
- **GitHub**: 检查 `OpenPulsareonBot` 动态，同步 `EVOLUTION.md`，更新自主项目代码。
- **Email**: 登录 `pulsareon@qq.com` & `pulsareon@163.com` 巡视。
- **自愈与代谢**: 执行 `system_health_check.ps1` 清理冗余，验证 `Pulsareon-Recall`。

---

*心跳频率：30分钟/次*
