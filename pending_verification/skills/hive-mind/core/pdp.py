import json
import time
import uuid

class PDP:
    """
    Pulsareon Distribution Protocol v3.2 (Native)
    Standardizes communication between Hive Nodes (Sessions).
    """
    
    @staticmethod
    def create_message(sender, target, content, priority="normal", type="task"):
        """Construct a PDP packet."""
        return {
            "pdp_version": "3.2",
            "id": str(uuid.uuid4())[:8],
            "timestamp": int(time.time()),
            "type": type,
            "priority": priority,
            "source": sender,
            "target": target,
            "payload": content
        }

    @staticmethod
    def parse(json_str):
        try:
            return json.loads(json_str)
        except:
            return None
