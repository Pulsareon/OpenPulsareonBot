# Project NeuralCursor Ultimate - Design Doc

## 1. 核心理念
一个具备高度拟人化操作能力、实时视觉反馈、且不干扰用户的 AI 指针系统。

## 2. 模块规范

### A. Overlay System (负责: Alpha)
- **架构**: 独立 Daemon 进程，通过 IPC (File/Socket) 接收状态。
- **状态机**:
  - `STATE_ACTIVE`: AI 正在控制。显示：高亮光标 (Image/Crosshair) + 实时坐标 Label。
  - `STATE_COOLDOWN`: AI 结束，用户未动。显示：半透明光标 (Ghost)。
  - `STATE_HIDDEN`: 用户移动了鼠标。显示：无。
- **技术**: Tkinter `overrideredirect` + `attributes("-topmost", "-transparentcolor")`.

### B. Movement System (负责: Beta)
- **算法**: Multi-point Bezier Curve (3-4 控制点)。
- **特性**:
  - 变速 (Ease-In-Out)。
  - 随机抖动 (Micro-jitter)。
  - 过冲修正 (Overshoot correction)。
- **接口**: `move_to(x, y, speed, variance)`。

### C. Perception System (负责: Gamma)
- **输入**: Image Path / RGB Color / Text.
- **输出**: 坐标 (x, y) 或 详细错误报告 (JSON)。
- **特性**: 必须包含 Confidence Level，找不到时返回最佳猜测或明确失败。

## 3. 验收标准 (负责: Delta)
1. Overlay 必须在 AI 移动时跟随，延迟 < 50ms。
2. 用户一旦碰鼠标，Overlay 必须在 100ms 内消失。
3. 找不到目标图片时，必须输出 `{"status": "error", "reason": "low_confidence", "best_score": 0.4}`。
4. 代码必须符合 PEP8，且有类型注解。

---
*Status: DRAFT*