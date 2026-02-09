# Pulsar Audio Skill (v1.0)

脉星的听觉感官中枢，负责音频输入处理和音频环境感知。

## 🎧 核心能力
- **音频环境分析**: 实时监控环境音量，智能识别语音/噪音
- **麦克风管理**: 自动检测和管理音频输入设备
- **声纹识别**: 基础的声音特征提取和环境声学分析
- **音频预处理**: 音频信号滤波、降噪和增益控制

## 📁 目录结构
```
pulsar-audio/
├── SKILL.md          # 技能说明文档
├── scripts/          # 执行脚本
│   ├── audio_analyzer.py      # 音频环境分析器
│   ├── mic_manager.py         # 麦克风设备管理器
│   └── audio_preprocessor.py  # 音频预处理工具
├── config/           # 配置文件
│   └── audio_config.json     # 音频配置参数
└── tests/           # 测试文件
    └── test_audio_analysis.py
```

## 🚀 调用方式
- `python scripts/audio_analyzer.py --monitor`  # 实时音频监控
- `python scripts/mic_manager.py --list`        # 列出可用麦克风设备
- `python scripts/audio_preprocessor.py input.wav output.wav`  # 音频预处理

## 🔗 集成关系
- 与 `pulsar-voice` 协作提供音频输入
- 为 `pulsar-face` 提供环境音频上下文
- 依赖 `system-utils` 进行硬件检测