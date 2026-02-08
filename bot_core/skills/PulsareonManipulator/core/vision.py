import pyautogui
import cv2
import numpy as np
import time

def find_image(image_path, confidence=0.8):
    """Find image on screen."""
    try:
        location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        if location:
            return pyautogui.center(location)
    except Exception as e:
        print(f"Vision Error: {e}")
    return None

def find_color(rgb_color, tolerance=10):
    """Find color (r,g,b) on screen. (Slow scan, use carefully)"""
    # Optimized: Take screenshot and use numpy
    img = pyautogui.screenshot()
    img_np = np.array(img)
    
    # Calculate distance
    target = np.array(rgb_color)
    diff = np.abs(img_np[:, :, :3] - target)
    mask = np.all(diff <= tolerance, axis=2)
    
    coords = np.argwhere(mask)
    if coords.size > 0:
        # Return first match (y, x) -> (x, y)
        y, x = coords[0]
        return x, y
    return None

def find_text(text):
    """OCR stub. Requires tesseract/easyocr."""
    print("OCR not implemented yet.")
    return None