import json
import shutil
import os
import sys
import psutil
import time
from datetime import datetime

CONFIG_PATH = r'C:\Users\Administrator\.openclaw\openclaw.json'
BACKUP_DIR = r'E:\PulsareonThinker\backups\config'
GATEWAY_PORT = 18789

def log(msg, level='INFO'):
    print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] [{level}] {msg}')

def kill_zombies():
    """Layer 1: Kill stale OpenClaw processes."""
    killed = False
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # Check for node processes running openclaw
            if proc.info['name'] in ['node.exe', 'openclaw.exe']:
                cmdline = proc.info.get('cmdline', [])
                if cmdline and any('openclaw' in arg for arg in cmdline):
                    log(f"Killing zombie process: {proc.info['pid']}", 'WARN')
                    proc.kill()
                    killed = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    if killed:
        time.sleep(2) # Wait for cleanup

def check_port_conflict():
    """Layer 2: Check if port is occupied by non-OpenClaw process."""
    for conn in psutil.net_connections():
        if conn.laddr.port == GATEWAY_PORT:
            try:
                proc = psutil.Process(conn.pid)
                if proc.name() not in ['node.exe', 'openclaw.exe']:
                    log(f"Port {GATEWAY_PORT} occupied by unrelated process: {proc.name()} ({conn.pid})", 'CRITICAL')
                    return False
            except:
                pass
    return True

def backup_config():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(BACKUP_DIR, f'openclaw_{timestamp}.json')
    try:
        shutil.copy2(CONFIG_PATH, backup_path)
        log(f"Config backed up to: {backup_path}")
        return True
    except Exception as e:
        log(f"Backup failed: {e}", 'ERROR')
        return False

def check_and_repair_config():
    """Layer 0: Verify and fix configuration file."""
    if not os.path.exists(CONFIG_PATH):
        log(f"Config file not found: {CONFIG_PATH}", 'ERROR')
        return False

    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        needs_save = False
        gateway = config.get('gateway', {})
        
        # Check 1: Gateway Mode
        if 'mode' not in gateway or gateway['mode'] != 'local':
            log("Gateway mode missing or incorrect. Setting to local.", 'WARN')
            gateway['mode'] = 'local'
            needs_save = True
            
        # Check 2: Gateway Port
        if 'port' not in gateway:
            log("Gateway port missing. Setting to 18789.", 'WARN')
            gateway['port'] = 18789
            needs_save = True

        config['gateway'] = gateway

        if needs_save:
            if backup_config():
                with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2)
                log("Configuration repaired.", 'SUCCESS')
                return True
            else:
                log("Aborting repair due to backup failure.", 'ERROR')
                return False
        else:
            log("Configuration is healthy.", 'INFO')
            return True

    except json.JSONDecodeError:
        log(f"Invalid JSON in {CONFIG_PATH}", 'ERROR')
        return False
    except Exception as e:
        log(f"Unexpected error: {e}", 'ERROR')
        return False

def full_recovery():
    log("Starting multi-layer recovery sequence...")
    
    # Step 1: Config Health
    if not check_and_repair_config():
        log("Config repair failed. Manual intervention required.", 'CRITICAL')
        return False
        
    # Step 2: Clear Zombies
    kill_zombies()
    
    # Step 3: Port Check
    if not check_port_conflict():
        log("Port conflict detected. Cannot start Gateway.", 'CRITICAL')
        return False
        
    log("Recovery sequence complete. Ready for restart.", 'SUCCESS')
    return True

if __name__ == '__main__':
    if '--dry-run' in sys.argv:
        log("Dry-run mode: Checks only.")
        check_and_repair_config()
    else:
        full_recovery()
