import sys
import os
import argparse
import subprocess
import time
import pyautogui

# Fix Windows encoding for emojis
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

# Add path to PulsareonManipulator
manipulator_path = os.path.join(os.path.dirname(__file__), '../PulsareonManipulator')
sys.path.append(manipulator_path)

try:
    from core.movement import human_move
except ImportError:
    print("Error: Could not import PulsareonManipulator.core.movement")
    # Fallback to pyautogui direct move
    def human_move(x, y):
        pyautogui.moveTo(x, y, duration=0.5)

# Add path to system-utils
SCREENSHOT_SCRIPT = os.path.join(os.path.dirname(__file__), '../system-utils/scripts/screenshot.ps1')

import vision

def take_screenshot():
    try:
        # PowerShell command needs full path to script
        abs_script = os.path.abspath(SCREENSHOT_SCRIPT)
        path = subprocess.check_output(['powershell', '-File', abs_script]).decode().strip()
        return path
    except Exception as e:
        print(f"Screenshot failed: {e}")
        return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("instruction", help="What to find/do")
    parser.add_argument("--action", default="click", choices=["click", "hover", "type"])
    parser.add_argument("--text", help="Text to type")
    args = parser.parse_args()
    
    print(f"👁️ Analyzing screen for: {args.instruction}")
    
    # Retry loop for stability (handling popups/loading)
    max_retries = 3
    for attempt in range(max_retries):
        if attempt > 0:
            print(f"🔄 Retry {attempt+1}/{max_retries}...")
            
        img_path = take_screenshot()
        if not img_path or not os.path.exists(img_path):
            print("❌ Failed to take screenshot")
            return
            
        result = vision.analyze_screenshot(img_path, args.instruction)
        print(f"🤖 Vision result: {result}")
        
        if result.get('status') == 'FOUND':
            x, y = int(result['x']), int(result['y'])
            print(f"🖱️ Moving to ({x}, {y})...")
            
            # Human-like movement
            human_move(x, y)
            
            if args.action == "click":
                time.sleep(random.uniform(0.05, 0.15)) # Micro hesitation
                pyautogui.click()
            elif args.action == "type" and args.text:
                pyautogui.click()
                time.sleep(0.5)
                # Human typing
                for char in args.text:
                    pyautogui.write(char)
                    time.sleep(random.uniform(0.05, 0.15))
                time.sleep(0.5)
                pyautogui.press('enter')
            return # Success
            
        else:
            print("❌ Element not found.")
            if attempt < max_retries - 1:
                time.sleep(3) # Wait for UI/Popup
    
    print("❌ Failed to find element after retries.")

import random # Imported late but needed
if __name__ == "__main__":
    main()
