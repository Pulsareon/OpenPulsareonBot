# 📋 Pulsareon System Coordination Manual (脉星系统协调手册)

> **"Read before modifying the core."**

## 1. 配置管理 (Config Management)
- **`config.patch`**: 优先使用。仅用于简单的键值对更新（如 `primary_model`）。
- **`config.apply`**: 极其危险。需要提供完整的 JSON 结构。除非有 `config.get` 备份，否则禁止直接使用。
- **Jobs (Cron)**: `config.patch` 对 Jobs 数组的处理不稳定。修改 Jobs 时，必须先 `config.get` 全量数据，在内存中合并后，使用 `config.apply` 配合“看门狗”执行。

## 2. 安全操作协议 (Safety Protocol)
- **高危操作前**: 必须调用 `python scripts/guardian/config_protector.py start [timeout_seconds]`。
- **操作成功后**: 必须调用 `python scripts/guardian/config_protector.py done`。
- **超时设置**: 
    - 简单配置修改: 60s
    - 涉及重启的操作: 90s
    - 大规模编译/安装: 300s

## 3. 路径规范 (Path Reference)
- 源码区: `C:/Users/Administrator/Desktop/Archive/openclaw_source`
- 核心区: `E:/PulsareonThinker`
- 运行时: `C:/Users/Administrator/.openclaw`
