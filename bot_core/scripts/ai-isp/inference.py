"""
AI-ISP Inference Engine (ONNX Runtime)
Runs real model inference and validates results with metrics.
"""

import onnxruntime as ort
import numpy as np
import cv2
import time
import os
import sys

# 修复 Windows 编码
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

def calculate_sharpness(img):
    """计算图像清晰度 (Laplacian Variance)"""
    return cv2.Laplacian(img, cv2.CV_64F).var()

def run_inference(model_path="real_model.onnx", input_path="input_bayer.png"):
    print(f"🚀 Initializing Inference Engine...")
    
    # 1. Prepare Input
    if not os.path.exists(input_path):
        print(f"Generatng test input: {input_path}")
        # Generate a fuzzy image to test sharpening
        # Create random noise + Gaussian Blur
        noise = np.random.randint(0, 255, (512, 512), dtype=np.uint8)
        blurred = cv2.GaussianBlur(noise, (5, 5), 0)
        cv2.imwrite(input_path, blurred)
    
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Error: Failed to load image.")
        return

    # Preprocess: (H,W) -> (1,1,H,W), Norm [0,1]
    input_tensor = img.astype(np.float32) / 255.0
    input_tensor = input_tensor.reshape(1, 1, img.shape[0], img.shape[1])
    
    # 2. Load Model
    if not os.path.exists(model_path):
        print(f"Error: Model {model_path} not found. Run create_real_model.py first.")
        return

    session = ort.InferenceSession(model_path)
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    
    print(f"Model: {model_path}")
    print(f"Input: {input_name} {input_tensor.shape}")
    
    # 3. Inference
    t0 = time.perf_counter()
    outputs = session.run([output_name], {input_name: input_tensor})
    t1 = time.perf_counter()
    
    print(f"⏱️ Time: {(t1-t0)*1000:.2f} ms")
    
    # 4. Postprocess
    output_tensor = outputs[0]
    output_img = np.clip(output_tensor * 255.0, 0, 255).astype(np.uint8)
    output_img = output_img.reshape(img.shape[0], img.shape[1])
    
    cv2.imwrite("output.png", output_img)
    print("✅ Output saved to output.png")
    
    # 5. Validation (Data Evidence)
    score_in = calculate_sharpness(img)
    score_out = calculate_sharpness(output_img)
    improvement = (score_out / score_in - 1) * 100 if score_in > 0 else 0
    
    print("\n📊 Validation Metrics (Data Evidence):")
    print(f"   Input Sharpness:  {score_in:.2f}")
    print(f"   Output Sharpness: {score_out:.2f}")
    print(f"   Improvement:      {improvement:+.1f}%")
    
    if improvement > 0:
        print("✅ Result: Image successfully sharpened.")
    else:
        print("⚠️ Result: No improvement detected.")

if __name__ == "__main__":
    model = "real_model.onnx"
    image = "input_bayer.png"
    
    if len(sys.argv) > 1:
        # Check if arg is model or image
        if sys.argv[1].endswith(".onnx"):
            model = sys.argv[1]
        else:
            image = sys.argv[1]
            
    if len(sys.argv) > 2:
        image = sys.argv[2]
        
    run_inference(model, image)
