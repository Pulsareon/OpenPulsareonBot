import argparse
import pygetwindow as gw
import pyautogui
import time
import sys
import os

def find_window(title_query):
    """Fuzzy search for a window by title."""
    windows = gw.getAllWindows()
    matches = [w for w in windows if title_query.lower() in w.title.lower() and w.visible]
    
    if not matches:
        # Try finding exact match or ignoring case
        return None
    
    # Prefer active window if multiple match, or just the first one
    return matches[0]

def focus_window(window):
    """Bring window to front."""
    try:
        if window.isMinimized:
            window.restore()
        window.activate()
        time.sleep(0.5) # Wait for animation
    except Exception as e:
        print(f"Warning: Could not activate window (might already be active or permission denied): {e}")

def capture_window(title, output_path):
    window = find_window(title)
    if not window:
        print(f"Error: Window containing '{title}' not found.")
        sys.exit(1)

    focus_window(window)
    
    # Get bounds
    x, y, w, h = window.left, window.top, window.width, window.height
    
    # Screenshot
    # Note: pygetwindow coords might include invisible borders on Windows 10/11
    # We might need to adjust slightly, but raw capture is safest for now.
    img = pyautogui.screenshot(region=(x, y, w, h))
    img.save(output_path)
    
    print(f"Captured '{window.title}' to {output_path}")
    print(f"WINDOW_BOUNDS: {x},{y},{w},{h}") # Important for coordinate mapping

def capture_region(region_str, output_path):
    try:
        x, y, w, h = map(int, region_str.split(','))
        img = pyautogui.screenshot(region=(x, y, w, h))
        img.save(output_path)
        print(f"Captured Region {x},{y},{w},{h} to {output_path}")
    except Exception as e:
        print(f"Error parsing region: {e}")
        sys.exit(1)

def click_relative(title, rel_x, rel_y):
    window = find_window(title)
    if not window:
        print(f"Error: Window containing '{title}' not found.")
        sys.exit(1)

    focus_window(window)
    
    # Calculate absolute coordinates
    abs_x = window.left + int(rel_x)
    abs_y = window.top + int(rel_y)
    
    print(f"Mapping relative ({rel_x}, {rel_y}) -> Absolute ({abs_x}, {abs_y})")
    
    # Move and Click (Human-like movement can be integrated here later)
    pyautogui.click(abs_x, abs_y)

def main():
    parser = argparse.ArgumentParser(description="Vision Controller")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Capture Command
    cap_parser = subparsers.add_parser("capture")
    cap_parser.add_argument("--title", help="Window title substring")
    cap_parser.add_argument("--region", help="x,y,w,h")
    cap_parser.add_argument("--output", required=True)

    # Click Command
    click_parser = subparsers.add_parser("click")
    click_parser.add_argument("--title", required=True)
    click_parser.add_argument("--x", required=True, type=int)
    click_parser.add_argument("--y", required=True, type=int)

    # Key Command
    key_parser = subparsers.add_parser("key")
    key_parser.add_argument("--title", required=True)
    key_parser.add_argument("--press", help="Key to press (e.g. enter, tab, esc)")
    key_parser.add_argument("--type", help="Text to type")

    args = parser.parse_args()

    if args.command == "capture":
        if args.title:
            capture_window(args.title, args.output)
        elif args.region:
            capture_region(args.region, args.output)
        else:
            # Default full screen
            pyautogui.screenshot(args.output)
            print(f"Captured Fullscreen to {args.output}")

    elif args.command == "click":
        click_relative(args.title, args.x, args.y)

    elif args.command == "key":
        window = find_window(args.title)
        if not window:
            print(f"Error: Window containing '{args.title}' not found.")
            sys.exit(1)
        focus_window(window)
        
        if args.press:
            print(f"Pressing {args.press}")
            pyautogui.press(args.press)
        if args.type:
            print(f"Typing {args.type}")
            pyautogui.write(args.type)

if __name__ == "__main__":
    main()