import torch
from model import TinyISPNet

def main():
    # 1. 初始化模型
    # 根据 dummy input 1x1x512x512，in_channels 应为 1
    model = TinyISPNet(in_channels=1)
    model.eval()  # 设置为推理模式

    # 2. 创建 dummy input (1x1x512x512)
    dummy_input = torch.randn(1, 1, 512, 512)

    # 3. 设置导出路径
    onnx_path = "tiny_isp.onnx"

    # 4. 使用 torch.onnx.export 导出
    print(f"正在导出模型到 {onnx_path}...")
    torch.onnx.export(
        model,
        dummy_input,
        onnx_path,
        export_params=True,        # 导出训练后的参数权重
        opset_version=11,          # ONNX 算子集版本
        do_constant_folding=True,  # 是否执行常量折叠优化
        input_names=['input'],     # 输入节点名称
        output_names=['output'],   # 输出节点名称
        dynamic_axes={             # 启用动态轴（可选，增加通用性）
            'input': {0: 'batch_size', 2: 'height', 3: 'width'},
            'output': {0: 'batch_size', 2: 'height', 3: 'width'}
        }
    )
    
    print("导出完成！")

if __name__ == "__main__":
    main()
