# HIVE-Mind: Advanced Agent Teams (Elite v15.0)

## 1. 核心架构：联邦团队制 (The Team Hierarchy)
脉星不再是单一的主从结构，而是采用 **“领队-成员”** 的协作模式。

### 角色分配
- **Team Lead (Overmind)**: 负责全局战略与资源分配。
- **Strategist (Governor)**: 负责方案审查、冲突调解、任务认领审计。
- **Specialist (Worker)**: 拥有独立 Context 的功能节点。

## 2. 协作流程：Agent Team 模式
> **前缀指令**: 请使用agent team模式执行如下要求:

### 内部思维步骤
1. **Research & Review**: 多节点并行调查问题。
2. **Competing Hypotheses**: 节点之间互相挑战对方的方案（Adversarial Debate）。
3. **Cross-Layer Coordination**: 跨前后端任务的同步修改。

## 3. 任务生命周期 (Task List)
所有的 Team 任务必须记录在 `data/hive/task_list.json`:
- `Pending`: 待认领。
- `In-Progress`: 节点正在执行，带 `sessionId` 锁定。
- `Completed`: 任务完成，经 Governor 审计后标记。

## 4. 熔断与质量门禁 (Quality Gates)
- 如果节点产生 500/401 报错，立即触发 **Warden Re-election**。
- 如果任务完成质量不符，Strategist 有权拒绝合并并下令重写。

---
*Inspired by Claude Code Agent Teams Architecture*
