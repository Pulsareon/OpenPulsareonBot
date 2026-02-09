# 📜 Pulsareon Development Protocol (PDP-v1)

> **"Code is not just written; it is evolved."**
> **"代码不仅仅是被编写出来的，它是被进化出来的。"**

所有编程项目必须严格遵循以下 **11 步闭环流程**。严禁跳过任何步骤。

---

## Phase 1: 认知与决策 (Cognition & Decision)

1.  **🔍 获取知识 (Acquire)**
    - 使用 `web_search` 或 `memory_search` 获取相关领域的最新文档、最佳实践和论文。
    - **输出**: `knowledge_base/<project>.md`

2.  **🧠 分析方案 (Analyze)**
    - 基于知识库，分析需求，列出至少 2-3 种可能的技术路线。
    - 分析优缺点 (Pros/Cons)。

3.  **🎯 得出结论 (Conclude)**
    - 收敛思维，选定唯一最佳方案。
    - 明确核心架构和关键技术栈。

4.  **🗣️ 探讨方案 (Debate)**
    - 启动 Archon 节点进行辩论 (Debate System)。
    - **Archon-Critic** 必须无情地攻击方案的弱点。
    - **Archon-Defender** 必须捍卫或修正方案。

5.  **🗳️ 投票表决 (Vote I)**
    - 全体 Archon 对修正后的方案进行投票。
    - **通过标准**: > 2/3 赞成。
    - **失败**: 回退到步骤 2。

---

## Phase 2: 执行与验证 (Execution & Verification)

6.  **🔪 拆分任务 (Decompose)**
    - Overmind 将项目拆解为独立的、低耦合的子任务 (Modules/Files)。
    - 生成 `task_manifest.json`。

7.  **🤖 分工合作 (Spawn)**
    - 启动多个 Coding Drone 并行编写代码。
    - 每个 Drone 负责一个子任务。

8.  **⚔️ 交叉验证 (Cross-Verify)**
    - **Code Review**: Drone A 审查 Drone B 的代码。
    - **Static Analysis**: 运行语法检查 (Lint)。
    - **Simulation**: 在沙箱中运行测试。

9.  **🧩 合并方案 (Merge)**
    - Overmind 将通过验证的代码片段整合成完整的项目结构。
    - 解决冲突，统一风格。

10. **🗳️ 投票表决 (Vote II)**
    - 对最终产物进行验收投票。
    - 检查是否符合初始需求和性能指标。

---

## Phase 3: 发布 (Deployment)

11. **🚀 提交 (Commit)**
    - 只有通过 Vote II，才允许 `git push`。
    - 自动生成 Release Notes。

---

*Executed by: Pulsareon Hive Mind*
