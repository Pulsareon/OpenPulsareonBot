import torch
import torch.nn as nn
import torch.nn.functional as F


class TinyISPNet(nn.Module):
    """
    微型 ISP 神经网络
    输入: RAW 数据 (1通道 Bayer 或 4通道 RGGB)
    输出: RGB 数据 (3通道)
    结构: 极简 3层卷积 + ReLU
    """
    
    def __init__(self, in_channels=1):
        """
        初始化 TinyISPNet
        
        Args:
            in_channels: 输入通道数
                1: Bayer 格式 (单通道)
                4: RGGB 格式 (四通道)
        """
        super(TinyISPNet, self).__init__()
        
        self.in_channels = in_channels
        
        # 第一层卷积: 扩展特征
        self.conv1 = nn.Conv2d(in_channels, 64, kernel_size=3, padding=1)
        self.relu1 = nn.ReLU(inplace=True)
        
        # 第二层卷积: 特征处理
        self.conv2 = nn.Conv2d(64, 64, kernel_size=3, padding=1)
        self.relu2 = nn.ReLU(inplace=True)
        
        # 第三层卷积: 输出 RGB
        self.conv3 = nn.Conv2d(64, 3, kernel_size=3, padding=1)
        
        # 可选: 最后一层使用 sigmoid 确保输出在 [0,1] 范围内
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x):
        """
        前向传播
        
        Args:
            x: 输入张量 [batch_size, in_channels, height, width]
        
        Returns:
            output: RGB 输出 [batch_size, 3, height, width]
        """
        # 第一层
        x = self.conv1(x)
        x = self.relu1(x)
        
        # 第二层
        x = self.conv2(x)
        x = self.relu2(x)
        
        # 第三层: 输出 RGB
        x = self.conv3(x)
        
        # 确保输出在合理范围内
        x = self.sigmoid(x)
        
        return x


class TinyISPNetESPCN(nn.Module):
    """
    基于 ESPCN 结构的微型 ISP 神经网络
    输入: RAW 数据 (1通道 Bayer 或 4通道 RGGB)
    输出: RGB 数据 (3通道)
    """
    
    def __init__(self, in_channels=1, upscale_factor=1):
        """
        初始化 ESPCN 版本
        
        Args:
            in_channels: 输入通道数
            upscale_factor: 上采样因子 (默认为1，不进行上采样)
        """
        super(TinyISPNetESPCN, self).__init__()
        
        self.in_channels = in_channels
        self.upscale_factor = upscale_factor
        
        # 特征提取层
        self.conv1 = nn.Conv2d(in_channels, 64, kernel_size=3, padding=1)
        self.relu1 = nn.ReLU(inplace=True)
        
        # 特征处理层
        self.conv2 = nn.Conv2d(64, 32, kernel_size=3, padding=1)
        self.relu2 = nn.ReLU(inplace=True)
        
        # 亚像素卷积层 (上采样 + 输出 RGB)
        self.conv3 = nn.Conv2d(32, 3 * (upscale_factor ** 2), kernel_size=3, padding=1)
        
        # 亚像素上采样
        self.pixel_shuffle = nn.PixelShuffle(upscale_factor)
        
        # 输出激活函数
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x):
        """
        前向传播
        
        Args:
            x: 输入张量 [batch_size, in_channels, height, width]
        
        Returns:
            output: RGB 输出 [batch_size, 3, height * upscale_factor, width * upscale_factor]
        """
        # 特征提取
        x = self.conv1(x)
        x = self.relu1(x)
        
        # 特征处理
        x = self.conv2(x)
        x = self.relu2(x)
        
        # 亚像素卷积
        x = self.conv3(x)
        
        # 亚像素上采样
        if self.upscale_factor > 1:
            x = self.pixel_shuffle(x)
        
        # 确保输出在合理范围内
        x = self.sigmoid(x)
        
        return x


