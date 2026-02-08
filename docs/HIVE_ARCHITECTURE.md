# Hive Architecture v3.2 (Simplified)

**核心原则**：实用优先，减少仪式感。

---

## 设计哲学

1. **Overmind 就是我** - 不需要额外的 Python 调度器，主会话本身就是调度中心
2. **Archon 是专家顾问** - 按需咨询，不是常驻进程
3. **Drone 是一次性工具** - spawn → execute → die
4. **Governor 是诊断工具** - 不是自动化调度器，是给我看状态的

---

## 简化后的层级

```
┌─────────────────────────────────────────────────────────┐
│                    OVERMIND (我)                         │
│              agent:main:telegram:dm:xxx                  │
│                                                         │
│  职责:                                                   │
│  • 直接与用户对话                                         │
│  • 决定何时需要子代理                                      │
│  • 读取心跳期间的 Governor 报告                           │
│  • 手动或按需 spawn Archon/Drone                         │
└────────────────────────┬────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
    │ Archon  │    │ Archon  │    │ Drone   │
    │ (按需)   │    │ (按需)   │    │ (一次性) │
    │         │    │         │    │         │
    │ 复杂决策 │    │ 安全审计 │    │ 执行任务 │
    └─────────┘    └─────────┘    └─────────┘
```

---

## 何时使用子代理

### 用 sessions_spawn + Drone 当：
- 任务独立，不需要主会话上下文
- 需要不同模型 (Gemini 快速、DeepSeek 分析)
- 批量处理或长时间运行
- 防止主会话 context 膨胀

### 用 sessions_spawn + Archon 当：
- 需要第二意见 (架构审查)
- 安全敏感操作需要独立验证
- 复杂决策需要多角度分析

### 直接在主会话做当：
- 简单任务
- 需要完整上下文
- 与用户交互相关

---

## Governor 的真正角色

Governor 不再是"自动调度器"，而是**诊断报告生成器**：

```python
# 心跳期间执行
python scripts/hive/continuity_engine.py

# 输出示例:
# [Governor v3.1] Report at 2026-02-07T22:20:34
# Resources: CPU 24% | RAM 56.1%
# Archons: 0 healthy, 2 missing
# Drones: 0 active
# 
# [!] Archons need spawn:
#   - archon-logic (model: deepseek)
```

**我 (Overmind) 读取这个报告，决定是否需要采取行动。**

不是 Governor 自己 spawn，而是我看到报告后判断：
- 真的需要 Archon 在线吗？→ 如果需要，手动 spawn
- 还是只在特定任务时按需创建？→ 大多数情况是这样

---

## 实际工作流

### 场景 1: 用户要求复杂重构
```
User: 整理 hive 目录

Overmind (我):
  1. 评估任务复杂度 → 中等
  2. 决定：可以自己做，不需要 Drone
  3. 直接执行
```

### 场景 2: 用户要求安全审计
```
User: 检查系统安全

Overmind (我):
  1. 评估：需要独立视角
  2. 决定：spawn Archon-Shield
  3. sessions_spawn(label="archon-shield", model="sonnet", task="审计...")
  4. 等待结果，汇总给用户
```

### 场景 3: 批量处理
```
User: 给所有 Python 文件加文档

Overmind (我):
  1. 评估：大量文件，会污染 context
  2. 决定：spawn 多个 Drone
  3. sessions_spawn(label="drone-doc-1", task="处理 file1.py")
  4. sessions_spawn(label="drone-doc-2", task="处理 file2.py")
  5. ...
  6. 收集结果
```

---

## 心跳期间的简化逻辑

```markdown
## HEARTBEAT.md (简化版)

1. 执行 `python scripts/hive/continuity_engine.py`
2. 阅读输出
3. 如果有 Synapse 上报 → 处理
4. 如果资源异常 → 告警
5. 不需要自动 spawn Archon (除非明确配置)
```

---

## Synapse 保留

Synapse 继续作为**子代理上报通道**：
- Drone 完成任务后写入 synapse.json
- 心跳期间 Continuity Engine 读取并展示
- Overmind 决定如何处理

---

## 废弃概念

1. **"常驻 Archon"** - 不再需要，按需创建即可
2. **自动 spawn** - Governor 只报告，不行动
3. **PDP 复杂协议** - 简化为普通文本任务描述
4. **投票/共识** - 复杂化，实际很少用到

---

## 保留的核心脚本

```
scripts/hive/
├── governor.py          # 诊断报告 (给我看)
├── continuity_engine.py # 心跳入口
├── synapse.py           # 上报通道
├── resource_monitor.py  # 资源监控
└── legacy/              # 存档
```

---

*v3.2 核心改变：从"自动化调度"回归"智能辅助"*
