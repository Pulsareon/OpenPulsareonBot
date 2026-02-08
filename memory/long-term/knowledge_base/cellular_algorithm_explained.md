"""
细胞艺术 - 简化版本（易于理解）
"""
import numpy as np

# 想象画布是一个网格
# 2560行 x 1440列
# 每个格子有3个颜色值：红、绿、蓝

# 初始状态：随机放置一些"种子"
seeds = [
    {"x": 1000, "y": 700, "radius": 30, "color": [200, 100, 50]},  # 橙色
    {"x": 1500, "y": 900, "radius": 40, "color": [50, 150, 200]},  # 蓝色
    # ... 更多种子
]

# 进化循环（重复150次）
for generation in range(150):

    # 每一代，每个细胞都会：
    for seed in seeds:
        # 1. 生长 - 半径变大
        seed["radius"] += 1.5

        # 2. 失去生命力 - 生命值慢慢减小
        seed["life"] *= 0.99

        # 3. 可能分裂（当生命还充足时）
        if seed["life"] > 0.2 and random() < 0.03:
            new_seed = {
                "x": seed["x"] + 随机偏移,
                "y": seed["y"] + 随机偏移,
                "radius": seed["radius"] * 0.7,
                "color": 稍微变化,
                "life": seed["life"] * 0.8
            }
            seeds.append(new_seed)

    # 绘制：计算每个像素受到哪些细胞的影响
    # 距离细胞中心近的像素更亮
    # 多个细胞重叠的地方颜色混合
    绘制所有细胞到画布

# 保存图像
save_to_file(output.jpg)

# 结果：
# 初始：12个细胞
# 最终：56个细胞
# 最高世代：第5代
# 图像：美丽的光晕图案
