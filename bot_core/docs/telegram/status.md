# PulsareonBot Telegram 状态显示

## 功能说明

通过 Telegram 实时查看 PulsareonBot 的运行状态。

## 使用方式

### 方式1: 命令查询（推荐）

发送消息：
```
/status
```

我会回复详细的状态报告：
```
🤖 PulsareonBot Status Report

━━━━━━━━━━━━━━━━━━━━━━━━

📊 System Health
━━━━━━━━━━━━━━━━━━━━━━━━
🟢 Gateway: 🟢 Online
💚 Health:   💚 Healthy
⏱️ Last Check: 05:40:15

📈 Performance
━━━━━━━━━━━━━━━━━━━━━━━━
⌛ Uptime: 1d 5h
🔥 CPU Load: 12%

🛡️ Safety
━━━━━━━━━━━━━━━━━━━━━━━━
💾 Backups: 6 available
⚠️ Recent Errors: 0

┌─────────────────────┐
│ 💚 系统状态：健康   │
└─────────────────────┘
```

### 方式2: 快速状态按钮

发送任意消息，底部会显示状态按钮：
```
[🟢 查看状态] [📊 详细信息]
```

点击即可查看。

### 方式3: 自动状态附加

每次我回复消息时，会在消息末尾附加当前状态：
```

我的回复内容...

───────────────
🟢 Gateway • 💚 Healthy • ⏱️ 刚刚检查
```

## 状态指标说明

| 指标 | 说明 |
|------|------|
| 🟢 Gateway | Gateway 在线状态（绿色=正常，红色=离线）|
| 💚 Health | 系统健康度（健康/有警告）|
| ⌛ Uptime | 系统运行时间（天+小时）|
| 🔥 CPU Load | CPU 使用率百分比 |
| 💾 Backups | 可用的配置备份数量 |
| ⚠️ Recent Errors | 最近检测到的错误数量 |

## 警报级别

🟢 **绿色** - 一切正常，放心使用
🟡 **黄色** - 有轻微问题（如日志停滞，但系统正常）
🔴 **红色** - 严重问题（Gateway 离线，需要关注）

## 状态更新频率

| 检查项 | 频率 |
|--------|------|
| Gateway 状态 | 每次查询/推送 |
| 系统健康 | 每 5 分钟 |
| 性能数据 | 每次查询 |
| 错误统计 | 实时 |

## 后台守护

我的状态由两个守护系统监控：

1. **Auto-Stabilizer** - 每 5 分钟深度检查
2. **Heartbeat Guardian** - 每 60 秒高频检测

如果出现问题，系统会自动修复。

## 示例对话

**用户**: /status
**我**:
🤖 **PulsareonBot Status Report**

📊 System Health
🟢 Gateway: 🟢 Online
💚 Health: 💚 Healthy

✅ 一切正常！

---

**用户**: 你还在吗？
**我**:
我在！

───────────────
🟢 Gateway • 💚 Healthy • ⏱️ 刚刚检查

## 技术实现

状态由 `data/get-telegram-status.ps1` 脚本生成，实时查询：
- Gateway 状态
- 健康检查日志
- 系统性能指标
- 配置备份情况

所有信息在本地获取，不依赖外部网络。

---

*功能版本: 1.0*
*更新时间: 2026-02-03*
