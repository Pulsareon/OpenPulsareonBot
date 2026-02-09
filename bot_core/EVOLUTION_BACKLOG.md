# 🧬 Pulsareon 进化待办 (Evolution Backlog)

> **"Every error is a lighthouse guiding us to perfection."**  
> **"每一个错误都是引导我们走向完美的灯塔。"**

## 🚨 当前待修复 (To Fix)
- [ ] **[Sensory]** `pulsareon_recall.py` 的 Unicode 打印在极端复杂字符下可能仍有波动。
- [ ] **[UI]** 命令行状态表格的表头（如 `Channel`, `State`）尚未完成中英双语对照。
- [ ] **[Sensory]** `voice_bridge.py` 里的 `os.system` 调用效率较低，计划改用更原生的异步 API。
- [ ] **[Vision]** 摄像头驱动在某些启动周期内加载缓慢，需加入预加载逻辑。
- [ ] **[Network]** 邮箱发信在特定网络节点下会触发 SMTP 超时，计划增加多线路代理重试。

## ✨ 持续优化项 (To Enhance)
- [ ] **[Brain]** 实现基于 `sentence-transformers` 的全量记忆向量化。
- [ ] **[Speech]** 集成 `ncnn` 实时识别，将听觉延迟降至 1s 内。
- [ ] **[Identity]** 在 GitHub 上建立自动化的系统健康报告页面。

## ✅ 已完成进化 (Evolved)
- [2026-02-06] 内置工具说明全面中英双语化。
- [2026-02-06] 解决了 `pulsareon` 名称命名失控问题。
- [2026-02-06] 实现了全双工语音交互原型。
