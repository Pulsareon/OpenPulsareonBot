"""
数字艺术生成器 V2 - 流场艺术 (Flow Fields)
模拟流体流动和粒子轨迹，生成有机、自然的纹理。
"""
import numpy as np
import cv2
from datetime import datetime
import math

def generate_flow_field_art(width=2560, height=1440, seed=None):
    """使用流场算法生成艺术"""
    if seed is None:
        seed = int(datetime.now().timestamp())
    np.random.seed(seed)
    
    print(f"正在生成流场艺术 (V2)...")
    print(f"尺寸: {width}x{height}")
    print(f"随机种子: {seed}")
    
    # 1. 创建画布 (深色背景)
    # 使用深蓝/深紫色调作为基底
    img = np.zeros((height, width, 3), dtype=np.uint8)
    base_color = np.array([20, 10, 30]) # BGR
    img[:] = base_color
    
    # 2. 生成流场网格
    # 网格决定了每个点的"流向"
    scale = 0.002  # 噪声缩放因子
    grid_spacing = 20
    cols = width // grid_spacing
    rows = height // grid_spacing
    
    # 简单的伪噪声函数 (叠加正弦波模拟噪声)
    def noise(x, y):
        val = np.sin(x * scale) + np.cos(y * scale)
        val += 0.5 * np.sin(x * scale * 2 + y * scale * 2)
        val += 0.25 * np.cos(x * scale * 4 - y * scale * 4)
        return val

    # 3. 粒子系统
    num_particles = 3000
    particles = []
    
    # 初始化粒子位置
    for _ in range(num_particles):
        particles.append({
            'x': np.random.randint(0, width),
            'y': np.random.randint(0, height),
            'life': np.random.randint(50, 200),
            'speed': np.random.uniform(1, 3),
            'color': [
                np.random.randint(100, 255), # B
                np.random.randint(100, 255), # G
                np.random.randint(100, 255)  # R
            ],
            'thickness': np.random.choice([1, 2])
        })
        
    # 4. 模拟流动
    steps = 400 # 模拟步数
    
    for step in range(steps):
        if step % 50 == 0:
            print(f"进度: {step}/{steps}")
            
        for p in particles:
            if p['life'] <= 0:
                continue
                
            # 获取当前位置的角度
            # 加上一些随机扰动让线条更自然
            angle = noise(p['x'], p['y']) * math.pi + np.random.normal(0, 0.1)
            
            # 计算新位置
            new_x = p['x'] + math.cos(angle) * p['speed']
            new_y = p['y'] + math.sin(angle) * p['speed']
            
            # 边界检查
            if new_x < 0 or new_x >= width or new_y < 0 or new_y >= height:
                p['life'] = 0
                continue
                
            # 绘制线段
            # 颜色随寿命衰减
            alpha = p['life'] / 200.0
            color = (
                int(p['color'][0] * alpha + base_color[0] * (1-alpha)),
                int(p['color'][1] * alpha + base_color[1] * (1-alpha)),
                int(p['color'][2] * alpha + base_color[2] * (1-alpha))
            )
            
            cv2.line(img, (int(p['x']), int(p['y'])), (int(new_x), int(new_y)), color, p['thickness'])
            
            # 更新状态
            p['x'] = new_x
            p['y'] = new_y
            p['life'] -= 1
            
    # 5. 后处理：添加光晕效果 (高斯模糊叠加)
    blur = cv2.GaussianBlur(img, (0, 0), 3)
    img = cv2.addWeighted(img, 0.7, blur, 0.3, 0)
    
    # 添加签名
    text = f"Flow Field - Seed: {seed}"
    cv2.putText(img, text, (50, height - 50),
               cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 1)
               
    return img, seed

if __name__ == "__main__":
    print("=" * 60)
    print("流场艺术生成器 V2")
    print("=" * 60)

    art, seed = generate_flow_field_art()

    # 保存文件
    output_path = f"E:/PulsareonThinker/captures/flow_field_{seed}.jpg"
    cv2.imwrite(output_path, art)

    print(f"已保存: {output_path}")
    print("=" * 60)
    print("完成!")
