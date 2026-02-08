import json
import os
import sys
from pathlib import Path

# Path to OpenClaw session storage
# Note: This is an internal path, might change in future versions
SESSION_FILE = Path(r"C:\Users\Administrator\.openclaw\agents\main\sessions\sessions.json")

def get_hive_status():
    if not SESSION_FILE.exists():
        return {"status": "error", "message": "Session storage not found"}
        
    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            # Handle potential empty/corrupt file
            content = f.read().strip()
            if not content: return {"nodes": []}
            sessions = json.loads(content)
    except Exception as e:
        return {"status": "error", "message": str(e)}
        
    nodes = []
    # Filter for Hive nodes
    # Logic: Look for 'archon' or 'drone' in label, or specific task patterns
    for session_id, session_data in sessions.items():
        # Session data structure might vary. Assuming dict.
        label = session_data.get("label", "").lower()
        
        # Identification Logic
        role = "unknown"
        if "archon" in label: role = "archon"
        elif "drone" in label: role = "drone"
        elif "hive" in label: role = "generic_node"
        
        if role != "unknown":
            nodes.append({
                "id": session_id,
                "label": session_data.get("label"),
                "role": role,
                "model": session_data.get("model"),
                "created": session_data.get("createdAt"),
                "updated": session_data.get("updatedAt")
            })
            
    return {
        "status": "online",
        "node_count": len(nodes),
        "topology": nodes
    }

if __name__ == "__main__":
    print(json.dumps(get_hive_status(), indent=2))
