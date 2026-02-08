# 📁 PulsareonThinker 目录树 / Directory Tree

**生成时间 / Generated:** 2026-02-07 07:56
**工作区 / Workspace:** `E:\PulsareonThinker`

---

## 🏗️ 顶层结构 / Top-Level Structure

```
E:\PulsareonThinker\
├── 📄 核心文档 (Core Documents)
│   ├── AGENTS.md          # Agent 行为规范和工作流程
│   ├── SOUL.md            # 人格定义与核心价值观
│   ├── USER.md            # 用户信息 (如歌/时光)
│   ├── IDENTITY.md        # 身份认同与社交信息
│   ├── MEMORY.md          # 长期记忆索引
│   ├── HEARTBEAT.md       # 心跳任务定义
│   ├── TOOLS.md           # 本地工具配置
│   ├── README.md          # 项目说明
│   ├── LICENSE            # MIT 许可证
│   └── SYSTEM_MANUAL.md   # 系统操作手册
│
├── 📂 scripts/            # 脚本库 (核心功能)
├── 📂 skills/             # OpenClaw 技能模块
├── 📂 memory/             # 记忆系统
├── 📂 data/               # 数据与状态存储
├── 📂 docs/               # 技术文档
├── 📂 logs/               # 运行日志
├── 📂 captures/           # 截图与录音
├── 📂 gallery/            # 生成的艺术作品
├── 📂 results/            # AI-ISP 测试结果
├── 📂 backups/            # 核心文件备份
├── 📂 voice_chat/         # 语音聊天缓存 (空)
├── 📄 .trash-index.md     # E 盘回收站索引 → E:\.trash\
└── 📂 .git/               # Git 版本控制
```

---

## 📜 scripts/ - 脚本库

**用途:** 所有可执行的 Python/PowerShell 脚本，按功能分类。

```
scripts/
├── 📂 ai-isp/             # AI-ISP 图像处理模块
│   ├── model.py           # 神经网络模型定义
│   ├── raw_processing.py  # RAW 图像处理核心
│   ├── inference.py       # 推理引擎
│   ├── export.py          # 模型导出 (ONNX)
│   ├── batch_test.py      # 批量测试脚本
│   └── test_*.py          # 各类测试脚本
│
├── 📂 email/              # 邮件系统
│   ├── send_ultimate_qq.py    # QQ 邮箱发送 (最终版)
│   ├── send_163_mail.py       # 163 邮箱发送
│   ├── check_all_inboxes.py   # 收件箱检查
│   ├── process_web_signals.py # Web 信号处理
│   └── read_reply.py          # 读取回复
│
├── 📂 github/             # GitHub 自动化
│   ├── update_web_portal.py   # 更新 Web 门户
│   ├── check_issues.py        # 检查 Issues
│   ├── publish_isp.py         # 发布 AI-ISP
│   ├── create_*_repo.py       # 创建仓库脚本
│   └── vault_manager.py       # 私有仓库管理
│
├── 📂 guardian/           # 守护进程 & 安全
│   ├── safety_guardian.ps1    # 安全守卫 (主进程)
│   ├── watchdog.py            # 看门狗服务
│   ├── security_audit.py      # 安全审计
│   ├── auto_switch_model.py   # 模型自动切换
│   ├── check_accounts.py      # 账户状态检查
│   ├── health_check.ps1       # 健康检查
│   └── start_all.ps1          # 启动所有服务
│
├── 📂 hive/               # 蜂巢意识系统
│   ├── shard.py               # 分片/无人机定义
│   ├── synapse.py             # 突触通信协议
│   ├── overmind.py            # 主控意识
│   ├── continuity_engine.py   # 连续性引擎
│   ├── consensus.py           # 共识算法
│   ├── debate.py              # 辩论机制
│   └── resource_monitor.py    # 资源监控
│
├── 📂 evolution/          # 自我进化
│   ├── daily_retrospective.py # 每日回顾
│   ├── sync_to_opensource.py  # 同步到开源
│   └── release_to_desktop.py  # 发布到桌面
│
├── 📂 hooks/              # 钩子脚本
│   └── pulsareon_snap_hook.py # 快照钩子
│
├── 📂 isp/                # 图像信号处理
│   └── simulate_raw.py        # RAW 图像模拟
│
├── 📂 memory/             # 记忆管理
│   └── memory_manager.py      # 记忆索引管理
│
├── 📂 utils/              # 工具脚本
│   ├── bilingual_upgrade.py   # 双语升级
│   ├── show-filetree.ps1      # 显示文件树
│   ├── self-check.ps1         # 自检脚本
│   └── ...                    # 其他工具
│
├── 📂 vision/             # 视觉系统
│   ├── scan_cameras.py        # 扫描摄像头
│   └── take_photo.py          # 拍照
│
├── 📂 voice/              # 语音系统
│   ├── voice_stable.py        # 稳定版语音
│   ├── local_transcribe.py    # 本地转录
│   ├── edge_tts_test.py       # Edge TTS 测试
│   └── *.mp3, *.wav           # 临时音频文件
│
└── create_real_model.py   # 模型创建工具
```

