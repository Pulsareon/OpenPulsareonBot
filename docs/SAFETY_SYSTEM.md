# 安全维护系统文档

**版本：** 2.0
**更新时间：** 2026-02-05

---

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Pulsareon Safety System                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐       │
│  │ CLI Proxy   │   │  OpenClaw   │   │   Safety    │       │
│  │    API      │   │   Gateway   │   │  Guardian   │       │
│  │  :8317      │   │  :18789     │   │  (daemon)   │       │
│  └─────────────┘   └─────────────┘   └─────────────┘       │
│         │                 │                 │               │
│         └─────────────────┴─────────────────┘               │
│                           │                                 │
│                    ┌──────┴──────┐                         │
│                    │  Accounts   │                         │
│                    │   Monitor   │                         │
│                    └─────────────┘                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 核心组件

### 1. Safety Guardian (`safety_guardian.ps1`)

持续运行的守护进程，每30秒检查一次：

- **CLI Proxy API 状态**：进程 + 端口 8317
- **OpenClaw Gateway 状态**：端口 18789
- **账户健康状态**：通过 Python 脚本
- **磁盘空间**：C: 和 E: 驱动器
- **日志清理**：每小时清理过大/过旧的日志

### 2. Health Check (`health_check.ps1`)

快速健康检查脚本：

```powershell
# 交互式输出
powershell -File "E:\PulsareonThinker\scripts\guardian\health_check.ps1"

# JSON输出（用于自动化）
powershell -File "E:\PulsareonThinker\scripts\guardian\health_check.ps1" -Json

# 静默模式（只返回退出码）
powershell -File "E:\PulsareonThinker\scripts\guardian\health_check.ps1" -Quiet
```

退出码：
- 0 = HEALTHY
- 1 = WARNING
- 2 = CRITICAL

### 3. Account Checker (`check_accounts.py`)

Python 脚本检查 CLI Proxy API 账户状态：

```bash
python "E:\PulsareonThinker\scripts\guardian\check_accounts.py"
```

输出保存到 `data/accounts.json`

### 4. Recovery Script (`recovery.ps1`)

紧急恢复脚本：

```powershell
# 检查模式（不做任何修改）
powershell -File "E:\PulsareonThinker\scripts\guardian\recovery.ps1"

# 重启所有服务
powershell -File "E:\PulsareonThinker\scripts\guardian\recovery.ps1" -RestartAll

# 强制模式（停止冲突进程）
powershell -File "E:\PulsareonThinker\scripts\guardian\recovery.ps1" -Force
```

### 5. Startup Script (`start_all.ps1`)

启动所有核心服务：

```powershell
powershell -File "E:\PulsareonThinker\scripts\guardian\start_all.ps1"
```

---

## 文件位置

| 文件 | 路径 | 用途 |
|------|------|------|
| Safety Guardian | `scripts/guardian/safety_guardian.ps1` | 主守护进程 |
| Health Check | `scripts/guardian/health_check.ps1` | 快速检查 |
| Account Checker | `scripts/guardian/check_accounts.py` | 账户状态 |
| Recovery | `scripts/guardian/recovery.ps1` | 紧急恢复 |
| Start All | `scripts/guardian/start_all.ps1` | 启动服务 |
| Guardian Log | `logs/safety_guardian.log` | 守护日志 |
| Guardian Status | `data/guardian_status.json` | 状态快照 |
| Account Status | `data/accounts.json` | 账户状态 |

---

## 监控数据

### Guardian Status (`data/guardian_status.json`)

```json
{
  "timestamp": "2026-02-05 08:30:00",
  "services": {
    "cliProxy": { "Running": true, "Port": true, "APIHealth": true },
    "gateway": { "Port": true, "APIHealth": true }
  },
  "accounts": { ... },
  "models": { ... },
  "alerts": [],
  "health": "HEALTHY"
}
```

### Account Status (`data/accounts.json`)

```json
{
  "timestamp": "2026-02-05T08:29:18",
  "antigravity": [ ... ],
  "gemini": [ ... ],
  "summary": {
    "antigravity": { "active": 11, "quota_exhausted": 0, ... },
    "gemini": { "active": 11, "error": 0 }
  }
}
```

---

## 心跳集成

在 `HEARTBEAT.md` 中配置了自动检查：

1. 每次心跳检查服务健康
2. 检查账户状态
3. 必要时自动切换模型
4. 记录问题到日志

---

## 已知问题与解决

### EISDIR 错误
- **问题**：OpenClaw chokidar watch `memory.md` 解析到目录
- **原因**：Windows 大小写不敏感
- **解决**：重命名 `memory/` → `memories/`

### PowerShell && 语法
- **问题**：PowerShell 不支持 `&&`
- **解决**：使用 `cmd /c` 或 PowerShell 原生语法

### 编码问题
- **问题**：GBK 编码无法显示 Unicode emoji
- **解决**：使用 ASCII 替代 `[OK]` `[!!]` 等

---

## 手动操作指南

### 检查系统状态
```powershell
openclaw status
powershell -File "E:\PulsareonThinker\scripts\guardian\health_check.ps1"
python "E:\PulsareonThinker\scripts\guardian\check_accounts.py"
```

### 重启服务
```powershell
# 重启 CLI Proxy API
taskkill /f /im cli-proxy-api.exe
cd C:\Users\Administrator\Desktop\CLIProxyAPI_6.7.46_windows_amd64
start cli-proxy-api.exe

# 重启 OpenClaw Gateway
openclaw gateway restart
```

### 查看日志
```powershell
# OpenClaw 日志
openclaw logs --limit 50

# Guardian 日志
Get-Content "E:\PulsareonThinker\logs\safety_guardian.log" -Tail 50
```

---

*此文档自动生成于 2026-02-05*
