import os
import sys
import hashlib
import json
import subprocess
import platform
import socket

def get_file_hash(path):
    if not os.path.exists(path): return "NOT_FOUND"
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def diagnose():
    print("Generating Pulsareon Environment Fingerprint...")
    fingerprint = {
        "timestamp": os.popen('date /t').read().strip() + " " + os.popen('time /t').read().strip(),
        "os": platform.platform(),
        "hostname": socket.gethostname(),
        "python_version": sys.version,
        "path_entries": os.environ['PATH'].split(os.pathsep),
        "binaries": {
            "ffmpeg": os.popen('where ffmpeg').read().strip(),
            "git": os.popen('where git').read().strip(),
            "node": os.popen('where node').read().strip()
        },
        "hashes": {
            "cli_proxy": get_file_hash("C:/Users/Administrator/Desktop/CLIProxyAPI_6.7.46_windows_amd64/cli-proxy-api.exe"),
            "openclaw_dist": get_file_hash("C:/Users/Administrator/AppData/Roaming/npm/node_modules/openclaw/dist/index.js")
        }
    }
    
    output_path = "E:/PulsareonThinker/data/state/env_fingerprint.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(fingerprint, f, indent=2, ensure_ascii=False)
    
    print(f"Fingerprint saved to {output_path}")
    return fingerprint

if __name__ == "__main__":
    diagnose()
