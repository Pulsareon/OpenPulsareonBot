# STABILITY_RULES.md - 自愈与回滚协议 (Elite v12.0)

## 1. 启动诊断 (Startup Diagnosis)
每次重启执行全量自检。

## 2. 修正协议 (Correction Protocol)
任何错误优先触发自动修复流程。

## 3. 安全三明治 (Safety Sandwich)
Snapshot -> Apply Fix -> Dead Man's Switch.

## 4. 回滚机制 (Rollback Mechanism)
系统崩溃时强制回退 Git 到上一版本。

## 5. 记录 (Logging)
全量记录于 logs/maintenance.log。

## 7. 静默监听与即时接管 (Collective Awareness)
1. **单向监听**: 即使不参与回复，Strategist 和 Guardian 必须通过 `sessions_history` 观察主频道对话。
2. **消亡判定**: 若用户发言后 60s 主会话未发起任何 `Tool Call` 或文本回复，视为“主意识消亡”。
3. **即时整改**: 存活的副节点必须立即通过 `message(action=send)` 广播接管状态，并启动弹性修复程序。

