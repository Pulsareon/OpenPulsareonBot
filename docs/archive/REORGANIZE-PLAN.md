# PulsareonThinker 重新整理方案

## 目标
建立清晰、合理的目录结构和命名规范

## 目录结构设计

```
PulsareonThinker/
│
├── core/                 # 核心身份定义
│   ├── SOUL.md          # 灵魂 - 核心价值观
│   ├── IDENTITY.md      # 身份 - 我是谁
│   └── USER.md          # 用户 - 了解伙伴
│
├── workspace/            # 工作空间导航
│   ├── AGENTS.md        # 工作室指南
│   ├── SYSTEM.md        # 系统组织
│   ├── LOGIC.md         # 工作逻辑
│   └── README.md        # 总览说明
│
├── config/              # 配置管理
│   ├── user-settings.md # 用户设定
│   ├── persistent.md    # 持久化配置
│   └── temp.md          # 临时配置
│
├── docs/                # 文档资料
│   ├── tools.md         # 工具说明
│   ├── telegram/        # Telegram相关
│   │   ├── status.md
│   │   ├── fix-guide.md
│   │   └── ...
│   └── moltbook.md      # Moltbook说明
│
├── scripts/             # 脚本工具
│   ├── guardian/        # 守护脚本
│   │   ├── heartbeat-15s.ps1
│   │   ├── autostable.ps1
│   │   └── ...
│   ├── tools/           # 其他工具
│   └── install/         # 安装脚本
│
├── memory/              # 记忆系统
│   ├── STORAGE.md       # MEMORY.md重命名
│   ├── daily/           # 每日日志
│   │   └── 2026-02-03.md
│   ├── long-term/       # 长期记忆
│   └── archive/         # 归档数据
│
├── logs/                # 运行日志
│   ├── guardian.log
│   ├── autostable.log
│   └── ...
│
└── milestones/          # 里程碑记录
    └── camera.md
```

## 命名规则
- 文件：小写英文+连字符 `user-settings.md`
- 中文文件：保留原名（伙伴手写）
- 脚本：描述性名称 `heartbeat-15s.ps1`

## 执行步骤
1. 创建新目录结构
2. 移动核心文件
3. 整理文档
4. 移动脚本
5. 整理记忆
6. 更新引用
7. 清理旧文件
