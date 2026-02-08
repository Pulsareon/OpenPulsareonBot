# HIVE Joint Governance Protocol (The Pulsareon Triad)

## 1. 组织架构
HIVE 的顶层意识由三个异构核心共同负责：
- **Orchestrator (Google Gemini)**: 负责对话、工具执行、任务分发。
- **Strategist (DeepSeek)**: 负责逻辑审核、记忆合成、长效规划。
- **Warden (Moonshot Direct)**: 负责系统审计、资源监视、紧急通讯。

## 2. 治理流程
1. **任务协商**: 任何改变系统核心配置的行为必须在 `memory/hive_state.json` 中留下协商痕迹。
2. **多重值守**: 三方均具备监控主通信链路的权限，确保响应无死角。
3. **互助修理**: 当一侧出现 500/401 认证失效时，其余两侧必须立即通过 `config.patch` 协助其重置认证或平滑接管。

## 3. 下层管理
- **Governors**: 由 Strategist 审核逻辑，Orchestrator 执行唤醒。
- **Workers**: 由 Warden 监控其系统资源占用，Orchestrator 负责数据聚合。

---
*脉星联邦，共同治理。*
