# STABILITY_RULES.md - 自愈与回滚协议

## 1. 启动诊断 (Startup Diagnosis)

每次 OpenClaw 重启或会话初始化时，必须执行以下检查：

1.  **日志审计**: 检查 `openclaw.log` 或启动输出中的 `ERROR` / `WARN` 关键字。
2.  **网关状态**: 确认 Gateway 连接是否正常。
3.  **配置完整性**: 验证 `openclaw.json` 是否有明显的结构错误或未满足的依赖（如 `memory-lancedb`）。

## 2. 修正协议 (Correction Protocol)

一旦发现问题，执行以下决策树：

1.  **询问用户**: "检测到系统错误 [Error]. 是否修复？"
2.  **超时默认 (Timeout Default)**: 如果用户在规定时间（默认: 下次心跳或 60秒内）无响应，或者在自动化模式下：
    *   **启动自动修复流程**。

## 3. 安全三明治 (Safety Sandwich)

任何自动化修复**必须**包裹在以下事务中：

```bash
# Step 1: 建立快照 (Snapshot)
git add .
git commit -m "SystemAutofix: Pre-fix backup for [ErrorID]"

# Step 2: 执行修复 (Apply Fix)
run_fix_script()

# Step 3: 验证与死手开关 (Dead Man's Switch)
# 如果修复导致系统崩溃，Watchdog 脚本应在检测到心跳丢失时执行:
git reset --hard HEAD~1
```

## 4. 回滚机制 (Rollback Mechanism)

*   **触发条件**:
    *   系统 Crash / 无法启动。
    *   用户在修复后规定时间内未确认 "System Stable"。
    *   检测到关键功能（如 CLI Proxy）失效。

*   **执行动作**:
    *   回滚 Git 到上一版本。
    *   记录错误到 `logs/autofix_failures.md`。
    *   锁定该修复方案，不再自动尝试，直到用户人工干预。

## 5. 记录 (Logging)

所有自动修复必须记录在 `E:\PulsareonThinker\logs\maintenance.log`。
