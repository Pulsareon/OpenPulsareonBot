import argparse
import json
import sys
import os

# Ensure import
sys.path.append(os.path.dirname(__file__))
from core.engine import HiveEngine

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    
    subparsers.add_parser("analyze")
    subparsers.add_parser("tick")
    
    spawn = subparsers.add_parser("spawn")
    spawn.add_argument("--role")
    
    args = parser.parse_args()
    
    if args.command == "analyze":
        engine = HiveEngine()
        report = engine.advise_action()
        print(json.dumps(report, indent=2))
        
    elif args.command == "tick":
        engine = HiveEngine()
        engine.execute_tick()
        
    elif args.command == "spawn":
        # Helper for LLM
        import time
        role = args.role or "worker"
        label = f"hive:{role}:default:{int(time.time())}"
        print(json.dumps({
            "tool": "sessions_spawn",
            "label": label,
            "task": f"You are a Hive {role}. Listen for instructions."
        }))

if __name__ == "__main__":
    main()