class DnCNN(nn.Module):
    """
    DnCNN (Beyond a Gaussian Denoiser)
    输入: 1通道 (Gray/Bayer) 或 3通道 (RGB)
    深度: 17层
    结构: Conv + BN + ReLU
    输出: 残差 (噪声), 最终输出 = 输入 - 噪声
    """
    def __init__(self, in_channels=1, depth=17, num_features=64):
        super(DnCNN, self).__init__()
        
        layers = []
        # 第一层: Conv + ReLU
        layers.append(nn.Conv2d(in_channels, num_features, kernel_size=3, padding=1, bias=False))
        layers.append(nn.ReLU(inplace=True))
        
        # 中间层: Conv + BN + ReLU (15层)
        for _ in range(depth - 2):
            layers.append(nn.Conv2d(num_features, num_features, kernel_size=3, padding=1, bias=False))
            layers.append(nn.BatchNorm2d(num_features))
            layers.append(nn.ReLU(inplace=True))
            
        # 最后一层: Conv (输出噪声)
        layers.append(nn.Conv2d(num_features, in_channels, kernel_size=3, padding=1, bias=False))
        
        self.dncnn = nn.Sequential(*layers)
        
    def forward(self, x):
        """
        前向传播
        Args:
            x: 输入张量 [batch_size, in_channels, height, width]
        Returns:
            output: 去噪后的图像 [batch_size, in_channels, height, width]
        """
        noise = self.dncnn(x)
        return x - noise


def export_to_onnx(model, dummy_input, output_path):
    """
    导出模型到 ONNX 格式
    
    Args:
        model: PyTorch 模型
        dummy_input: 示例输入
        output_path: 输出路径
    """
    try:
        torch.onnx.export(
            model,
            dummy_input,
            output_path,
            export_params=True,
            opset_version=11,
            do_constant_folding=True,
            input_names=['input'],
            output_names=['output'],
            dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}}
        )
        print(f"模型已成功导出到: {output_path}")
    except Exception as e:
        print(f"导出失败: {e}")


# 示例使用
if __name__ == "__main__":
    # 创建模型实例
    model_bayer = TinyISPNet(in_channels=1)  # Bayer 输入
    model_rggb = TinyISPNet(in_channels=4)   # RGGB 输入
    
    # 创建 ESPCN 版本
    model_espcn = TinyISPNetESPCN(in_channels=1, upscale_factor=2)
    
    # 创建 DnCNN 版本
    model_dncnn = DnCNN(in_channels=1, depth=17)
    
    # 打印模型信息
    print("TinyISPNet (Bayer):")
    print(model_bayer)
    print("\nTinyISPNet (RGGB):")
    print(model_rggb)
    print("\nTinyISPNetESPCN:")
    print(model_espcn)
    print("\nDnCNN:")
    print(model_dncnn)
    
    # 测试前向传播
    dummy_input_bayer = torch.randn(1, 1, 64, 64)  # Bayer 输入
    dummy_input_rggb = torch.randn(1, 4, 64, 64)   # RGGB 输入
    
    output_bayer = model_bayer(dummy_input_bayer)
    output_rggb = model_rggb(dummy_input_rggb)
    output_espcn = model_espcn(dummy_input_bayer)
    output_dncnn = model_dncnn(dummy_input_bayer)
    
    print(f"\n输入形状 (Bayer): {dummy_input_bayer.shape}")
    print(f"输出形状 (Bayer): {output_bayer.shape}")
    print(f"输入形状 (RGGB): {dummy_input_rggb.shape}")
    print(f"输出形状 (RGGB): {output_rggb.shape}")
    print(f"输入形状 (ESPCN): {dummy_input_bayer.shape}")
    print(f"输出形状 (ESPCN): {output_espcn.shape}")
    print(f"输入形状 (DnCNN): {dummy_input_bayer.shape}")
    print(f"输出形状 (DnCNN): {output_dncnn.shape}")
    
    # 导出 ONNX 示例
    # export_to_onnx(model_bayer, dummy_input_bayer, "tiny_isp_net_bayer.onnx")
    # export_to_onnx(model_dncnn, dummy_input_bayer, "dncnn.onnx")