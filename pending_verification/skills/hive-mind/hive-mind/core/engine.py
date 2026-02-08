import json
import time
from pathlib import Path
import psutil
import requests

SESSION_FILE = Path(r"C:\Users\Administrator\.openclaw\agents\main\sessions\sessions.json")
CONFIG_FILE = Path(r"C:\Users\Administrator\.openclaw\openclaw.json")

class HiveEngine:
    def __init__(self):
        self.sessions = {}
        self.topology = {"overmind": None, "governors": [], "workers": []}
        self.gateway_url = "http://127.0.0.1:18789"
        self.gateway_token = None
        self.load_config()
        self.load_state()

    def load_config(self):
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    gw = cfg.get("gateway", {})
                    self.gateway_url = f"http://{gw.get('bind', '127.0.0.1')}:{gw.get('port', 18789)}"
                    if gw.get("auth", {}).get("mode") == "token":
                        self.gateway_token = gw.get("auth", {}).get("token")
            except:
                pass

    def load_state(self):
        # 1. Load from Hive State (Primary)
        # 2. Reconcile with Sessions (Secondary)
        if SESSION_FILE.exists():
            try:
                with open(SESSION_FILE, "r", encoding="utf-8") as f:
                    data = f.read().strip()
                    if data:
                        raw_sessions = json.loads(data)
                        if isinstance(raw_sessions, list):
                            self.sessions = {s["id"]: s for s in raw_sessions}
                        else:
                            self.sessions = raw_sessions
            except:
                self.sessions = {}
        self._build_topology()

    def _build_topology(self):
        self.topology = {"overmind": None, "governors": [], "workers": []}
        for sid, s in self.sessions.items():
            # Identify Overmind (Main Agent)
            if "agent:main:telegram" in sid or "agent:main:main" in sid:
                self.topology["overmind"] = {"id": sid, "role": "overmind", "data": s}
                continue
            
            label = s.get("label", "")
            if not label or "hive:" not in label: continue
            
            parts = label.split(":")
            role = parts[1] if len(parts) > 1 else "unknown"
            node = {"id": sid, "data": s, "role": role, "meta": parts}
            
            if role == "overmind": 
                # Sub-agent overmind (if any)
                pass 
            elif role == "governor": self.topology["governors"].append(node)
            elif role == "worker": self.topology["workers"].append(node)

    def spawn_session(self, role, task=None):
        if not self.gateway_token: 
            print("[ERR] No Gateway Token")
            return
            
        print(f"[HIVE] Spawning {role}...")
        
        # Load Prompt
        prompt = f"You are a Hive {role}. Await instructions."
        try:
            prompt_path = Path(__file__).parent.parent / "assets" / "GENESIS_PROMPT.md"
            if prompt_path.exists():
                with open(prompt_path, "r", encoding="utf-8") as f:
                    prompt = f.read().replace("{{role}}", role).replace("{{session_id}}", "NEW")
        except:
            pass
            
        url = f"{self.gateway_url}/v1/sessions"
        
        # Use Tool API (sessions_spawn logic)
        # Note: API might be different. Using standard agent/run or sessions/spawn
        # Actually, best way is to use `agents_spawn` or `sessions` POST.
        # OpenClaw API: POST /v1/sessions (create new)
        
        data = {
            "agentId": "main",
            "model": "cli-proxy/gemini-2.5-flash",
            "label": f"hive:{role}:default:{int(time.time())}",
            "initialMessage": prompt,
            "kind": "isolated" # Hive nodes should be isolated? Or sub-agent?
            # If isolated, they persist but are not sub-agents of main context.
            # If we want sub-agents, we need to spawn from main session.
            # But here we are external script.
            # Creating a 'root' session is fine.
        }
        
        try:
            r = requests.post(url, json=data, headers={"Authorization": f"Bearer {self.gateway_token}"})
            print(f"[HIVE] Spawn Result: {r.status_code} {r.text}")
        except Exception as e:
            print(f"[HIVE] Spawn Error: {e}")

    def execute_tick(self):
        """
        The Heartbeat Function.
        Analyzes and ACTS.
        """
        # Update Sentinel Heartbeat
        try:
            hb_file = Path(r"E:\PulsareonThinker\data\state\heartbeat.timestamp")
            hb_file.parent.mkdir(parents=True, exist_ok=True)
            with open(hb_file, "w") as f:
                f.write(time.strftime("%Y-%m-%d %H:%M:%S"))
        except:
            pass

        report = self.advise_action()
        print(f"[HIVE] Load: {report['load']}% | Actions: {len(report['actions'])}")
        
        for act in report['actions']:
            if act["type"] == "spawn_worker":
                self.spawn_session("worker")
            elif act["type"] == "elect_overmind":
                # If Main Agent is missing, we can't do much (we are likely dead too).
                print("[WARN] Overmind Missing!")
            
    def advise_action(self):
        load = psutil.cpu_percent(interval=0.1)
        actions = []
        
        # 1. Topology
        if not self.topology["overmind"]:
            actions.append({"type": "elect_overmind", "reason": "Missing"})
            
        # 2. Evolution
        # Target: At least 1 Governor, 2 Workers
        gov_count = len(self.topology["governors"])
        worker_count = len(self.topology["workers"])
        
        if load < 90:
            if gov_count < 1:
                actions.append({"type": "spawn_worker", "role": "governor", "reason": "Need Governor"})
            elif worker_count < 2:
                actions.append({"type": "spawn_worker", "role": "worker", "reason": "Need Workers"})
            elif worker_count < 5: # Cap at 5 for now
                # Random growth
                pass

        return {
            "status": "ok",
            "load": load,
            "actions": actions
        }
