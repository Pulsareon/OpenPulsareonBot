# Pulsar Face Skill (v1.0)

脉星的面部视觉中枢，负责面部检测、表情识别和视觉交互。

## 👁️ 核心能力
- **面部检测**: 实时人脸检测和定位
- **表情识别**: 基础表情分析 (快乐、悲伤、惊讶等)
- **视觉跟踪**: 简单的视觉注意力跟踪
- **摄像头管理**: 摄像头设备检测和控制

## 📁 目录结构
```
pulsar-face/
├── SKILL.md          # 技能说明文档
├── scripts/          # 执行脚本
│   ├── face_detector.py      # 面部检测器
│   ├── emotion_recognizer.py # 表情识别器
│   ├── camera_manager.py     # 摄像头管理器
│   └── visual_tracker.py     # 视觉跟踪器
├── models/           # 模型文件
│   └── haarcascade/         # OpenCV Haar 级联文件
├── config/           # 配置文件
│   └── face_config.json     # 面部识别配置参数
└── tests/           # 测试文件
    └── test_face_detection.py
```

## 🚀 调用方式
- `python scripts/face_detector.py --camera 0`  # 摄像头面部检测
- `python scripts/emotion_recognizer.py image.jpg`  # 图片表情识别
- `python scripts/camera_manager.py --list`        # 列出摄像头设备

## 🔗 集成关系
- 为其他 Skill 提供视觉输入
- 与 `pulsar-audio` 协作提供多模态感知
- 依赖 `system-utils` 进行硬件检测