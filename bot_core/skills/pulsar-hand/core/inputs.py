import pyautogui
import time
import random
from .overlay import overlay
from .config import Config

def click(button="left", double=False):
    x, y = pyautogui.position()
    action_name = "Double Click" if double else "Click"
    overlay.log(f"{action_name} ({button})")
    
    # Visual feedback: Active color
    overlay.update_cursor(x, y, active=True)
    
    # Pre-click hesitation
    time.sleep(random.uniform(0.02, 0.1))
    
    if double:
        pyautogui.doubleClick(button=button, interval=random.uniform(0.08, 0.15))
    else:
        pyautogui.mouseDown(button=button)
        time.sleep(random.uniform(0.04, 0.12)) # Realistic hold time
        pyautogui.mouseUp(button=button)
        
    # Visual feedback: Idle color
    overlay.update_cursor(x, y, active=False)

def type_text(text, interval=0.08):
    overlay.log(f"Typing {len(text)} chars...")
    
    for char in text:
        pyautogui.write(char)
        
        # Dynamic typing speed based on key distance (simulated variance)
        base_interval = interval
        if char == ' ': base_interval *= 1.2 # Space takes longer
        elif char.isupper(): base_interval *= 1.3 # Shift takes longer
        
        sleep_time = base_interval + random.uniform(-0.03, 0.03)
        if sleep_time < 0.01: sleep_time = 0.01
        
        time.sleep(sleep_time)