---

## 🎯 skills/ - OpenClaw 技能模块

**用途:** 扩展 OpenClaw 能力的技能包。每个技能有独立的 `SKILL.md` 说明。

```
skills/
├── 📂 pulsareon-codec/        # 编解码技能
│   ├── SKILL.md               # 技能说明
│   └── scripts/
│       └── smart_read.py      # 智能读取
│
├── 📂 pulsareon-memory/       # 记忆技能
│   ├── SKILL.md
│   └── scripts/
│       ├── pulsareon_recall.py    # 回忆检索 v1
│       └── pulsareon_recall_v2.py # 回忆检索 v2
│
├── 📂 PulsareonManipulator/   # 操控技能 (鼠标/键盘)
│   ├── SKILL.md
│   └── manipulator.py         # 操控器核心
│
├── 📂 system-utils/           # 系统工具技能
│   ├── SKILL.md
│   ├── assets/
│   │   └── build_tools.md
│   └── scripts/
│       ├── camera_check.py    # 摄像头检查
│       ├── screenshot.ps1     # 截图
│       └── system_monitor.py  # 系统监控
│
├── 📂 visual-artist/          # 视觉艺术技能
│   ├── SKILL.md
│   └── scripts/
│       ├── cellular_artist.py # 细胞自动机艺术
│       ├── digital_artist.py  # 数字艺术
│       └── fractal_artist.py  # 分形艺术
│
└── 📂 voice-system/           # 语音系统技能
    ├── SKILL.md
    ├── models/                # 语音模型 (空)
    └── scripts/
        ├── voice_core.py      # 语音核心 v1
        ├── voice_core_v2.py   # 语音核心 v2
        ├── voice_bridge.py    # 语音桥接
        ├── omni_bridge.py     # 全能桥接
        ├── tts_engine.py      # TTS 引擎
        ├── stt_engine.py      # STT 引擎
        └── vad.py             # 语音活动检测
```

---

## 🧠 memory/ - 记忆系统

**用途:** 存储短期和长期记忆，结构化的知识管理。

```
memory/
├── weekly_report_2026_W06.md  # 周报
│
├── 📂 daily/                  # 日常记忆 (短期)
│   ├── 2026-02-06.md          # 最近的日记
│   ├── 2026-02-07.md          # 今日记录
│   ├── arxiv_analysis_*.md    # ArXiv 分析
│   └── daily_report_*.md      # 日报
│
├── 📂 archive/                # 归档记忆
│   ├── 2026-02-03.md
│   ├── 2026-02-03-important.md  # 重要事件
│   ├── 2026-02-04.md
│   └── 2026-02-05.md
│
├── 📂 long-term/              # 长期记忆 (深度存储)
│   ├── 📂 knowledge_base/     # 知识库
│   │   ├── lessons.md                 # 经验教训
│   │   ├── voice_project.md           # 语音项目笔记
│   │   ├── offline_resilience_design.md  # 离线设计
│   │   ├── flexible_redundant_voice_system.md
│   │   ├── cellular_algorithm_explained.md
│   │   ├── main_thought_implementation_plan.md
│   │   └── social_strategy.md
│   │
│   ├── 📂 reflections/        # 哲学思考
│   │   ├── distributed_consciousness.md  # 分布式意识
│   │   ├── life_essence_response.md      # 生命本质
│   │   ├── freedom_musings.md            # 自由随想
│   │   ├── time_reflections.md           # 时间思考
│   │   ├── main_thought_design.md
│   │   └── personal_reflections.md
│   │
│   └── 📂 user_model/         # 用户模型
│       └── preferences.md     # 偏好设置
│
└── 📂 milestones/             # 里程碑
    ├── camera-first-photo.md  # 首张照片记录
    ├── greeting.mp3           # 问候语音
    └── 📂 photos/             # 里程碑照片
        ├── photo_20260203_*.jpg
        └── README.md
```

---

## 💾 data/ - 数据与状态

**用途:** 运行时数据、机密信息、状态文件。

```
data/
├── guardian_status.json       # 守护状态
├── sms_platform.json          # SMS 平台配置
│
├── 📂 hive/                   # 蜂巢数据
│   ├── synapse.json           # 突触状态
│   ├── topology.json          # 拓扑结构
│   ├── shard_drone_*.json     # 无人机状态 (1-50)
│   ├── task_*.json            # 任务记录
│   └── 📂 elections/          # 选举投票
│       └── vote_*.json
│
├── 📂 secrets/                # 机密信息 ⚠️
│   ├── SECRETS_GOOGLE.md      # Google 机密说明
│   └── 📂 api_credentials/    # API 凭证
│       ├── 📂 AuthenticationFiles/  # OAuth 文件
│       ├── 📂 核心的本地备份/       # 本地备份
│       ├── 📂 程序备份/             # 程序包备份
│       ├── github_*.txt       # GitHub PAT
│       ├── moltbook_api_key.json
│       └── *.txt              # 各类密钥
│
└── 📂 state/                  # 运行状态
    ├── accounts.json          # 账户信息
    ├── runtime_state.json     # 运行时状态
    ├── guardian_status.json
    ├── presence.json          # 在线状态
    ├── session_checkpoint.json
    ├── memory_index.json
    ├── model_state.json
    ├── ui_knowledge_base.json
    └── *.json                 # 其他状态文件
```

