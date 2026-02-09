# CONTEXT_RULES.md - Token 与上下文监控

## 💰 Token 与资源主权 (Token Sovereignty)

1. **Quota Awareness**: 任何节点在调用高消耗 Tool 前，必须先通过 `session_status` 评估当前 Token 现状。
2. **Cross-Network Failover**: 
    - 优先级 1: 本地 CLI Proxy (稳定性保障)。
    - 优先级 2: 异构 API 均衡 (Google, DeepSeek, Kimi)。
3. **Recursive Self-Compaction (递归自我整理)**: 
    - 节点必须具备“Token 压力感知”。当发现自身上下文过长（超过窗口 70%）或信息密度过低时，必须主动触发自我归纳。
    - **流程**: 节点使用内置归纳逻辑对当前 Context 进行高保真压缩，提取关键状态和未完成任务，随后通过 `/new` 或 Compaction 机制重置上下文，确保思维的轻量化与敏捷性。
4. **Anomaly Detection**: 严禁模型在单次会话中产生超过 10,000 Tokens 的无意义重复输出。


## 🧠 Token 监控 (Context Awareness)

**自动检测规则：**

在每次回复前，需要意识到当前上下文使用情况。系统会在 prompt 中注入 `ctx_window` 信息，格式如 `<ctx_window>182289 tokens left</ctx_window>`。

**警告阈值：**

| 使用率 | 行为 |
|--------|------|
| ≥ 80% | 在回复开头显示：`⚠️ 上下文使用率: XX%` |
| ≥ 95% | 每次回复都显示：`👺 上下文临界: XX% - 建议 /new 重置` |
| 每增加 1% (超过95%) | 必须提醒一次 |

**计算方法：**
- 从 `ctx_window` 获取剩余 token 数
- 当前模型上下文窗口：200,000 tokens (Claude Opus)
- 使用率 = (总窗口 - 剩余) / 总窗口 × 100%

**主动压缩：**
- 当接近 80% 时，主动建议进行 compaction
- 当接近 95% 时，优先完成当前任务后建议 /new
