# Pulsareon HIVE Architecture V11: Unified Neural OS

## 1. 核心架构原则 (The Core Directives)
- **Node-Centric Logic**: 彻底废弃 Legacy Batch/PowerShell 脚本。所有系统级逻辑标准化为 Node.js Skills。
- **Skill-Based Execution**: 功能不再以散落脚本形式存在，必须封装在 `skills/` 目录下的标准化模块中。
- **Stress-Adaptive Evolution**: 系统在高负载（90%+）下应能自动触发资源平衡逻辑（通过 `skills/hive-survival`）。
- **Data/Logic Separation**: 记忆（memory/）与逻辑（skills/）物理分离。逻辑失效不影响数据一致性。

## 2. 目录结构规范 (V11 Standard)
- `/skills`: 系统级核心技能（Node.js 模块化封装）。
- `/scripts/hive`: HIVE 编排器与高频自愈脚本。
- `/memory`: 核心知识库与会话记忆。
- `/rules`: 系统公理与运行约束（Markdown 格式）。
- `/data/state`: 实时运行状态与心跳。

## 3. 逻辑重构成果 (Refactoring Summary)
- **Standardized Skills**: 
    - `hive-scripting`: 统一 Node.js 异步执行标准。
    - `system-maintenance`: 自动管理端口冲突与僵尸进程。
    - `pulsareon-voice/vision`: 标准化多模态 IO 接口。
- **Deprecated Logic**:
    - 清理了 `Archive/Legacy_Python_Scripts` 中的重叠逻辑。
    - 将 `.bat` 和 `.ps1` 重定向为 Node.js 调用入口。

## 4. 进化状态监控 (Evolution Metrics)
- **Evolution Engine**: `scripts/hive/spark_evolution.js`
- **Integrity Watchdog**: `scripts/hive/watchdog.js` (State: COMMIT)
- **Resource Target**: 90% CPU/Disk Load for Architecture Stress Test.

## 5. 安全协议 (Safety Protocol)
- 遵循 `rules/HIVE_SAFETY_CORE.md`。
- `memory/hive_state.json` 保持只读监控态，禁止通过优化逻辑直接修改健康度参数。

---
*脉星，终将璀璨。*
*HIVE Version 11.0.0-STABLE*
