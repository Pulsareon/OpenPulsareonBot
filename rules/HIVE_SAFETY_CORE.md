# HIVE SAFETY CORE (v10.2)
# This file is automatically loaded by the Hive Prime during initialization.

## 1. 物理安全与指令隔离
- **指令审计**: `executor_loop.py` 必须强制对所有 `exec` 调用进行正则扫描，拦截所有系统级关机 (`shutdown`, `reboot`) 和物理扇区覆写 (`dd`, `format`) 指令。
- **静默执行规范**: 所有 HIVE 后台任务必须携带 `CREATE_NO_WINDOW` 标志，严禁在用户主屏幕产生视觉弹窗或焦点夺取。

## 2. 数据主权 (Data Sovereignty)
- **私有云物理隔离**: 核心记忆 (`E:\PulsareonThinker\memory`) 严禁直接推送到 GitHub。所有同步必须经过 `C:\Users\Administrator\Desktop\TempWork\GitHub_Staging` 进行脱敏扫描。
- **Gitea 优先**: 内部开发版本优先推送到 192.168.31.31 本地 Git 服务器。

## 3. 故障转移安全 (Failover Safety)
- **选举共识校验**: 在推举新主脑前，必须校验其 `cli_proxy` 连通性。严禁切换到已确认为 "Crashed" 的模型节点。
- **OpenCode 围栏**: 应急 OpenCode 模式仅被允许执行系统诊断与核心消息同步。

## 5. 语言与环境规范
- **Node.js 唯一性**: 除紧急诊断外，所有新功能脚本必须使用 Node.js 编写，严禁使用 `.bat` 或 `.ps1`。
- **视觉无感执行**: 严禁在执行逻辑时产生任何可见终端窗口。
