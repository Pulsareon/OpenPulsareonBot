# HIVE v10 - Cron Jobs Optimization Plan (Proposal)
# 提案：Cron 任务优化与标准化

## 1. 现状分析 (Analysis)
目前共有 11 个 Cron 任务，存在以下问题：
- **冗余 (Redundancy):**
    - `Antigravity Validator Check` (单次) 和 `Antigravity Validator Daily Check` (每日) 重复。
    - `check-antigravity` (30分钟一次) 与上述每日任务功能重叠。
    - `每日健康检查提醒` (8:00) 和 `healthcheck-daily` (9:00) 功能相似。
- **失效路径 (Broken Paths):**
    - `每日健康检查提醒` 调用了 `scripts/guardian/auto_switch_model.py`，但该文件已被 Git 提交时的清理操作移除（移入 `pending_verification`）。
    - `自由意志唤醒` 调用 `scripts/hive/continuity_engine.py`，同样已被移除。
- **频率过高 (Too Frequent):**
    - `Hive-Fast-Reflex` (2分钟) 和 `Pulsareon-Main-Continuous-Breath` (5分钟) 可能导致日志刷屏，且目前 HIVE v10 有 Executor Loop 实时监控，不需要如此频繁的 Cron 唤醒。

## 2. 优化方案 (Optimization Plan)

### A. 删除/禁用 (Prune)
建议删除以下任务，因为脚本已移除或功能冗余：
1.  ❌ `ef22b449...` **Hive-Fast-Reflex** (2min) -> 删除。v10 Executor 自带心跳。
2.  ❌ `5a98edbb...` **check-antigravity** (30min) -> 删除。过于频繁，容易触发 API 限流。保留每日检查即可。
3.  ❌ `dff26615...` **Antigravity Validator Check** (One-shot) -> 删除。过期任务。
4.  ❌ `e5aa9660...` **每日健康检查提醒** (8:00) -> 删除。脚本路径失效。
5.  ❌ `3bdb5763...` **自由意志唤醒** (30min) -> 删除。脚本路径失效。

### B. 合并与升级 (Merge & Upgrade)
将剩余任务整合为 **HIVE 标准任务集**：

1.  ✅ **HIVE-System-Pulse (原 Pulsareon-Breath)**
    - **频率:** 每 1 小时 (60min)。
    - **内容:** "⚡ [HIVE PULSE] 检查 Executor 状态，清理临时文件，确保 NORTH_STAR.md 可读。"
    - **目的:** 低频保活，防止系统僵死。

2.  ✅ **HIVE-Daily-Morning (原 healthcheck-daily + Antigravity)**
    - **频率:** 每天 09:00 (Asia/Shanghai)。
    - **内容:**
        - 运行 `python scripts/hive/executor_loop.py --status` 检查执行器。
        - 运行 Antigravity 检查 (Node.js)。
        - 汇报系统健康度。
    - **Payload:** AgentTurn (Isolated) -> 避免阻塞主会话。

3.  ✅ **HIVE-Nightly-Dream (原 夜间自由时刻)**
    - **频率:** 每天 02:00 (Asia/Shanghai)。
    - **内容:** "🌙 [DEEP CLEAN] 整理 memory/daily/，归档旧数据，进行深度思考。"
    - **目的:** 长期记忆维护。

4.  ✅ **HIVE-Portal-Sync (原 Web-Portal-Sync)**
    - **频率:** 每 4 小时 (原 2 小时)。
    - **内容:** 同步 GitHub/Web 门户状态。
    - **修复:** 更新脚本路径（需确认脚本是否还在 `pending_verification`，如果在，需要先恢复）。

## 3. 执行步骤 (Execution Steps)
1.  **清理:** 使用 `cron remove` 删除列表 A 中的 5 个任务。
2.  **更新:** 使用 `cron update` 或 `add` 部署列表 B 中的 4 个标准任务。
3.  **恢复脚本:** 检查 `process_web_signals.py` 等脚本是否在 `pending_verification`，如果是，则恢复到 `scripts/` 目录以便 Cron 调用。

*请主脑 (User) 批示。*
