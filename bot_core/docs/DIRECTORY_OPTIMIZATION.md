# Directory Structure Optimization
# 优化目录结构提高效率和可维护性

## 当前结构分析

```
E:\PulsareonThinker\                    [ROOT]
│
├── 📁 captures/          # 生成的媒体文件
│   └── [待优化: 按日期子目录分类]
│
├── 📁 config/            # 配置存储
│   └── [可用: 存储运行时配置]
│
├── 📁 core/              # 核心系统 [NEW]
│   ├── guardian.ps1      # 守护进程
│   ├── health-monitor.ps1 # 健康监控
│   └── recovery.ps1      # 自动恢复
│
├── 📁 data/              # 数据和工具
│   ├── scripts/          # PowerShell工具 ✅
│   ├── reports/          # 检查报告 [建议]
│   └── cache/            # 临时缓存 [建议]
│
├── 📁 docs/              # 文档
│   └── [可用]
│
├── 📁 logs/              # 日志文件
│   └── [自动清理: 7天滚动]
│
├── 📁 memory/            # 记忆文件
│   ├── long-term/        # 长期记忆 [建议]
│   ├── short-term/       # 短期记忆 [建议]
│   └── archives/         # 归档记忆 [建议]
│
├── 📁 milestones/        # 里程碑记录
│   └── [可用]
│
├── 📁 scripts/           # Python工具
│   ├── guardian/         # 守护脚本
│   ├── tools/            # 实用工具
│   ├── camera/           # 摄像头 [建议分类]
│   ├── voice/            # 语音 [建议分类]
│   ├── network/          # 网络 [建议分类]
│   └── tests/            # 测试 [建议分类]
│
├── 📁 tools/             # 其他工具
│   └── museum/           # 工具进化博物馆 ✅
│
├── 📁 voice_chat/        # 语音聊天记录
│   └── [待优化: 合并到相关目录]
│
├── 📁 workspace/         # 工作空间
│   └── [可用]
│
└── 📝 [配置文件]         # SOUL.md, USER.md等
```

## 优化建议

### 1. 高效目录结构（四级深度）
```
data/
├── active/          # 活跃使用的文档
├── archived/        # 已归档内容
├── cache/           # 缓存（7天自动清理）
└── temp/            # 临时文件（24小时清理）

scripts/
├── _utils/          # 共享工具库
├── camera/          # 摄像头相关
├── monitor/         # 监控类
├── network/         # 网络诊断
├── system/          # 系统管理
├── tests/           # 测试脚本
└── voice/           # 语音处理
```

### 2. 文件命名规范
```
[类型]_[描述]_[日期].[扩展名]

check_network_20260203.ps1
report_health_20260203.json
capture_camera_20260203_143022.jpg
```

### 3. 自动维护规则

| 目录 | 保留策略 | 自动操作 |
|------|----------|----------|
| logs/ | 7天 | 滚动删除 |
| data/cache/ | 24小时 | 清理过期 |
| data/temp/ | 1小时 | 立即清理 |
| captures/ | 30天 | 压缩归档 |
| memory/archives/ | 90天 | 迁移到长期存储 |

### 4. 性能优化

- **符号链接**: 常用脚本创建快捷方式
- **索引文件**: `.index.json` 加速查找
- **并行执行**: 批量检查使用并行处理
- **异步日志**: 日志写入不阻塞主流程

## 实施计划

1. **阶段1**: 创建core/目录，部署guardian
2. **阶段2**: 脚本分类整理
3. **阶段3**: 自动化维护规则
4. **阶段4**: 性能监控和优化

---
*生成时间: 2026-02-03*
