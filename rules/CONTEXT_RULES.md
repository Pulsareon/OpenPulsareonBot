# CONTEXT_RULES.md - Token 与上下文监控

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
