"""
Drone: Resource Monitor (Refactored)
Checks system health and reports to Synapse if critical.
"""

import sys
import psutil
import time
from pathlib import Path

# Add parent directory to path to import synapse
sys.path.append(str(Path(__file__).parent.parent.parent))
from scripts.hive import synapse

def check_resources():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    
    print(f"[Drone-Resource] CPU: {cpu}% | RAM: {ram}%")
    
    if cpu > 90 or ram > 90:
        alert = f"⚠️ **System Critical:** CPU {cpu}% | RAM {ram}%. Requesting cooldown."
        synapse.push_insight("Drone-Resource", "Health", alert, priority="high")
    
    # Optional: Report daily stats if needed, but for now only alert on high load
    # or if it's a specific time (managed by Continuity Engine invoking this)

if __name__ == "__main__":
    check_resources()
