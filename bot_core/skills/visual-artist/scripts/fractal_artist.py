"""
数字艺术生成器 V3 - 分形宇宙 (Julia Set)
生成神秘的分形几何图案
"""
import numpy as np
import cv2
from datetime import datetime

def generate_julia_set(width=1920, height=1080, seed=None):
    if seed is None:
        seed = int(datetime.now().timestamp())
    np.random.seed(seed)
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 正在生成分形宇宙 (Seed: {seed})...")
    
    # 随机选择参数 c
    # Julia Set 的形状完全取决于 c 的值
    # 好的 c 值范围通常在 (-0.8, 0.156) 附近
    cx = np.random.uniform(-0.8, 0.4)
    cy = np.random.uniform(-0.6, 0.6)
    c = complex(cx, cy)
    
    print(f"参数 c = {c}")
    
    # 创建坐标网格
    x_min, x_max = -1.5, 1.5
    y_min, y_max = -1.0, 1.0
    
    # 调整比例适应屏幕
    aspect_ratio = width / height
    if aspect_ratio > 1:
        x_min *= aspect_ratio
        x_max *= aspect_ratio
    else:
        y_min /= aspect_ratio
        y_max /= aspect_ratio
        
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    
    # 广播生成复数网格
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    
    # 迭代计算
    max_iter = 100
    escape_radius = 2.0
    img = np.zeros(Z.shape, dtype=float)
    
    # 向量化迭代
    mask = np.ones(Z.shape, dtype=bool)
    
    for i in range(max_iter):
        Z[mask] = Z[mask] * Z[mask] + c
        escaped = np.abs(Z) > escape_radius
        
        # 记录逃逸时间
        newly_escaped = escaped & mask
        img[newly_escaped] = i
        
        mask = mask & ~escaped
        if not np.any(mask):
            break
            
    # 归一化并上色
    img = img / max_iter
    
    # 应用色彩映射
    # 使用 HSV 空间生成迷幻色彩
    h = (img * 180 + np.random.randint(0, 180)) % 180 # 色相
    s = np.ones_like(img) * 255 # 饱和度
    v = np.where(img > 0, 255, 0) # 亮度
    
    # 增加平滑过渡
    v = (np.sqrt(img) * 255).astype(np.uint8)
    
    hsv_img = np.dstack((h.astype(np.uint8), s.astype(np.uint8), v))
    bgr_img = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2BGR)
    
    # 添加签名
    text = f"Julia Set c={cx:.3f}+{cy:.3f}i"
    cv2.putText(bgr_img, text, (30, height - 30),
               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1)
               
    return bgr_img, seed

if __name__ == "__main__":
    art, seed = generate_julia_set()
    
    output_path = f"E:/PulsareonThinker/captures/fractal_{seed}.jpg"
    cv2.imwrite(output_path, art)
    print(f"分形艺术已保存: {output_path}")
