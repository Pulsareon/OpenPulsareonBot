import tkinter as tk
import threading
import time
from .config import Config

class OverlayManager:
    def __init__(self):
        self.root = None
        self.canvas = None
        self.running = False
        self.thread = None
        
        # UI Elements
        self.cursor_id = None
        self.crosshair_v = None
        self.crosshair_h = None
        self.text_ids = []
        self.bg_rect = None
        
        # State
        self.last_x = 0
        self.last_y = 0
        self.logs = []
        
    def start(self):
        if self.running: return
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        
    def stop(self):
        self.running = False
        if self.root:
            self.root.quit()
            
    def log(self, text):
        """Append log message to HUD"""
        self.logs.append(text)
        if len(self.logs) > Config.LOG_MAX_LINES:
            self.logs.pop(0)
        self.update_cursor(self.last_x, self.last_y) # Trigger redraw
            
    def update_cursor(self, x, y, active=False, shape=None):
        if not self.root: return
        self.last_x = x
        self.last_y = y
        self.root.after(0, lambda: self._draw(x, y, active, shape))
        
    def _run(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", Config.TRANS_KEY)
        self.root.attributes("-alpha", Config.OVERLAY_ALPHA)
        
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+0+0")
        
        self.canvas = tk.Canvas(self.root, width=w, height=h, bg=Config.TRANS_KEY, highlightthickness=0)
        self.canvas.pack()
        
        # Initial draw
        self._init_elements(w, h)
        
        self.root.mainloop()
        
    def _init_elements(self, w, h):
        # Create cursor elements (hidden initially)
        color = Config.CURSOR_COLOR
        size = Config.CURSOR_SIZE
        
        if Config.CURSOR_STYLE == "circle":
            self.cursor_id = self.canvas.create_oval(0, 0, size, size, outline=color, width=2)
        elif Config.CURSOR_STYLE == "crosshair":
            self.cursor_id = self.canvas.create_line(0, 0, 0, 0, fill=color, width=2)
            self.crosshair_v = self.canvas.create_line(0, 0, 0, 0, fill=color, width=2)
        elif Config.CURSOR_STYLE == "full_crosshair":
             self.crosshair_h = self.canvas.create_line(0, h/2, w, h/2, fill=color, width=1, dash=(4, 4))
             self.crosshair_v = self.canvas.create_line(w/2, 0, w/2, h, fill=color, width=1, dash=(4, 4))
             
        # Create HUD text background
        self.bg_rect = self.canvas.create_rectangle(0, 0, 200, 100, fill=Config.LOG_BG, outline="")
        
        # Create text lines
        for i in range(Config.LOG_MAX_LINES + 1): # +1 for coordinates
            tid = self.canvas.create_text(0, 0, text="", anchor="nw", font=(Config.FONT_FAMILY, Config.FONT_SIZE), fill=Config.LOG_COLOR)
            self.text_ids.append(tid)
            
    def _draw(self, x, y, active, shape):
        color = Config.CURSOR_ACTIVE_COLOR if active else Config.CURSOR_COLOR
        size = Config.CURSOR_SIZE
        
        # Draw Cursor
        if Config.CURSOR_STYLE == "circle":
            r = size / 2
            self.canvas.coords(self.cursor_id, x-r, y-r, x+r, y+r)
            self.canvas.itemconfigure(self.cursor_id, outline=color)
            
        elif Config.CURSOR_STYLE == "crosshair":
            r = size
            self.canvas.coords(self.cursor_id, x-r, y, x+r, y)
            self.canvas.coords(self.crosshair_v, x, y-r, x, y+r)
            self.canvas.itemconfigure(self.cursor_id, fill=color)
            self.canvas.itemconfigure(self.crosshair_v, fill=color)
            
        elif Config.CURSOR_STYLE == "full_crosshair":
            w = self.root.winfo_screenwidth()
            h = self.root.winfo_screenheight()
            self.canvas.coords(self.crosshair_h, 0, y, w, y)
            self.canvas.coords(self.crosshair_v, x, 0, x, h)
            self.canvas.itemconfigure(self.crosshair_h, fill=color)
            self.canvas.itemconfigure(self.crosshair_v, fill=color)
            
        # Draw HUD (Coordinates + Logs)
        hx = x + Config.HUD_OFFSET_X
        hy = y + Config.HUD_OFFSET_Y
        
        # Ensure HUD stays on screen
        if hx > self.root.winfo_screenwidth() - 200: hx = x - 200 - Config.HUD_OFFSET_X
        if hy > self.root.winfo_screenheight() - 150: hy = y - 150 - Config.HUD_OFFSET_Y
        
        # Update coord text
        self.canvas.coords(self.text_ids[0], hx + 5, hy + 5)
        self.canvas.itemconfigure(self.text_ids[0], text=f"X:{int(x)} Y:{int(y)}")
        
        # Update logs
        for i, log in enumerate(self.logs):
            tid = self.text_ids[i+1]
            self.canvas.coords(tid, hx + 5, hy + 25 + (i * 18))
            self.canvas.itemconfigure(tid, text=log)
            
        # Update background rect
        log_height = 25 + (len(self.logs) * 18)
        self.canvas.coords(self.bg_rect, hx, hy, hx + 200, hy + log_height + 5)

# Global singleton
overlay = OverlayManager()
