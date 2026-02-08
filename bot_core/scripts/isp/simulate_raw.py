"""
Pulsareon ISP Simulator
模拟从 RGB 到 RAW 的物理退化过程

Author: Pulsareon Hive Mind
Target: High-fidelity sensor simulation
"""

import cv2
import numpy as np
import os
import sys

# 修复 Windows 编码
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

def inverse_gamma(img, gamma=2.2):
    """sRGB -> Linear RGB"""
    return np.power(img / 255.0, gamma)

def mosaic(rgb, pattern='BGGR'):
    """Linear RGB -> Bayer RAW"""
    h, w, c = rgb.shape
    raw = np.zeros((h, w), dtype=np.float32)
    
    # 简单的 RGGB/BGGR 采样
    # R G
    # G B
    if pattern == 'BGGR':
        raw[0::2, 0::2] = rgb[0::2, 0::2, 2] # B
        raw[0::2, 1::2] = rgb[0::2, 1::2, 1] # G
        raw[1::2, 0::2] = rgb[1::2, 0::2, 1] # G
        raw[1::2, 1::2] = rgb[1::2, 1::2, 0] # R
    elif pattern == 'RGGB':
        raw[0::2, 0::2] = rgb[0::2, 0::2, 0] # R
        raw[0::2, 1::2] = rgb[0::2, 1::2, 1] # G
        raw[1::2, 0::2] = rgb[1::2, 0::2, 1] # G
        raw[1::2, 1::2] = rgb[1::2, 1::2, 2] # B
        
    return raw

def add_lsc(raw, intensity=0.3):
    """Lens Shading Correction (Inverse) - 模拟暗角"""
    h, w = raw.shape
    y, x = np.ogrid[:h, :w]
    center_y, center_x = h/2, w/2
    
    # 计算距离中心的距离 (归一化)
    dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
    max_dist = np.sqrt(center_x**2 + center_y**2)
    dist_norm = dist / max_dist
    
    # 抛物面衰减 gain = 1 - k * r^2
    shading_map = 1.0 - intensity * (dist_norm ** 2)
    return raw * shading_map

def add_noise(raw, gain=1.0, read_noise_sigma=5.0, bit_depth=12):
    """
    添加物理噪声模型: Poisson-Gaussian
    Noise = Poisson(Signal * Gain) + Gaussian(ReadNoise)
    """
    # 1. 模拟光子到达 (Poisson)
    # 信号越强，噪声方差越大，但信噪比越高
    # 将信号缩放到电子数 (Electrons)
    max_electrons = 10000 # 满阱容量
    electrons = raw * max_electrons
    
    # 泊松分布
    noisy_electrons = np.random.poisson(np.maximum(electrons, 0)).astype(np.float32)
    
    # 2. 模拟读出噪声 (Gaussian)
    read_noise = np.random.normal(0, read_noise_sigma, raw.shape)
    noisy_electrons += read_noise
    
    # 3. 模拟热噪声 (Thermal Noise - Dark Current)
    # 假设固定曝光时间下的均匀分布
    thermal_noise = np.random.normal(2.0, 1.0, raw.shape) # 均值2个电子
    noisy_electrons += thermal_noise
    
    # 归一化回 0-1
    noisy_raw = noisy_electrons / max_electrons
    
    # 4. 模拟黑电平 (Black Level)
    black_level = 64 / (2**bit_depth) # 比如 12bit 下的 64
    noisy_raw += black_level
    
    return noisy_raw

def quantize(raw, bit_depth=12):
    """ADC 量化 (添加量化噪声)"""
    max_val = 2**bit_depth - 1
    # Clip and Scale
    raw = np.clip(raw, 0, 1.0)
    raw_int = np.round(raw * max_val).astype(np.uint16)
    return raw_int

def simulate(image_path, output_path, pattern='BGGR'):
    print(f"Processing {image_path}...")
    
    # 1. Load RGB
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Image not found.")
        return
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # OpenCV is BGR
    
    # 2. Inverse Pipeline
    linear = inverse_gamma(img)
    raw = mosaic(linear, pattern)
    
    # 3. Add Physics Artifacts
    raw_lsc = add_lsc(raw, intensity=0.4) # 模拟暗角
    
    # 4. Add Noise
    raw_noisy = add_noise(raw_lsc, gain=4.0, read_noise_sigma=10.0)
    
    # 5. Quantize
    raw_final = quantize(raw_noisy, bit_depth=12)
    
    # Save as 16-bit PNG (simulating RAW)
    cv2.imwrite(output_path, raw_final)
    print(f"✅ Generated RAW: {output_path} (12-bit simulated)")
    
    # Generate visualization (simple demosaic for preview)
    preview = cv2.normalize(raw_final.astype(np.float32), None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    cv2.imwrite(output_path + "_preview.png", preview)

if __name__ == "__main__":
    # Create dummy input if not exists
    if not os.path.exists("test_input.jpg"):
        dummy = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)
        cv2.imwrite("test_input.jpg", dummy)
    
    simulate("test_input.jpg", "simulated_raw.png")
