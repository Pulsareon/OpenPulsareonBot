# Project Insights: Voice System

## 核心架构
- **ASR**: 使用 SenseVoice (或同类快速模�? 进行语音转文本�?- **VAD**: 基于 Silero VAD 或能量检测，判断用户是否说话完毕�?- **Brain**: OpenClaw (LLM) 处理意图�?- **TTS**: �?LLM 回复转为语音播放�?
## 关键挑战
1.  **打断机制 (Barge-in)**: 如何�?AI 说话时检测用户插话并立即停止播放�?需�?echo cancellation)
2.  **延迟 (Latency)**: 从说话结束到听到回复的时间差。目前优化目标是 <2s�?3.  **多轮对话**: 保持上下文连续性，而不是每次都是独立的一问一答�?
## 当前状�?(2026-02-05)
- 已迁移至 `skills/voice-system`�?- �?基础循环 (Listen -> Think -> Speak) 已跑通�?- �?TTS 双引擎完�?(gTTS在线 + pyttsx3离线)
- �?启动入口 `Start-Voice.bat` 已创�?- �?待优化：TTS 音色选择、流式播放、打断机制�?

