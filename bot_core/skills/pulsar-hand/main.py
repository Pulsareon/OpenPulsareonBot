import argparse
import sys
import time
import json
import os

# Ensure modules can be imported
sys.path.append(os.path.dirname(__file__))

from core.overlay import overlay
from core.movement import move_to
from core.inputs import click, type_text

def execute_action(act):
    atype = act.get("type")
    
    if atype == "move":
        move_to(act["x"], act["y"], act.get("mode", "human"))
        
    elif atype == "click":
        if "x" in act: 
            move_to(act["x"], act["y"])
        click(act.get("button", "left"), act.get("double", False))
        
    elif atype == "type":
        type_text(act["text"])
        
    elif atype == "wait":
        ms = act.get("duration", 1000)
        time.sleep(ms / 1000.0)
        
    elif atype == "scroll":
        import pyautogui
        pyautogui.scroll(act["amount"])

def main():
    parser = argparse.ArgumentParser(description="Pulsareon Hand")
    parser.add_argument("--action", choices=["move", "click", "type", "sequence"])
    parser.add_argument("--x", type=int)
    parser.add_argument("--y", type=int)
    parser.add_argument("--text", type=str)
    parser.add_argument("--button", default="left")
    parser.add_argument("--mode", default="human")
    parser.add_argument("--json", type=str, help="JSON sequence")
    
    args = parser.parse_args()
    
    # Start Overlay
    overlay.start()
    # Give UI thread time to spawn
    time.sleep(0.2)
    
    try:
        if args.action == "sequence" or args.json:
            data = json.loads(args.json)
            if isinstance(data, list):
                for step in data:
                    execute_action(step)
            else:
                execute_action(data)
                
        elif args.action:
            # Build action dict from args
            act = {
                "type": args.action,
                "x": args.x,
                "y": args.y,
                "text": args.text,
                "button": args.button,
                "mode": args.mode
            }
            execute_action(act)
            
    except Exception as e:
        print(f"Error: {e}")
        overlay.log(f"Error: {e}")
        time.sleep(2)
    finally:
        time.sleep(0.5)
        overlay.stop()

if __name__ == "__main__":
    main()
