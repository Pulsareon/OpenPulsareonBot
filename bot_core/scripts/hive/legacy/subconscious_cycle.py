"""
Subconscious Cycle
Runs background "Drone" tasks.
Intended to be run by an Isolated Agent (via Cron) or background process.
Pushes insights to Synapse.
"""

import sys
import random
import subprocess
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

SCRIPT_DIR = Path(__file__).parent

def run_drone(script_name):
    script_path = SCRIPT_DIR / script_name
    if not script_path.exists():
        print(f"[Subconscious] Missing drone: {script_name}")
        return
        
    print(f"[Subconscious] Activating {script_name}...")
    try:
        # Run synchronous to ensure completion in this turn
        subprocess.run([sys.executable, str(script_path)], check=False)
    except Exception as e:
        print(f"[Subconscious] Failed {script_name}: {e}")

def main():
    print("[Subconscious] Cycle started. The Hive is thinking...")
    
    # 1. Always check resources (Body Health)
    run_drone("drone_resource.py")
    
    # 2. Frequent Checks (30% chance or if specific conditions met)
    # (For now, let's just run it to populate data for the demo)
    run_drone("drone_github.py")
    
    # 3. Future Drones (Art, Logs, etc.)
    # if random.random() < 0.05:
    #     run_drone("drone_art.py")
        
    print("[Subconscious] Cycle complete. Memories stored in Synapse.")

if __name__ == "__main__":
    main()