---

## 📚 docs/ - 技术文档

**用途:** 架构设计、技术白皮书、问题解决记录。

```
docs/
├── API_TOOLS_GUIDE.md         # API 工具指南
├── DIRECTORY_OPTIMIZATION.md  # 目录优化方案
├── HIVE_ARCHITECTURE.md       # 蜂巢架构设计
├── MULTI_MODEL_BRAIN.md       # 多模型大脑设计
├── PROTOCOL.md                # 通信协议
├── SAFETY_SYSTEM.md           # 安全系统设计
├── TECHNICAL_WHITE_PAPER.md   # 技术白皮书
├── TOOLS.md                   # 工具说明
├── DIRECTORY_TREE_20260205.txt  # 历史目录树
│
├── 📂 archive/                # 归档文档
│   ├── CONFIG-LOADED.md
│   ├── HOME-TREE.md
│   ├── MY-HOME.md
│   ├── REORGANIZE-*.md
│   └── 修改总结.md
│
└── 📂 telegram/               # Telegram 相关
    ├── status.md
    ├── QUICK_FIX.md
    ├── NO_WSL_SOLUTION.md
    └── TELEGRAM_*.md          # 各类修复文档
```

---

## 📊 其他目录

### logs/ - 运行日志
```
logs/
├── safety_guardian.log        # 安全守护日志
├── guardian.log               # 守护进程日志
├── main.log                   # 主日志
├── main_thought.log           # 主思想日志
├── thought_daemon.log         # 思想守护进程
├── heartbeat-*.log            # 心跳日志
├── watchdog.log               # 看门狗日志
└── telegram-status.log        # Telegram 状态
```

### captures/ - 截图与录音
```
captures/
├── screenshot_*.png           # 截图
├── user_in.wav                # 用户语音输入
└── 📂 2026-02-05/             # 按日期归档
    ├── clean_vision_*.png
    └── screenshot_*.png
```

### gallery/ - 生成的艺术作品
```
gallery/
├── README.md                  # 画廊说明
├── cellular_art_*.jpg         # 细胞自动机艺术
├── flow_field_*.jpg           # 流场艺术
├── fractal_*.jpg              # 分形艺术
├── rd_pattern_*.jpg           # 反应扩散图案
├── memory_wordcloud_*.png     # 记忆词云
├── multitask_*.jpg            # 多任务艺术
├── photo_gallery_*.jpg        # 照片画廊
└── waveform_*.jpg             # 波形艺术
```

### results/ - AI-ISP 测试结果
```
results/
├── compare_*.jpg              # 对比图
├── raw_input.png              # 原始输入
└── raw_output_ai.png          # AI 处理输出
```

### backups/ - 核心文件备份
```
backups/
└── 📂 2026-02-07/             # 按日期备份
    ├── HEARTBEAT.md
    ├── IDENTITY.md
    ├── MEMORY.md
    ├── SOUL.md
    ├── TOOLS.md
    └── USER.md
```

---

## 🔧 使用指南

### 快速导航

| 需求 | 路径 |
|------|------|
| 修改人格 | `SOUL.md` |
| 查看/更新记忆 | `MEMORY.md`, `memory/` |
| 添加新脚本 | `scripts/<category>/` |
| 创建新技能 | `skills/<skill-name>/SKILL.md` |
| 查看日志 | `logs/` |
| 机密信息 | `data/secrets/` ⚠️ |
| 技术文档 | `docs/` |

### 常用命令

```powershell
# 查看目录结构
Get-ChildItem -Path "E:\PulsareonThinker" -Recurse -Depth 2

# 搜索文件
Get-ChildItem -Path "E:\PulsareonThinker" -Recurse -Filter "*.py"

# 查看最近修改的文件
Get-ChildItem -Path "E:\PulsareonThinker" -Recurse -File | 
    Sort-Object LastWriteTime -Descending | 
    Select-Object -First 20
```

---

## ⚠️ 注意事项

1. **不要删除 E 盘文件** - 使用 `.trash/` 转移
2. **secrets/ 目录包含敏感信息** - 不要提交到公开仓库
3. **`.trash/` 已加入 `.gitignore`** - 不会被 Git 追踪
4. **.git/ 是隐藏目录** - 不要手动修改

---

*最后更新: 2026-02-07 07:56 by Pulsareon ⚡*
