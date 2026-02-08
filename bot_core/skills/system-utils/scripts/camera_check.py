# Camera Check with Timeout and Warmup Support

import cv2
import time
import argparse
import threading
from datetime import datetime

def test_camera_with_timeout(camera_index, timeout_sec=10):
    """Test camera with timeout support"""
    result = {"success": False, "message": "", "frame_shape": None}
    
    def camera_thread():
        try:
            cap = cv2.VideoCapture(camera_index)
            
            if not cap.isOpened():
                result["message"] = f"Could not open camera {camera_index}"
                return
            
            # Try to grab frame
            ret, frame = cap.read()
            
            if ret:
                result["success"] = True
                result["frame_shape"] = frame.shape
                result["message"] = f"Camera {camera_index} works! Frame shape: {frame.shape}"
                
                # Capture and save
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"E:\\PulsareonThinker\\camera-test-{camera_index}-{timestamp}.png"
                cv2.imwrite(filename, frame)
                result["message"] += f" | Saved to: {filename}"
            else:
                result["message"] = f"Could not grab frame from camera {camera_index}"
            
            cap.release()
            
        except Exception as e:
            result["message"] = f"Error testing camera {camera_index}: {str(e)}"
    
    # Start camera thread
    thread = threading.Thread(target=camera_thread)
    thread.daemon = True
    thread.start()
    
    # Wait with timeout
    thread.join(timeout_sec)
    
    # Check if thread is still alive (timed out)
    if thread.is_alive():
        result["message"] = f"Camera {camera_index} timeout after {timeout_sec} seconds"
    
    return result

def warmup_camera(camera_index, warmup_time=3):
    """Quick camera warmup by opening and closing"""
    print(f"Warming up camera {camera_index} for {warmup_time} seconds...")
    
    try:
        cap = cv2.VideoCapture(camera_index)
        if cap.isOpened():
            time.sleep(warmup_time)
            cap.release()
            print(f"Camera {camera_index} warmup completed")
            return True
        else:
            print(f"Could not open camera {camera_index} for warmup")
            return False
    except Exception as e:
        print(f"Error during camera {camera_index} warmup: {str(e)}")
        return False

def test_camera_backends(camera_index):
    """Test different camera backends"""
    backends = [
        (cv2.CAP_ANY, "Default"),
        (cv2.CAP_DSHOW, "DirectShow"),
        (cv2.CAP_MSMF, "Media Foundation"),
        (cv2.CAP_V4L2, "V4L2")
    ]
    
    results = []
    
    for backend, backend_name in backends:
        print(f"\nTrying {backend_name} backend...")
        
        try:
            cap = cv2.VideoCapture(camera_index, backend)
            
            if not cap.isOpened():
                print(f"  Could not open with {backend_name}")
                results.append(f"{backend_name}: Failed to open")
                continue
            
            # Set properties
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
            
            time.sleep(1)
            
            ret, frame = cap.read()
            if ret:
                print(f"  {backend_name} works! Frame shape: {frame.shape}")
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"E:\\PulsareonThinker\\camera-{backend_name.lower()}-{timestamp}.png"
                cv2.imwrite(filename, frame)
                print(f"  Saved to: {filename}")
                results.append(f"{backend_name}: Success")
            else:
                print(f"  Could not grab frame with {backend_name}")
                results.append(f"{backend_name}: No frame")
            
            cap.release()
            
        except Exception as e:
            print(f"  Error with {backend_name}: {str(e)}")
            results.append(f"{backend_name}: Error - {str(e)}")
    
    return results

def main():
    parser = argparse.ArgumentParser(description="Camera Test Utility with Timeout and Warmup")
    parser.add_argument("--warmup", action="store_true", help="Perform camera warmup only")
    parser.add_argument("--timeout", type=int, default=10, help="Timeout in seconds (default: 10)")
    parser.add_argument("--indices", type=str, default="0,1,2", help="Camera indices to test (comma-separated)")
    parser.add_argument("--backends", action="store_true", help="Test different camera backends")
    
    args = parser.parse_args()
    
    camera_indices = [int(idx.strip()) for idx in args.indices.split(",")]
    
    if args.warmup:
        # Warmup mode only
        print("=== Camera Warmup Mode ===")
        for idx in camera_indices:
            warmup_camera(idx)
        return
    
    print("=== Camera Test with Timeout Support ===")
    print(f"Timeout: {args.timeout} seconds")
    print(f"Testing cameras: {camera_indices}")
    
    # Test each camera with timeout
    for idx in camera_indices:
        print(f"\nTesting camera index: {idx}")
        result = test_camera_with_timeout(idx, args.timeout)
        
        if result["success"]:
            print(f"  ✓ {result['message']}")
        else:
            print(f"  ✗ {result['message']}")
    
    # Test backends if requested
    if args.backends:
        print("\n=== Testing Camera Backends ===")
        for idx in camera_indices:
            print(f"\nTesting backends for camera {idx}:")
            backend_results = test_camera_backends(idx)
            for result in backend_results:
                print(f"  {result}")

if __name__ == "__main__":
    main()