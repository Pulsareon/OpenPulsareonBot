class Config:
    # Overlay Settings
    OVERLAY_ALPHA = 0.8
    OVERLAY_BG = "white" # Transparent key for Windows
    TRANS_KEY = "white"
    
    # Cursor Styles
    # Options: "circle", "crosshair", "full_crosshair", "image"
    CURSOR_STYLE = "crosshair"
    CURSOR_COLOR = "#ff0000"     # Red for idle
    CURSOR_ACTIVE_COLOR = "#00ff00" # Green for action
    CURSOR_SIZE = 20
    
    # HUD Settings
    FONT_FAMILY = "Segoe UI"
    FONT_SIZE = 12
    HUD_OFFSET_X = 25
    HUD_OFFSET_Y = 25
    
    # Input Log
    LOG_MAX_LINES = 8
    LOG_COLOR = "#000000" # Black text
    LOG_BG = "#f0f0f0"    # Semi-transparent bg for text
    
    # Movement Physics
    MOUSE_SPEED_DEFAULT = 0.5
    GRAVITY = 9.0
    WIND = 3.0
    TARGET_RADIUS = 5.0 # Pixels
