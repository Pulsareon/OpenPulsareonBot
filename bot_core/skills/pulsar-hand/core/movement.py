import pyautogui
import math
import random
import time
from .overlay import overlay
from .config import Config

# Disable PyAutoGUI fail-safe
pyautogui.FAILSAFE = False 

def human_wind_mouse(start_x, start_y, dest_x, dest_y, speed=None):
    """
    Simulates human mouse movement using gravity/wind algorithm.
    """
    if speed is None: speed = Config.MOUSE_SPEED_DEFAULT
    
    G_0 = Config.GRAVITY
    W_0 = Config.WIND
    D_0 = 12
    
    current_x, current_y = start_x, start_y
    v_x = v_y = W_x = W_y = 0
    
    dist = math.hypot(dest_x - start_x, dest_y - start_y)
    
    # Adaptive speed: faster for long distance, slower for precision
    adaptive_speed = max(0.1, min(1.5, dist / 800.0)) * speed
    
    steps = int(dist / (8 * adaptive_speed))
    if steps < 15: steps = 15 # Minimum frames
    
    sqrt2 = math.sqrt(2)
    sqrt3 = math.sqrt(3)
    sqrt5 = math.sqrt(5)
    
    for i in range(1, steps + 1):
        dist = math.hypot(dest_x - current_x, dest_y - current_y)
        
        # Gravity (pull to target)
        if dist < D_0: D = D_0
        else: D = dist

        # Wind (random noise)
        wind = min(W_0, dist)
        
        if dist >= D_0:
            W_x = W_x / sqrt3 + (random.random() * (wind * 2 + 1) - wind) / sqrt5
            W_y = W_y / sqrt3 + (random.random() * (wind * 2 + 1) - wind) / sqrt5
        else:
            W_x /= sqrt2
            W_y /= sqrt2

        v_x += W_x + (dest_x - current_x) * G_0 / D
        v_y += W_y + (dest_y - current_y) * G_0 / D

        if dist < D_0:
            v_x /= 2
            v_y /= 2

        current_x += v_x
        current_y += v_y
        
        mx, my = int(current_x), int(current_y)
        
        # Move
        pyautogui.moveTo(mx, my)
        overlay.update_cursor(mx, my, active=True)
            
        # Variable sleep for human timing
        time.sleep(random.uniform(0.002, 0.006))

    # Final snap
    pyautogui.moveTo(dest_x, dest_y)
    overlay.update_cursor(dest_x, dest_y, active=False)

def move_to(x, y, mode="human"):
    start_x, start_y = pyautogui.position()
    overlay.log(f"Move -> {x},{y} ({mode})")
    
    if mode == "fast":
        pyautogui.moveTo(x, y, duration=0.1)
        overlay.update_cursor(x, y)
    else:
        # Add slight inaccuracy
        offset = 1
        tx = x + random.randint(-offset, offset)
        ty = y + random.randint(-offset, offset)
        human_wind_mouse(start_x, start_y, tx, ty)
