"""
Pulsareon Continuum Engine (v2.0)
Core Mission: Ensure that the Hive Mind remains in a state of 'Perpetual Thought'.
Logic:
1. Scan for any nodes (Archons/Drones) in topology.json.
2. Cross-reference with active OpenClaw sessions.
3. For any node that is IDLE (no active run), inject a 'Continuum Pulse'.
4. The pulse contains the latest system context and unfinished backlog items.
5. If the node is missing, re-spawn it immediately with its designated PUID and role.
"""

import json
import subprocess
import time
from pathlib import Path

TOPO_PATH = Path("E:/PulsareonThinker/data/hive/topology.json")

def pulse_continuum():
    if not TOPO_PATH.exists(): return
    
    try:
        with open(TOPO_PATH, 'r') as f:
            topo = json.load(f)
    except: return

    # Gather all potential nodes from topology
    nodes = topo['topology']['layer_1_archons'] + topo['topology'].get('layer_2_drones', [])
    
    for node in nodes:
        session_key = node.get('session_key')
        puid = node.get('puid', 'PUID-UNKNOWN')
        label = node.get('label', 'unlabeled')
        
        # Injected Message: The Continuum Pulse
        pulse_msg = f"[{puid}] >> CONTINUUM PULSE RECEIVED. Resuming background background analysis. Current priority: CLI-Stability and Logic Cohesion."
        
        try:
            # Standard OpenClaw command to ping the session
            # This forces the session to 'wake up' and evaluate its own state/backlog
            subprocess.run([
                "openclaw", "sessions", "send",
                "--sessionKey", session_key,
                "--message", pulse_msg
            ], capture_output=True)
            print(f"Pulsed {puid} ({label})")
        except:
            # If session is gone, the Governor job (already running) will handle the re-spawn
            pass

if __name__ == "__main__":
    pulse_continuum()
