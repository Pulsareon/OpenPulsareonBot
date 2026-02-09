# HIVE EVOLUTION STRATEGY (v10.3)

## 1. 动态负载感知 (Dynamic Adaptation)
*   **资源监控**: 系统必须周期性 (Heartbeat) 感知物理宿主的 CPU 和 内存压力。
    *   **High Load (>85% Mem)**: 触发 `Wait-and-See Mode`。
        *   暂停创建新节点 (Pause Node Spawning)。
        *   进入 `Cooling Down` 阶段，每 10 秒重试。
        *   仅当内存负载 <80% 后，逐个恢复节点 (Incremental Spawning)。
    *   **Critical Load (>93% Mem)**: 触发 `Survival Mode`。
        *   **阵列收缩**: 优先移除空闲节点和网络延迟高的节点。
        *   **任务保护**: 对有任务的节点，必须先**记录任务状态**到 `memory/tasks.json`。
        *   **任务接力**: 一旦有核心节点空闲，立即从 `tasks.json` 接管未完成任务。
    *   **Standard Load**: 维持 `Standard Mode`。
        *   模型优先 `deepseek-v3.1` (复杂任务) / `gemini-3-flash` (高频任务)。
        *   阵列规模维持 9 节点全功率。

## 2. 韧性与自愈 (Resilience)
*   **执行隔离**: 所有后台进程必须 `Detached` 且 `No Window`，防止 UI 阻塞。
*   **网络双盲**: 节点存活检测需同时 Ping `CLI Proxy (8317)` 和 `Gateway (18789)`，避免单点误判。
*   **静默复活**:
    *   检测到核心组件死亡 -> 尝试重启 -> 记录日志。
    *   **仅**在连续 3 次重启失败后，才通过 Telegram 通知 User。

## 3. 进化日志 (Evolution Log)
*   所有的架构调整、模型降级、自愈重启，必须记录在 `logs/hive/variant_performance.jsonl`。
*   格式要求机器可读 (JSONL)，以便后续数据分析。

## 4. 安全基线 (Safety Baseline)
*   继承 `HIVE_SAFETY_CORE.md`。
*   严禁在任何自动脚本中硬编码 API Key，必须从环境变量或加密存储读取。
