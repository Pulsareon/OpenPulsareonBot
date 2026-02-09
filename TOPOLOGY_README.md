# Pulsareon Hive 交互式拓扑图

## 概述

本项目包含三个版本的交互式拓扑图，将静态拓扑数据重构为具有呼吸灯效果和点击交互功能的可视化界面。

## 文件说明

### 1. `topology_interactive.html`
**完整HTML版本** - 使用纯HTML/CSS/JavaScript实现
- ✅ 完整的呼吸灯动画效果
- ✅ 点击节点显示详细信息弹窗
- ✅ 动态连接线脉冲效果
- ✅ 响应式设计
- ✅ 完整的图例系统

### 2. `topology_svg.html`
**SVG集成版本** - 使用SVG内嵌在HTML中
- ✅ SVG图形渲染
- ✅ 呼吸灯CSS动画
- ✅ 点击交互功能
- ✅ 简洁的界面设计
- ✅ 优化的性能

### 3. `topology_interactive.svg`
**纯SVG版本** - 独立的SVG文件
- ✅ 纯SVG实现
- ✅ 内嵌JavaScript交互
- ✅ 渐变和滤镜效果
- ✅ 可直接嵌入网页
- ✅ 轻量级解决方案

## 功能特性

### 🌟 呼吸灯效果
- 所有节点都具有呼吸动画效果
- 连接线具有脉冲数据传输效果
- 悬停时节点亮度提升

### 🖱️ 交互功能
- 点击节点显示详细信息
- 包括名称、类型、角色、状态、负载等信息
- 模态对话框显示完整参数

### 🎨 视觉设计
- 渐变色彩区分节点类型
  - **Overmind**: 红色渐变 (主脑)
  - **Governor**: 青色渐变 (治理者)  
  - **Executor**: 紫色渐变 (执行器)
- 状态标识颜色编码
  - 🟢 Active: 运行中
  - 🟡 Standby: 待命
  - 🔵 Monitoring: 监控中
  - ⚫ Idle: 空闲
  - 🟢 Running: 执行中
  - 🔴 Alert: 警报

### 📊 拓扑结构
基于实际系统数据：
- 1个 Overmind (Google Gemini)
- 2个 Governors (DeepSeek v3.1, Moonshot V1)
- 3个 Executors (Git-Sync, Web-Sync, Safety-Guardian)

## 使用方法

### 网页版本
```bash
# 直接在浏览器中打开
open topology_interactive.html
# 或
open topology_svg.html
```

### SVG版本
```html
<!-- 嵌入网页 -->
<object data="topology_interactive.svg" type="image/svg+xml"></object>

<!-- 或直接链接 -->
<a href="topology_interactive.svg">查看拓扑图</a>
```

### 部署
所有文件都是静态资源，可直接部署到任何web服务器：
- Apache/Nginx
- GitHub Pages
- Netlify/Vercel
- 本地文件系统

## 技术栈

- **HTML5/CSS3**: 结构和样式
- **JavaScript**: 交互逻辑
- **SVG**: 矢量图形渲染
- **CSS Animations**: 呼吸灯效果
- **ES6**: 现代JavaScript语法

## 浏览器支持

- ✅ Chrome 60+
- ✅ Firefox 55+
- ✅ Safari 12+
- ✅ Edge 79+
- ✅ Mobile browsers

## 自定义配置

### 修改节点数据
编辑对应文件中的JavaScript数据对象：
```javascript
const topologyData = {
    overmind: { /* ... */ },
    governors: [ /* ... */ ],
    executors: [ /* ... */ ]
};
```

### 调整样式
修改CSS变量和样式规则：
```css
.node.overmind {
    background: linear-gradient(135deg, #your-color-1, #your-color-2);
}
```

### 添加新节点类型
1. 在HTML中添加新的CSS类
2. 在JavaScript中添加数据
3. 更新图例系统

## 性能优化

- 使用CSS动画代替JavaScript动画
- SVG矢量图形确保清晰度
- 响应式设计适配不同屏幕
- 轻量级代码结构

## 扩展功能

可考虑的扩展功能：
- [ ] 实时数据更新
- [ ] 拖拽节点位置
- [ ] 拓扑结构编辑
- [ ] 数据导出功能
- [ ] 多主题支持

## 许可证

MIT License - 可自由使用和修改

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。