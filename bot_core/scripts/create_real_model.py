import onnx
from onnx import helper, TensorProto
import numpy as np

# 创建图像锐化ONNX模型

def create_sharpening_model():
    # 1. 定义输入和输出 tensor value info
    # 输入格式: [batch_size, channels, height, width]
    input_tensor = helper.make_tensor_value_info(
        'input', TensorProto.FLOAT, [1, 1, None, None]  # H和W可以是任意大小
    )
    
    output_tensor = helper.make_tensor_value_info(
        'output', TensorProto.FLOAT, [1, 1, None, None]
    )
    
    # 2. 定义锐化卷积核权重 (锐化算子)
    # 锐化滤波器: [[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]
    kernel_weights = np.array([
        [[[-1.0, -1.0, -1.0],
          [-1.0,  9.0, -1.0],
          [-1.0, -1.0, -1.0]]]
    ], dtype=np.float32)
    
    # 创建权重 initializer
    kernel_tensor = helper.make_tensor(
        name='kernel',
        data_type=TensorProto.FLOAT,
        dims=[1, 1, 3, 3],  # [output_channels, input_channels, height, width]
        vals=kernel_weights.flatten().tolist()
    )
    
    # 3. 创建卷积节点
    conv_node = helper.make_node(
        'Conv',
        inputs=['input', 'kernel'],
        outputs=['output'],
        name='conv_sharpen',
        # 设置卷积属性
        kernel_shape=[3, 3],
        pads=[1, 1, 1, 1],  # 上下左右各填充1像素
        strides=[1, 1]
    )
    
    # 4. 构建计算图
    graph = helper.make_graph(
        nodes=[conv_node],
        name='sharpening_model',
        inputs=[input_tensor],
        outputs=[output_tensor],
        initializer=[kernel_tensor]
    )
    
    # 5. 创建模型
    model = helper.make_model(
        graph,
        producer_name='onnx-sharpening-model',
        opset_imports=[helper.make_opsetid('', 13)]
    )
    
    return model

def create_edge_detection_model():
    """创建边缘检测模型（拉普拉斯算子）"""
    # 1. 定义输入和输出 tensor value info
    input_tensor = helper.make_tensor_value_info(
        'input', TensorProto.FLOAT, [1, 1, None, None]
    )
    
    output_tensor = helper.make_tensor_value_info(
        'output', TensorProto.FLOAT, [1, 1, None, None]
    )
    
    # 2. 定义拉普拉斯边缘检测卷积核
    # 拉普拉斯算子: [[0,1,0], [1,-4,1], [0,1,0]]
    kernel_weights = np.array([
        [[[0.0,  1.0, 0.0],
          [1.0, -4.0, 1.0],
          [0.0,  1.0, 0.0]]]
    ], dtype=np.float32)
    
    # 创建权重 initializer
    kernel_tensor = helper.make_tensor(
        name='kernel',
        data_type=TensorProto.FLOAT,
        dims=[1, 1, 3, 3],
        vals=kernel_weights.flatten().tolist()
    )
    
    # 3. 创建卷积节点
    conv_node = helper.make_node(
        'Conv',
        inputs=['input', 'kernel'],
        outputs=['output'],
        name='conv_edge',
        kernel_shape=[3, 3],
        pads=[1, 1, 1, 1],
        strides=[1, 1]
    )
    
    # 4. 构建计算图
    graph = helper.make_graph(
        nodes=[conv_node],
        name='edge_detection_model',
        inputs=[input_tensor],
        outputs=[output_tensor],
        initializer=[kernel_tensor]
    )
    
    # 5. 创建模型
    model = helper.make_model(
        graph,
        producer_name='onnx-edge-detection-model',
        opset_imports=[helper.make_opsetid('', 13)]
    )
    
    return model

if __name__ == "__main__":
    # 创建锐化模型
    sharpening_model = create_sharpening_model()
    
    # 保存模型
    onnx.save(sharpening_model, "real_model.onnx")
    print("锐化模型已保存为 'real_model.onnx'")
    
    # 可选：创建边缘检测模型
    edge_model = create_edge_detection_model()
    onnx.save(edge_model, "edge_model.onnx")
    print("边缘检测模型已保存为 'edge_model.onnx'")
    
    print("\n模型信息:")
    print(f"锐化模型输入形状: {sharpening_model.graph.input[0]}")
    print(f"锐化模型输出形状: {sharpening_model.graph.output[0]}")
    print(f"卷积核权重形状: [1, 1, 3, 3]")
    print("锐化滤波器: [[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]")