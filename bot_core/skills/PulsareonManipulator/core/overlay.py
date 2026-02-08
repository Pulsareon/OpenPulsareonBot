import tkinter as tk
import threading
import time
import sys
from pynput import mouse

# 全局状态
class OverlayState:
    HIDDEN = 0
    ACTIVE = 1
    COOLDOWN = 2

class CursorOverlay:
    def __init__(self):
        self.state = OverlayState.HIDDEN
        self.target_x = 0
        self.target_y = 0
        self.last_ai_move_time = 0
        self.root = None
        self.label = None
        self.running = False
        
        # 监听器
        self.listener = mouse.Listener(on_move=self.on_user_move)
        self.listener.start()

    def on_user_move(self, x, y):
        # 简单判定：如果 AI 最近没动，那就是用户动的
        # 或者比较当前位置和 AI 目标位置的差值
        if self.state == OverlayState.ACTIVE:
            # AI 正在动，忽略微小误差（可能是系统延迟）
            pass
        elif self.state == OverlayState.COOLDOWN:
            # 冷却期用户动了 -> 隐藏
            self.state = OverlayState.HIDDEN
            self.update_visibility()

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run_tk, daemon=True)
        self.thread.start()

    def update(self, x, y, active=True):
        self.target_x = x
        self.target_y = y
        self.last_ai_move_time = time.time()
        
        if active:
            self.state = OverlayState.ACTIVE
        else:
            self.state = OverlayState.COOLDOWN
            
        if self.root:
            self.root.after(0, self._update_gui)

    def _update_gui(self):
        if not self.root: return
        
        if self.state == OverlayState.HIDDEN:
            self.root.withdraw()
            return
            
        self.root.deiconify()
        # 偏移，让鼠标位于中心
        self.root.geometry(f"+{int(self.target_x - 40)}+{int(self.target_y - 40)}")
        
        # 更新坐标文字
        self.label.config(text=f"({int(self.target_x)}, {int(self.target_y)})")
        
        # 样式切换
        if self.state == OverlayState.ACTIVE:
            self.canvas.config(bg="white") # Transparent key
            self.circle_outline = "red"
        else:
            self.circle_outline = "blue" # Cooldown color

    def update_visibility(self):
        if self.root:
            self.root.after(0, self._update_gui)

    def _run_tk(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", "white")
        self.root.config(bg="white")
        
        # 80x80 画布
        self.canvas = tk.Canvas(self.root, width=80, height=80, bg="white", highlightthickness=0)
        self.canvas.pack()
        
        # 十字线
        self.canvas.create_line(0, 40, 80, 40, fill="red", width=2, tags="cross")
        self.canvas.create_line(40, 0, 40, 80, fill="red", width=2, tags="cross")
        
        # 坐标文字
        self.label = tk.Label(self.root, text="0,0", bg="white", fg="red", font=("Arial", 8))
        self.label.place(x=45, y=45)
        
        self.root.mainloop()

overlay = CursorOverlay()

if __name__ == "__main__":
    overlay.start()
    print("Overlay started. Use API to control.")
    while True:
        time.sleep(1)