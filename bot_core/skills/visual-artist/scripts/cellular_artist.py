"""
细胞艺术生成器 - 基于元胞自动机的艺术作品
"""
import numpy as np
import cv2
from datetime import datetime

def cell_automata_art(width=2560, height=1440, num_cells=15, generations=100):
    """
    基于细胞分裂和生长的艺术生成
    """

    print("=" * 60)
    print("细胞艺术生成器")
    print("=" * 60)
    print(f"画布尺寸: {width}x{height}")
    print(f"初始细胞数: {num_cells}")
    print(f"进化代数: {generations}")
    print()

    # 创建画布 - 深色背景
    canvas = np.zeros((height, width, 3), dtype=np.float32)

    # 细胞属性：中心(x,y), 半径, 生长速度, 颜色(r,g,b), 透明度
    cells = []

    # 初始化细胞
    for i in range(num_cells):
        cell = {
            'x': np.random.randint(0, width),
            'y': np.random.randint(0, height),
            'radius': np.random.uniform(10, 50),
            'growth_rate': np.random.uniform(0.5, 3.0),
            'color': np.random.uniform(0.2, 0.8, 3),  # 归一化RGB
            'alpha': np.random.uniform(0.1, 0.4),
            'life': np.random.uniform(0.5, 1.0),  # 生命值，影响是否分裂
            'generation': 0
        }
        cells.append(cell)

    print(f"初始化 {num_cells} 个原始细胞...")

    # 进化过程
    for gen in range(generations):
        new_cells = []

        # 绘制当前所有细胞
        for cell in cells:
            # 创建坐标网格
            y = np.arange(height)
            x = np.arange(width)
            xx, yy = np.meshgrid(x, y)

            # 计算到细胞中心的距离
            dist_from_center = np.sqrt((xx - cell['x'])**2 + (yy - cell['y'])**2)

            # 细胞的光晕效果
            cell_shape = np.exp(-(dist_from_center**2) / (2 * cell['radius']**2))

            # 混合到画布上
            for c in range(3):
                canvas[:, :, c] += cell_shape * cell['color'][c] * cell['alpha']

        # 细胞生长和分裂
        for cell in cells:
            cell['radius'] += cell['growth_rate']
            cell['life'] *= 0.99  # 生命衰减

            # 分裂条件：生命值足够高且有概率
            if (cell['life'] > 0.2 and
                np.random.random() < 0.03 and
                len(cells) + len(new_cells) < 100):  # 限制总数

                # 创建新细胞（变异）
                offset_dist = cell['radius'] * 0.8
                angle = np.random.uniform(0, 2 * np.pi)

                new_cell = {
                    'x': cell['x'] + offset_dist * np.cos(angle),
                    'y': cell['y'] + offset_dist * np.sin(angle),
                    'radius': max(5, cell['radius'] * 0.7),
                    'growth_rate': cell['growth_rate'] * np.random.uniform(0.8, 1.2),
                    'color': np.clip(cell['color'] * np.random.uniform(0.9, 1.1), 0, 1),
                    'alpha': min(0.3, cell['alpha'] * 0.9),
                    'life': cell['life'] * 0.8,
                    'generation': cell['generation'] + 1
                }

                # 确保新细胞在画布内
                new_cell['x'] = np.clip(new_cell['x'], 0, width)
                new_cell['y'] = np.clip(new_cell['y'], 0, height)

                new_cells.append(new_cell)
                cell['life'] *= 0.5  # 分裂后生命减半

        cells.extend(new_cells)

    # 归一化并转换为uint8
    canvas = np.clip(canvas * 255, 0, 255).astype(np.uint8)

    print(f"进化完成！最终细胞数: {len(cells)}")
    print(f"最高世代: {max(c['generation'] for c in cells)}")

    # 添加标题和签名
    seed = int(datetime.now().timestamp())
    text_top = f"Cellular Evolution Art"
    text_bottom = f"Cells: {len(cells)} | Generations: {generations} | Seed: {seed}"

    cv2.putText(canvas, text_top, (50, 80),
               cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    cv2.putText(canvas, text_top, (50, 80),
               cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 1)

    cv2.putText(canvas, text_bottom, (50, height - 50),
               cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(canvas, text_bottom, (50, height - 50),
               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)

    print("=" * 60)

    return canvas, seed, len(cells)

# 运行
art, seed, final_cells = cell_automata_art(
    width=2560,
    height=1440,
    num_cells=12,
    generations=150
)

# 保存
output_path = f"E:/PulsareonThinker/captures/cellular_art_{seed}_{final_cells}.jpg"
cv2.imwrite(output_path, art)

print(f"细胞艺术已保存: {output_path}")
print("完成!")
