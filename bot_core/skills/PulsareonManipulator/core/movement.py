import pyautogui
import numpy as np
import time
import random
import math
from .overlay import overlay

def human_wind_mouse(start_x, start_y, dest_x, dest_y, G_0=9, W_0=3, M_0=15, D_0=12, move_mouse=pyautogui.moveTo):
    """
    WindMouse algorithm (Benland100) - highly human-like mouse movement.
    Based on gravity and wind simulation.
    """
    current_x, current_y = start_x, start_y
    v_x = v_y = W_x = W_y = 0
    
    dist = math.hypot(dest_x - start_x, dest_y - start_y)
    speed = max(0.2, min(2.0, dist / 1000.0))  # Adaptive speed factor
    
    # Steps proportional to distance
    # G_0 is gravity (pull to target), W_0 is wind (randomness)
    steps = int(dist / (G_0 * speed))
    if steps < 10: steps = 10
    
    if not overlay.running:
        overlay.start()

    path = []
    
    sqrt2 = math.sqrt(2)
    sqrt3 = math.sqrt(3)
    sqrt5 = math.sqrt(5)
    
    for i in range(1, steps + 1):
        dist = math.hypot(dest_x - current_x, dest_y - current_y)
        
        # Gravity (pull towards target)
        if dist < D_0:
            D = D_0 # Close range precision
        else:
            D = dist

        wind = min(W_0, dist)
        
        if dist >= D_0:
            W_x = W_x / sqrt3 + (random.random() * (wind * 2 + 1) - wind) / sqrt5
            W_y = W_y / sqrt3 + (random.random() * (wind * 2 + 1) - wind) / sqrt5
        else:
            W_x /= sqrt2
            W_y /= sqrt2

        v_x += W_x + (dest_x - current_x) * G_0 / D
        v_y += W_y + (dest_y - current_y) * G_0 / D

        if dist < D_0: # Dampen velocity close to target
            v_x /= 2
            v_y /= 2

        current_x += v_x
        current_y += v_y
        
        mx, my = int(current_x), int(current_y)
        
        # Only move if position changed
        if not path or path[-1] != (mx, my):
            path.append((mx, my))
            move_mouse(mx, my)
            overlay.update(mx, my, active=True)
            
            # Micro sleep for timing variation
            time.sleep(0.005 + random.uniform(0, 0.005))

    overlay.update(dest_x, dest_y, active=False)
    
    # Overshoot correction (rarely)
    if random.random() < 0.1:
        time.sleep(random.uniform(0.1, 0.3))
        move_mouse(dest_x, dest_y)

def human_move(x, y, speed=0.5):
    start_x, start_y = pyautogui.position()
    # Random offset to avoid pixel-perfect clicking
    offset_x = random.randint(-2, 2)
    offset_y = random.randint(-2, 2)
    human_wind_mouse(start_x, start_y, x + offset_x, y + offset_y)
