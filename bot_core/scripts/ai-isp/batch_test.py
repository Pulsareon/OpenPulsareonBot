"""
Batch Test & Visualization
下载真实图片（包括 Raw-like 16bit），运行 AI-ISP，生成对比图。
"""

import os
import cv2
import requests
import numpy as np
import onnxruntime as ort

# URL List
URLS = [
    ("landscape", "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=512&q=60"),
    ("city", "https://images.unsplash.com/photo-1449824913929-4bddafe9b3f9?w=512&q=60"),
    ("portrait", "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=512&q=60"),
    ("texture", "https://images.unsplash.com/photo-1550684848-fac1c5b4e853?w=512&q=60"),
    # 16-bit Bayer PNG (Simulated RAW)
    ("bayer_16bit", "https://raw.githubusercontent.com/embed-dsp/edsp/master/test_data/images/bayer_16bit.png")
]

MODEL_PATH = "real_model.onnx"
OUTPUT_DIR = "results"

def download_image(url, name):
    print(f"Downloading {name}...")
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            ext = url.split('.')[-1]
            if len(ext) > 4: ext = "jpg"
            path = f"{name}_original.{ext}"
            with open(path, 'wb') as f:
                f.write(r.content)
            return path
    except Exception as e:
        print(f"Download failed: {e}")
    return None

def process_image(img_path, model_session):
    print(f"Processing {img_path}...")
    
    # 尝试以无损模式读取
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    
    if img is None:
        print(f"Failed to read {img_path}")
        return None
        
    # 处理 16-bit
    if img.dtype == np.uint16:
        print("  Detected 16-bit image, normalizing to 8-bit for model...")
        img = (img / 256).astype(np.uint8)
        
    # 转灰度
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Preprocess
    input_tensor = img.astype(np.float32) / 255.0
    input_tensor = input_tensor.reshape(1, 1, img.shape[0], img.shape[1])
    
    # Inference
    try:
        input_name = model_session.get_inputs()[0].name
        output_name = model_session.get_outputs()[0].name
        outputs = model_session.run([output_name], {input_name: input_tensor})
        
        # Postprocess
        output_img = np.clip(outputs[0] * 255.0, 0, 255).astype(np.uint8)
        output_img = output_img.reshape(img.shape[0], img.shape[1])
        return output_img
    except Exception as e:
        print(f"Inference failed: {e}")
        return None

def make_comparison(original_path, processed_img, name):
    original = cv2.imread(original_path, cv2.IMREAD_GRAYSCALE)
    if original is None:
        # Fallback for 16-bit or other formats
        original = cv2.imread(original_path, cv2.IMREAD_UNCHANGED)
        if original.dtype == np.uint16:
            original = (original / 256).astype(np.uint8)
        if len(original.shape) == 3:
            original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
            
    # Resize to match
    if original.shape != processed_img.shape:
        processed_img = cv2.resize(processed_img, (original.shape[1], original.shape[0]))
        
    h, w = original.shape
    canvas = np.zeros((h + 40, w * 2, 3), dtype=np.uint8)
    
    orig_bgr = cv2.cvtColor(original, cv2.COLOR_GRAY2BGR)
    proc_bgr = cv2.cvtColor(processed_img, cv2.COLOR_GRAY2BGR)
    
    canvas[40:, :w] = orig_bgr
    canvas[40:, w:] = proc_bgr
    
    cv2.putText(canvas, "Original", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(canvas, "AI-ISP Output", (w + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    save_path = f"{OUTPUT_DIR}/compare_{name}.jpg"
    cv2.imwrite(save_path, canvas)
    print(f"[OK] Comparison saved: {save_path}")

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    try:
        session = ort.InferenceSession(MODEL_PATH)
    except Exception as e:
        print(f"Model load failed: {e}")
        return
    
    for name, url in URLS:
        path = download_image(url, name)
        if path:
            result = process_image(path, session)
            if result is not None:
                make_comparison(path, result, name)
            
            # Clean up original
            try: os.remove(path)
            except: pass

if __name__ == "__main__":
    main()
