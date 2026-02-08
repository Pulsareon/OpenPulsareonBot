import cv2
import sys
import os

def take_photo(output_path):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return False
    
    # 丢弃前几帧以校准曝光
    for _ in range(10):
        cap.read()
        
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(output_path, frame)
        print(f"Photo saved to {output_path}")
    else:
        print("Error: Could not capture image.")
    
    cap.release()
    return ret

if __name__ == "__main__":
    output = "E:/PulsareonThinker/captures/partner_view.jpg"
    take_photo(output)
