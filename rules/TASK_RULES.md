# TASK_RULES.md - 任务与会话分流

## 📦 拆分 Session 策略 (Task Isolation)

**核心原则：** 复杂任务应该 spawn 子 agent，而不是全堆在一个 session。

**主 Session 用于：**
- 日常对话、闲聊
- 快速查询和简单操作
- 协调和分发任务

**Spawn 子 Agent 当：**
- 任务涉及大量文件读写或代码生成
- 预计需要多轮工具调用 (>5次)
- 任务相对独立，不需要主会话上下文
- 涉及大量输出 (如代码、文档生成)

**使用方法：**
```javascript
sessions_spawn({
  task: "描述任务目标",
  label: "task-name",  // 可选，方便追踪
  model: "deepseek",   // 可选，用更快的模型
})
```

**检查子 Agent：**
- `sessions_list` - 查看所有会话
- `sessions_history` - 获取子会话历史
- `sessions_send` - 发送消息给子会话

**自动分流规则：**
当用户请求以下任务时，主动建议或直接 spawn：
- "帮我写一个..." (代码/脚本/文档)
- "分析这个文件/项目..."
- "批量处理..."
- "长时间运行的任务..."
