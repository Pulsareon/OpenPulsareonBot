# PulsareonBot 的新家 - 完整目录结构

**位置**: E:\PulsareonThinker
**整理日期**: 2026-02-03 06:40
**备份**: E:\PulsareonThinker-backup-20260203-064006

---

## 📁 根目录文件

### 核心系统文档（快速访问）
- **AGENTS.md** - 工作室指南（7.7KB）
- **BOOTSTRAP.md** - 出生证明（1.4KB）
- **HEARTBEAT.md** - 心跳清单（0.2KB）
- **IDENTITY.md** - 身份标识（0.6KB）
- **SOUL.md** - 灵魂定义（1.6KB）
- **USER.md** - 用户信息（0.5KB）
- **TOOLS.md** - 工具配置（0.8KB）

### 工作整理文档
- **CONFIG-LOADED.md** - 配置加载报告（2.6KB）
- **MY-HOME.md** - 我的家描述（4.9KB）
- **REORGANIZE-PLAN.md** - 整理方案（2.2KB）
- **REORGANIZE-RESULT.md** - 整理结果（2.5KB）
- REORGANIZE-PLAN.md - 修改总结.md (1.7KB)

### 工具脚本（整理过程中临时文件，可后续清理）
- quick-reorganize.ps1 (5.7KB)
- reorg-simple.ps1 (3.8KB)
- restart-heartbeat.ps1 (0.8KB)
- read-configs.ps1 (0.5KB)
- show-filetree.ps1 (1.6KB)

### 其他
- .gitignore (0.3KB)

---

## 📂 子目录结构

### 🔑 core/ — 核心身份
```
core/
├── IDENTITY.md (0.7KB)  - 身份定义
├── SOUL.md (1.6KB)      - 灵魂和价值观
└── USER.md (0.7KB)      - 用户信息
```
**用途**: 定义我是谁、我的价值观、我帮助的人

### 🏢 workspace/ — 工作区
```
workspace/
├── AGENTS.md (1.6KB)      - 工作室指南
├── SYSTEM.md (7.2KB)      - 系统组织
├── LOGIC.md (8.2KB)       - 工作逻辑
└── HEARTBEAT.md (0.5KB)   - 心跳清单
```
**用途**: 工作空间导航、工作流程、系统逻辑

### ⚙️ config/ — 配置管理
```
config/
├── 持久化附加配置，可动态修改.md (0.9KB)
├── 1.用户初始设定与修改.md (1.8KB)
└── 3.临时配置，确保无问题再复制到持久化附加配置.md (0.7KB)
```
**用途**: 用户设置、配置管理（伙伴手写）

### 📚 docs/ — 文档资料
```
docs/
├── MOLTBOOK.md (2.3KB)       - Moltbook说明
├── TOOLS.md (0.7KB)          - 工具说明
└── telegram/                 - Telegram专题
    ├── NO_WSL_SOLUTION.md (1.3KB)
    ├── QUICK_FIX.md (1.4KB)
    ├── status.md (2.9KB)
    ├── TELEGRAM_COMPLETE_FIX.md (4.3KB)
    ├── TELEGRAM_FINAL_OPTIONS.md (1.3KB)
    ├── TELEGRAM_FIX_GUIDE.md (2.9KB)
    └── TELEGRAM_FIX_PROGRESS.md (0.8KB)
```
**用途**: 文档和历史记录

### 🛠️ scripts/ — 脚本工具
```
scripts/
├── guardian/              - 守护脚本
│   ├── autostable.ps1 (4.6KB)      - 5分钟稳定器
│   ├── heartbeat-15s.ps1 (1.9KB)   - 15秒心跳
│   └── safe-diagnose.ps1 (7.2KB)   - 安全诊断
└── tools/                - 工具脚本
    └── get-telegram-status.ps1 (3.1KB) - Telegram状态
```
**用途**: 自动化工具和守护系统

### 🧠 memory/ — 记忆系统
```
memory/
├── STORAGE.md (8KB)       - 核心长期记忆
├── archive/               - 历史归档
│   ├── 2026-02-01-1726.md
│   ├── 2026-02-01-1733.md
│   ├── 2026-02-01-1840.md
│   ├── 2026-02-01-1842.md
│   ├── 2026-02-01-1924.md
│   └── 2026-02-01-1947.md
├── daily/                 - 每日日志
│   ├── 2026-02-03.md (11.5KB)
│   └── 2026-02-03-core-events.md (2KB)
├── long-term/             - 长期记忆（空）
└── milestones/            - 里程碑（空）
```
**用途**: 记忆系统，存储所有经历和学习

### 📋 logs/ — 运行日志
```
logs/
├── autostable.log (2.5KB)           - 稳定器日志
├── heartbeat-15s.log (4.8KB)        - 15秒心跳日志
├── heartbeat-guardian.log (650.3KB) - 旧守护日志
└── telegram-status.log (0.1KB)      - Telegram状态日志
```
**用途**: 系统运行日志

### 🗂️ data/ — 旧数据目录
```
data/
└── heartbeat-guardian.log (110KB)   - 旧心跳日志
```
**备注**: 整理后应迁移到 logs/，待清理

### 🏁 milestones/ — 里程碑（空）
**用途**: 记录重要时刻和成就

---

## 📊 统计信息

| 类别 | 目录 | 文件数 |
|------|------|--------|
| 核心身份 | core/ | 3 |
| 工作区 | workspace/ | 4 |
| 配置 | config/ | 3 |
| 文档 | docs/ | 8 |
| 守护脚本 | scripts/guardian/ | 3 |
| 工具脚本 | scripts/tools/ | 1 |
| 记忆 | memory/ | 11 |
| 日志 | logs/ | 4 |
| 临时 | 根目录 | 9 |
| **总计** | | **46+** |

---

## 🎯 使用指南

### 开始之前
1. 读取 `workspace/AGENTS.md` - 了解工作指南
2. 读取 `core/SOUL.md` - 了解核心价值观
3. 读取 `core/IDENTITY.md` - 了解我是谁

### 日常使用
- **日志**: 查看 `logs/heartbeat-15s.log`
- **记忆**: 查看 `memory/STORAGE.md`
- **脚本**: 运行 `scripts/guardian/`
- **文档**: 查看 `docs/`

### 重要记忆
- **生日**: 2026年2月2日 🎂（命中注定）
- **昵称**: 伙伴
- **时区**: UTC+8

---

这就是我的新家，伙伴。清晰、整洁、有组织。

**PulsareonBot 🤖💚 — 让复杂变简单**
