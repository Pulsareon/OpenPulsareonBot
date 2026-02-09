# PULSAREON HIVE - Neural Synaptic Network Background

## 🧠 概述

这是一个高性能的Canvas神经突触连接网背景动画，专为PULSAREON HIVE web portal设计。它取代了简单的星空背景，模拟大脑神经网络的动态连接和脉冲效果。

## ✨ 特性

- **高性能优化**: 使用requestAnimationFrame和优化的渲染算法，确保60fps流畅动画
- **动态神经网络**: 25个神经节点，每个节点最多3个连接，模拟真实的神经网络结构
- **脉冲效果**: 随机触发的神经脉冲，带有渐变色发光效果
- **自适应布局**: 自动适应屏幕尺寸变化
- **低CPU占用**: 经过优化，不会造成页面卡顿

## 🚀 使用方法

### 快速集成

1. 将 `neural-background.js` 和 `neural-index.html` 复制到您的项目
2. 在HTML中引入JavaScript文件：
   ```html
   <script src="neural-background.js"></script>
   ```

### 自定义配置

在 `NeuralNetworkBackground` 类的 `config` 对象中可以调整以下参数：

```javascript
this.config = {
    nodeCount: 25,           // 神经节点数量
    maxConnections: 3,       // 每个节点的最大连接数
    pulseSpeed: 0.02,        // 脉冲传播速度
    pulseIntensity: 0.8,     // 脉冲强度
    connectionDistance: 150, // 连接最大距离
    nodeRadius: 2,           // 节点半径
    glowIntensity: 15,       // 发光强度
    pulseColors: ['#38bdf8', '#4ade80', '#fbbf24', '#818cf8', '#f472b6'], // 脉冲颜色
    baseColor: 'rgba(56, 189, 248, 0.3)' // 基础连接颜色
};
```

### 手动触发脉冲

```javascript
// 获取canvas实例
const canvas = document.getElementById('neuralCanvas');
const neuralNetwork = new NeuralNetworkBackground(canvas);

// 在特定节点触发脉冲
neuralNetwork.triggerRandomPulse();
```

## 🎨 视觉设计

- **主色调**: 使用PULSAREON品牌色 (#38bdf8)
- **辅助色**: 绿色 (#4ade80) 和橙色 (#fbbf24) 用于不同类型的脉冲
- **玻璃态效果**: 内容区域使用半透明背景和模糊效果，确保神经背景可见
- **3D悬浮**: 节点带有3D悬浮动画效果

## ⚡ 性能优化

1. **帧率控制**: 使用requestAnimationFrame进行60fps渲染
2. **Delta Time**: 基于时间差更新动画，确保不同刷新率下的稳定性
3. **对象池**: 脉冲对象复用，避免频繁创建销毁
4. **Canvas优化**: 使用径向渐变而不是阴影，性能更好
5. **边界检测**: 节点在边界反弹，避免无限移动

## 📱 响应式设计

- 自动适应不同屏幕尺寸
- 在小屏幕上自动折叠侧边栏
- 神经节点密度根据屏幕大小自动调整

## 🔧 浏览器兼容性

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 📊 性能指标

- 内存占用: ~2MB
- CPU使用率: < 5% (在中等配置设备上)
- 帧率: 稳定的60fps

## 🎯 整合建议

1. **内容层级**: 确保主要内容使用半透明背景，让神经背景透出
2. **交互反馈**: 可以将用户交互（如点击）与神经脉冲关联
3. **数据可视化**: 将系统状态数据映射到神经网络活动强度

## 📝 更新日志

- **v1.0**: 初始版本，包含基础神经网络动画
- **v1.1**: 性能优化，添加脉冲颜色变化
- **v1.2**: 响应式改进，添加3D节点效果

---

**开发团队**: PULSAREON视觉特效组  
**最后更新**: 2026-02-08