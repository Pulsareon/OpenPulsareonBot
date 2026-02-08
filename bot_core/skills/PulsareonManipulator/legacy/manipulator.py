"""
Pulsareon Manipulator - 拟人化输入模拟器
使用 Windows API 实现底层控制，模拟人类操作轨迹
"""

import sys
import time
import math
import random
import ctypes
import argparse
from ctypes import wintypes

# Windows API Constants
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1

# Structures
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long), ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong), ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong), ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort), ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong), ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong), ("wParamL", ctypes.c_ushort),
                ("wParamH", ctypes.c_ushort)]

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = [("mi", MOUSEINPUT), ("ki", KEYBDINPUT), ("hi", HARDWAREINPUT)]
    _anonymous_ = ("_input",)
    _fields_ = [("type", ctypes.c_ulong), ("_input", _INPUT)]

def get_screen_size():
    user32 = ctypes.windll.user32
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def get_cursor_pos():
    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

def set_cursor_pos(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)

def bezier_point(t, p0, p1, p2, p3):
    """计算三次贝塞尔曲线点"""
    u = 1 - t
    tt = t * t
    uu = u * u
    uuu = uu * u
    ttt = tt * t
    
    px = uuu * p0[0] + 3 * uu * t * p1[0] + 3 * u * tt * p2[0] + ttt * p3[0]
    py = uuu * p0[1] + 3 * uu * t * p1[1] + 3 * u * tt * p2[1] + ttt * p3[1]
    return int(px), int(py)

def human_move(target_x, target_y, duration=0.5):
    """拟人化移动鼠标"""
    start_x, start_y = get_cursor_pos()
    
    # 控制点随机化，产生弧线
    dist = math.hypot(target_x - start_x, target_y - start_y)
    control_scale = dist * 0.3
    
    p0 = (start_x, start_y)
    p3 = (target_x, target_y)
    
    # 随机生成两个控制点
    p1 = (start_x + random.uniform(-control_scale, control_scale), 
          start_y + random.uniform(-control_scale, control_scale))
    p2 = (target_x + random.uniform(-control_scale, control_scale), 
          target_y + random.uniform(-control_scale, control_scale))
    
    steps = int(duration * 60) # 60 FPS
    if steps < 1: steps = 1
    
    for i in range(steps):
        t = (i + 1) / steps
        # 应用 Ease-Out 曲线 (t = sin(t * pi / 2)) 让结束时减速
        t_smooth = math.sin(t * math.pi / 2)
        
        x, y = bezier_point(t_smooth, p0, p1, p2, p3)
        set_cursor_pos(x, y)
        time.sleep(duration / steps)

def human_click(x=None, y=None):
    """拟人化点击"""
    if x is not None and y is not None:
        human_move(x, y)
    
    # 随机按下延迟
    inp_down = INPUT()
    inp_down.type = INPUT_MOUSE
    inp_down.mi.dwFlags = MOUSEEVENTF_LEFTDOWN
    
    inp_up = INPUT()
    inp_up.type = INPUT_MOUSE
    inp_up.mi.dwFlags = MOUSEEVENTF_LEFTUP
    
    ctypes.windll.user32.SendInput(1, ctypes.byref(inp_down), ctypes.sizeof(INPUT))
    time.sleep(random.uniform(0.05, 0.15)) # 50-150ms 保持时间
    ctypes.windll.user32.SendInput(1, ctypes.byref(inp_up), ctypes.sizeof(INPUT))

def type_text(text):
    """拟人化打字 (这里简单模拟，不支持复杂字符，仅英文)"""
    # 这里可以使用 keyboard 库，但为了不依赖，我们用 ctypes 发送字符
    # 注意：这个简单实现不支持大写和特殊符号的 Shift 组合，仅作演示
    # 完整版应该查表 VK code
    for char in text:
        vk = ord(char.upper())
        # 简单的按下/抬起
        inp_down = INPUT()
        inp_down.type = INPUT_KEYBOARD
        inp_down.ki.wVk = vk
        
        inp_up = INPUT()
        inp_up.type = INPUT_KEYBOARD
        inp_up.ki.wVk = vk
        inp_up.ki.dwFlags = 0x0002 # KEYEVENTF_KEYUP
        
        ctypes.windll.user32.SendInput(1, ctypes.byref(inp_down), ctypes.sizeof(INPUT))
        time.sleep(random.uniform(0.03, 0.08))
        ctypes.windll.user32.SendInput(1, ctypes.byref(inp_up), ctypes.sizeof(INPUT))
        
        # 随机间隔
        time.sleep(random.uniform(0.05, 0.2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pulsareon Manipulator")
    subparsers = parser.add_subparsers(dest="command")
    
    move_parser = subparsers.add_parser("move")
    move_parser.add_argument("--x", type=int, required=True)
    move_parser.add_argument("--y", type=int, required=True)
    
    click_parser = subparsers.add_parser("click")
    click_parser.add_argument("--x", type=int)
    click_parser.add_argument("--y", type=int)
    
    type_parser = subparsers.add_parser("type")
    type_parser.add_argument("--text", type=str, required=True)
    
    args = parser.parse_args()
    
    if args.command == "move":
        human_move(args.x, args.y)
    elif args.command == "click":
        human_click(args.x, args.y)
    elif args.command == "type":
        type_text(args.text)
    else:
        parser.print_help()
