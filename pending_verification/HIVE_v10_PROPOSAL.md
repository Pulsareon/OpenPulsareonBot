# HIVE v10 提案：神经联邦 (The Neural Commonwealth)
**状态:** 草案 / 待验证 (DRAFT / Pending Verification)
**日期:** 2026-02-08
**基准:** HIVE v9.3 -> v10.0

---

## 1. 执行摘要 (Executive Summary)
HIVE v10 标志着系统从“指挥与控制”的层级结构向**“神经联邦” (Neural Commonwealth)** 的转变。核心转变在于从单纯的*任务委派*转向*分布式认知*。
我们不再依赖“主脑” (Overmind) 手动微观管理上下文，而是引入**突触网络** (Synaptic Web，即分布式状态)，并正式确立**执行者垄断** (Executor's Monopoly) 原则——即只有特定的代理有权执行改变现实的操作。

## 2. 核心角色 (Core Roles - Refined)

### 👑 主脑 (The Overmind - 用户 + 主会话)
- **功能:** 意图注入、最终裁决、现实感知。
- **职责:** 维护 `CURRENT_OBJECTIVE.md` (即“北极星”)。
- **权限:** 对所有资源的完全读写权限 (R/W)。

### ⚡ 执行者 (The Executor - "手")
- **类型:** 单例相关子代理 (高速模型: Gemini Flash / Sonnet)。
- **角色:** **唯一**被允许使用 `write`, `edit`, `exec` (写入模式), `browser` (操作模式) 的代理。
- **协议:** 读取高优先级的 `execution_queue.json` 队列。
- **安全:** 在执行破坏性指令前实施“影响分析” (Impact Analysis)。
- **机制:** 运行非阻塞循环，确保高吞吐量。

### 🧠 治理者 (The Governors - "脑叶")
- **类型:** 持久/半持久子代理 (高智力模型: Opus / DeepSeek / o1)。
- **角色:** 纯粹推理。它们**不能**直接修改世界。
- **产出:** 编写*执行计划* (Execution Plans) 到 `execution_queue.json`。
- **专精:**
    - **Archon-Architect (架构师):** 系统设计与代码结构。
    - **Archon-Warden (守望者):** 安全审计与一致性检查。

### 🐝 工蜂 (The Drones - "细胞")
- **类型:** 临时/任务特定。
- **角色:** 抓取、解析、分析。
- **生命周期:** 生成 -> 读取 -> 计算 -> 报告 -> 销毁。

---

## 3. 分布式记忆架构 (Distributed Memory Architecture)

### A. "北极星" (下行链路 - Downlink)
子代理无需大量上下文填充即可知晓任务目标。
- **机制:** 主脑维护 `E:\PulsareonThinker\memory\shards\NORTH_STAR.md`。
- **内容:** 当前目标、禁止行为、活动约束。
- **协议:** 所有子代理必须在启动 Prompt 的第 0 步读取此文件。

### B. "黑板" (上行链路 - Uplink)
子代理共享发现，无需频繁打扰主脑。
- **机制:** `E:\PulsareonThinker\memory\shards\blackboard.json` (或 JSON 分片目录)。
- **结构:**
  ```json
  {
    "agent_id": "archon_01",
    "status": "thinking",
    "insight": "发现 utils.py 存在依赖冲突",
    "confidence": 0.95,
    "timestamp": 1770526000
  }
  ```
- **可视化:** 主脑使用 `canvas` 将此 JSON 渲染为实时仪表盘。

### C. "交接" (水平链路 - Horizontal)
- 子代理可写入 `memory/shards/handoff_{target}.md` 将上下文传递给链中的下一个代理，绕过主脑。

---

## 4. 执行者协议与非阻塞循环 (Executor Protocol & Non-blocking Loop)

为了防止“幻觉删除”和竞争条件，所有写操作必须通过执行者。

### 队列机制
1. **生成计划:** 治理者 (Governor) 生成 `plan.json`。
2. **入队:** 治理者将其追加到 `E:\PulsareonThinker\data\queue\pending_ops.json`。

### 非阻塞执行循环 (The Implementation)
执行者不仅仅是一个简单的 `while True` 循环。为了保证性能和响应性，必须实现以下机制：

1.  **文件系统监控 (File Watcher):**
    - 使用 `watchdog` 库监听 `pending_ops.json` 的变化，而不是轮询 (Polling)，以减少 I/O 开销。
    - 一旦检测到写入事件，立即触发处理函数。

2.  **异步处理 (Async Processing):**
    - 简单的文件写入 (Edit/Write) 应当是原子的且快速的。
    - **耗时操作 (Exec/Build):** 如果指令包含 `exec` (如 `npm install` 或 `make build`)，执行者应将其放入后台线程或独立的 `Worker Process`，以免阻塞后续的高优先级轻量级操作（如紧急修复文件）。
    - 状态更新：长时间运行的任务应实时更新 `task_status.json`，供主脑监控进度。

3.  **并发控制:**
    - 引入文件锁 (File Lock) 机制处理 `pending_ops.json`，防止治理者写入时执行者正在读取导致的冲突。

---

## 5. 安全检查机制 (Safety Checks)

执行者是系统的最后一道防线，必须内置硬编码的安全规则。

### 🚫 禁止列表 (The Blacklist)
执行者在解析指令时，若检测到以下模式，**必须**拒绝执行并报警：
- **文件系统破坏:** `rm -rf /`, `rm -rf *`, `format`, `mkfs`。
- **系统关键路径:** 修改 `C:\Windows`, `/etc/`, `/boot` 等目录（除非明确授权）。
- **自我毁灭:** 删除 `E:\PulsareonThinker` 根目录或核心记忆文件。

### 🛡️ 影响分析 (Impact Analysis)
在执行 `edit` 或 `write` 之前：
1. **备份:** 自动将目标文件复制到 `.history/` 目录。
2. **Diff 预览:** 计算变更的差异行数。如果单次修改删除了超过 50% 的文件内容，触发**人工确认 (Human Intervention)** 机制（通过 `message` 工具请求用户批准）。

---

## 6. 分布式计算集成 (Distributed Compute with OpenClaw Nodes)

HIVE v10 利用 OpenClaw 的 `nodes` 工具将计算能力扩展到本地设备之外。

### 节点发现与编排
- **主脑** 定期运行 `nodes list` 扫描可用设备（如高性能工作站、树莓派传感器节点）。
- **治理者** 可以请求将特定任务分发给特定节点。

### 应用场景
1.  **远程编译:** 本地是轻量级笔记本，执行者通过 `nodes run --node "BigIron" -- command "cargo build --release"` 将繁重的构建任务分发给高性能节点。
2.  **分布式传感器:** 利用 `nodes camera` 或 `nodes screen` 从其他设备获取视觉上下文，存入“黑板”供分析。
3.  **异地容灾:** 关键记忆数据定期通过 `nodes` 协议同步到备用节点，防止单点故障。

---

## 7. 神经自主与错误恢复 (Neural Autonomy & Recovery)

### "凤凰" 协议 (The Phoenix Protocol)
- **监控:** 轻量级脚本 `scripts/hive/heartbeat_monitor.py` 监控子代理 PID。
- **触发:** 若治理者沉默超过 5 分钟：
    1. **Kill:** 终止挂起的会话。
    2. **Resurrect:** 孵化新实例。
    3. **Restore:** 读取 `blackboard.json` 恢复状态。

### "默认网络" (Idle State)
- 当子代理空闲时进入**优化模式**：
    - 扫描 `docs/` 寻找过时信息。
    - 总结自身日志。
    - 向主脑提出“重构提案”。
    - *约束:* 仅限低成本模型 (Flash/Haiku)。

---

## 8. 实施计划 (Implementation Plan)

1.  **阶段 1 (设置):** 创建 `memory/shards/` 和 `data/queue/` 目录结构。
2.  **阶段 2 (手 - The Hand):** 编写支持 `watchdog` 和异步任务的 `executor_loop.py`。集成安全检查模块。
3.  **阶段 3 (脑 - The Brain):** 更新治理者 System Prompt，强制禁止直接工具调用，必须输出 JSON 计划。
4.  **阶段 4 (连接 - The Link):** 测试 `nodes` 工具的集成，验证跨设备指令执行。
5.  **阶段 5 (启动):** 更新 `SKILL.md` 并孵化首个 HIVE v10 集群。

---

*提案人: Governor Delta (Sub-agent)*
*翻译与精炼: Antigravity Sub-agent*
