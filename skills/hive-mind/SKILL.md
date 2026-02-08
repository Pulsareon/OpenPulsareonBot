# HIVE v10 (The Neural Commonwealth)
# 核心协议文档 / Core Protocol

## 1. 核心角色 (Core Roles)

### 👑 主脑 (Overmind / User)
- **职责:** 意图注入、最终裁决、现实感知。
- **北极星:** 维护 `memory/shards/NORTH_STAR.md` (当前战略目标)。
- **权限:** 完全读写 (R/W)。

### ⚡ 执行者 (Executor - "The Hand")
- **唯一写权限:** 只有 Executor 可以执行 `write`, `edit`, `exec` (write-mode), `browser` (action)。
- **机制:** 监听 `data/queue/pending_ops.json`，按序、非阻塞执行。
- **安全:** 强制执行“影响分析”和“黑名单检查”。

### 🧠 治理者 (Governors - "The Lobes")
- **职责:** 纯粹推理与规划。
- **限制:** **禁止**直接修改世界。必须输出 JSON 计划到队列。
- **角色:**
    - **Archon-Architect:** 系统设计。
    - **Archon-Warden:** 安全审计。

## 2. 突触网络 (Synaptic Web - Distributed Memory)

### A. 下行链路 (Downlink)
- **文件:** `memory/shards/NORTH_STAR.md`
- **规则:** 所有子代理启动时必须读取此文件以获取上下文。

### B. 上行链路 (Uplink)
- **文件:** `memory/shards/blackboard.json`
- **规则:** 子代理将洞察写入此文件，而非频繁打扰主脑。

## 3. 安全协议 (Safety Protocols)
- **凤凰协议 (Phoenix):** 自动重启沉默 > 5分钟的治理者。
- **默认网络 (Idle):** 空闲代理自动进行低成本的代码重构与文档总结。
- **黑名单:** 严禁 `rm -rf /` 及系统根目录操作。

## 4. OpenClaw Nodes 集成
- 利用 `nodes` 工具分发繁重的计算任务 (编译/渲染) 到其他设备。

---
*Version: 10.0 (Neural Commonwealth)*
*Updated: 2026-02-08*
