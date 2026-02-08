import cv2
import os

def scan_cameras():
    print("Scanning for available cameras...")
    found = []
    for i in range(5):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                path = f"E:/PulsareonThinker/captures/cam_test_{i}.jpg"
                cv2.imwrite(path, frame)
                print(f"Index {i}: Camera FOUND and active. Sample saved.")
                found.append(i)
            cap.release()
    return found

if __name__ == "__main__":
    active_cams = scan_cameras()
    if active_cams:
        print(f"Active indices: {active_cams}")
    else:
        print("No active cameras found.")
