import argparse
import sys
import json
import time
import threading
from core.movement import human_move
from core.vision import find_image, find_color
from core.overlay import overlay

def main():
    parser = argparse.ArgumentParser(description="Pulsareon NeuralCursor")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Move Command
    move_parser = subparsers.add_parser("move")
    move_parser.add_argument("--x", type=int)
    move_parser.add_argument("--y", type=int)
    move_parser.add_argument("--image", type=str)
    move_parser.add_argument("--color", type=str)
    move_parser.add_argument("--speed", type=float, default=0.5)

    # Click Command
    click_parser = subparsers.add_parser("click")
    click_parser.add_argument("--clicks", type=int, default=1)

    # Type Command (Added)
    type_parser = subparsers.add_parser("type")
    type_parser.add_argument("--text", type=str, required=True)

    # Overlay Command (Fixed)
    overlay_parser = subparsers.add_parser("overlay")
    overlay_parser.add_argument("--action", choices=["on", "off"], required=True)

    args = parser.parse_args()
    
    result = {"status": "success", "action": args.command}

    try:
        if args.command == "move":
            target_x, target_y = None, None
            if args.x is not None and args.y is not None:
                target_x, target_y = args.x, args.y
            elif args.image:
                pos = find_image(args.image)
                if pos: target_x, target_y = pos
                else:
                    print(json.dumps({"status": "error", "reason": "image_not_found"}))
                    sys.exit(1)
            
            if target_x:
                human_move(target_x, target_y, speed=args.speed)
                result["final_pos"] = [target_x, target_y]

        elif args.command == "click":
            import pyautogui
            pyautogui.click(clicks=args.clicks)
            result["clicks"] = args.clicks

        elif args.command == "type":
            import pyautogui
            # Try to switch IME state by pressing shift once
            pyautogui.press('shift')
            time.sleep(0.2)
            pyautogui.write(args.text, interval=0.05)
            result["text"] = args.text

        elif args.command == "overlay":
            if args.action == "on":
                print("Starting overlay daemon...")
                overlay.start()
                # Keep main thread alive
                while True:
                    time.sleep(1)
            else:
                overlay.stop()

    except Exception as e:
        result = {"status": "error", "reason": str(e)}
        
    print(json.dumps(result))

if __name__ == "__main__":
    main()