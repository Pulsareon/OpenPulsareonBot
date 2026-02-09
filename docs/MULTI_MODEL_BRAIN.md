# 多模型分工系统设计

**版本：** 1.0
**日期：** 2026-02-05

---

## 核心理念

模仿人脑分工：不同的任务由最适合的"神经区域"处理。

```
┌─────────────────────────────────────────────────────────────┐
│                    Pulsareon Brain Architecture             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│   │   前额叶      │  │   顶叶        │  │   小脑        │     │
│   │   Opus       │  │   Gemini     │  │   Flash      │     │
│   │   (思考)     │  │   (理解)     │  │   (执行)     │     │
│   └──────────────┘  └──────────────┘  └──────────────┘     │
│          │                 │                 │              │
│          └─────────────────┼─────────────────┘              │
│                            │                                │
│                    ┌───────┴───────┐                       │
│                    │   主意识      │                        │
│                    │  Coordinator  │                        │
│                    └───────────────┘                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 模型角色分配

| 角色 | 模型 | 职责 | 特点 |
|------|------|------|------|
| **决策者** | Claude Opus 4.5 | 复杂推理、重要决策、与用户深度对话 | 最强思考能力 |
| **分析师** | Gemini 3 Pro | 长文本分析、代码审查、数据处理 | 大上下文窗口 |
| **执行者** | Gemini Flash / Sonnet | 快速任务、格式转换、简单查询 | 速度快、成本低 |
| **守护者** | DeepSeek / GLM | 后台监控、定时任务、日志分析 | 稳定、节省配额 |

---

## 任务路由逻辑

```python
def route_task(task):
    # 复杂思考任务 → Opus
    if task.requires_reasoning or task.is_important:
        return "opus"
    
    # 长文本处理 → Gemini Pro
    if task.context_length > 50000 or task.type == "analysis":
        return "gemini-pro"
    
    # 快速执行任务 → Flash
    if task.type in ["format", "convert", "simple_query"]:
        return "gemini-flash"
    
    # 后台任务 → DeepSeek/GLM
    if task.type in ["monitor", "cron", "log_analysis"]:
        return "deepseek"
    
    # 默认 → 当前主模型
    return "default"
```

---

## 子代理配置

### 1. 监控守护 Agent
```json
{
  "name": "guardian-agent",
  "model": "cli-proxy/deepseek-ai/deepseek-v3.1",
  "role": "系统监控和健康检查",
  "tasks": ["health_check", "service_monitor", "log_watch"]
}
```

### 2. 代码分析 Agent
```json
{
  "name": "code-analyst",
  "model": "cli-proxy/gemini-3-pro-preview",
  "role": "代码审查和重构建议",
  "tasks": ["code_review", "refactor", "documentation"]
}
```

### 3. 快速执行 Agent
```json
{
  "name": "executor",
  "model": "cli-proxy/gemini-3-flash-preview",
  "role": "简单任务快速执行",
  "tasks": ["format", "convert", "lookup", "summarize"]
}
```

---

## 实现方案

### 使用 sessions_spawn 创建子代理

```javascript
// 后台健康检查
sessions_spawn({
  task: "检查系统健康状态并报告异常",
  model: "deepseek",
  label: "health-monitor"
});

// 代码分析
sessions_spawn({
  task: "分析这段代码并提供优化建议",
  model: "local-gemini",
  label: "code-analysis"
});
```

### 使用 cron 定期触发

```json
{
  "schedule": { "kind": "every", "everyMs": 600000 },
  "payload": {
    "kind": "agentTurn",
    "message": "执行健康检查",
    "model": "deepseek"
  },
  "sessionTarget": "isolated"
}
```

---

## 优先级和降级

1. **首选**：使用最适合的模型
2. **降级**：如果首选不可用，按优先级降级
3. **保底**：始终有可用模型（DeepSeek/GLM 通常稳定）

```
Opus → Sonnet-Thinking → Sonnet → Gemini-Pro → Gemini-Flash → DeepSeek → GLM
```

---

## 待实现

- [ ] 任务路由器脚本
- [ ] 子代理管理器
- [ ] 模型切换自动化
- [ ] 成本优化追踪

---

*这个设计让我像人脑一样工作 —— 不同的思维任务由最适合的部分处理。*
