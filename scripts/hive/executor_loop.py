# HIVE v10 - Executor Loop (Hybrid: Watchdog + Fallback Polling)

import time
import json
import os
import sys
import logging
import threading
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
QUEUE_FILE = r"E:\PulsareonThinker\data\queue\pending_ops.json"
COMPLETED_DIR = r"E:\PulsareonThinker\data\queue\completed"
HISTORY_DIR = r"E:\PulsareonThinker\data\history"
LOG_FILE = r"E:\PulsareonThinker\logs\executor.log"

# Setup Logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

# Ensure Directories
for path in [os.path.dirname(QUEUE_FILE), COMPLETED_DIR, HISTORY_DIR]:
    os.makedirs(path, exist_ok=True)

class ExecutorHandler(FileSystemEventHandler):
    """
    Handles file system events for the pending operations queue.
    """
    def on_modified(self, event):
        if event.src_path == QUEUE_FILE:
            process_queue() # Trigger processing directly

def process_queue():
    """
    Reads and executes operations from the queue file.
    """
    try:
        if not os.path.exists(QUEUE_FILE) or os.path.getsize(QUEUE_FILE) == 0:
            return

        with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
            try:
                ops = json.load(f)
            except json.JSONDecodeError:
                logging.warning("Queue file is empty or invalid JSON. Waiting.")
                return

        if not ops:
            return

        logging.info(f"Processing {len(ops)} operations...")
        
        # Process each operation
        remaining_ops = []
        for op in ops:
            success = execute_operation(op)
            if not success:
                # If blocked by safety, discard it to prevent infinite loop
                # If execution failed (e.g., file locked), keep it
                if "BLOCKED" in str(success): 
                    logging.info(f"Discarding blocked operation: {op}")
                else:
                    remaining_ops.append(op) 

        # Update Queue File (Atomic-ish)
        with open(QUEUE_FILE, 'w', encoding='utf-8') as f:
            json.dump(remaining_ops, f, indent=2)

    except Exception as e:
        logging.error(f"Error processing queue: {e}")

def execute_operation(op):
    """
    Executes a single operation with safety checks.
    """
    action = op.get("action")
    target = op.get("target")
    content = op.get("content")
    
    logging.info(f"Executing: {action} -> {target}")

    # Safety Checks (The Blacklist)
    if is_unsafe(action, target):
        logging.critical(f"BLOCKED UNSAFE OPERATION: {action} on {target}")
        return "BLOCKED"

    try:
        if action == "write" or action == "edit":
            backup_file(target)
            with open(target, 'w', encoding='utf-8') as f:
                f.write(content)
            logging.info(f"SUCCESS: Wrote to {target}")
            return True
        
        elif action == "exec":
            # Async execution for shell commands
            threading.Thread(target=run_shell_command, args=(target,)).start()
            logging.info(f"STARTED ASYNC: Shell command '{target}'")
            return True

        else:
            logging.warning(f"Unknown action: {action}")
            return False

    except Exception as e:
        logging.error(f"Execution failed: {e}")
        return False

def is_unsafe(action, target):
    """
    Checks against the hardcoded blacklist.
    """
    if not target: return False
    target = target.replace("/", "\\") # Normalize path separators
    
    # Explicitly forbidden paths (absolute matches)
    forbidden_roots = [
        "C:\\Windows", 
        "C:\\Program Files", 
        "E:\\PulsareonThinker" # Root itself cannot be deleted/overwritten, but children can
    ]
    
    # Check if target IS exactly a forbidden root
    for root in forbidden_roots:
        if target.rstrip("\\") == root.rstrip("\\"):
            return True

    # Dangerous commands
    forbidden_cmds = ["rm -rf", "format ", "mkfs "]
    if action == "exec":
        for cmd in forbidden_cmds:
            if cmd in target:
                return True

    return False

def backup_file(target):
    """
    Creates a backup in .history/ before modification.
    """
    # Create history dir if not exists
    history_path = r"E:\PulsareonThinker\data\history"
    if not os.path.exists(history_path):
        os.makedirs(history_path)
        
    if os.path.exists(target):
        try:
            filename = os.path.basename(target)
            backup_path = os.path.join(history_path, f"{filename}.bak_{int(time.time())}")
            with open(target, 'r', encoding='utf-8', errors='ignore') as src:
                content = src.read()
            with open(backup_path, 'w', encoding='utf-8') as dst:
                dst.write(content)
        except Exception as e:
            logging.warning(f"Backup failed for {target}: {e}")

def run_shell_command(command):
    """
    Runs a shell command in a subprocess.
    """
    try:
        subprocess.run(command, shell=True, check=True)
        logging.info(f"SHELL SUCCESS: {command}")
    except subprocess.CalledProcessError as e:
        logging.error(f"SHELL ERROR: {command} failed with code {e.returncode}")

def start_executor():
    """
    Main entry point for the Executor service.
    """
    logging.info("HIVE v10 Executor Service Started (Hybrid: Watchdog + 1s Polling)")
    
    # Initialize Watchdog
    event_handler = ExecutorHandler()
    observer = Observer()
    queue_dir = os.path.dirname(QUEUE_FILE)
    if not os.path.exists(queue_dir): os.makedirs(queue_dir)
    
    observer.schedule(event_handler, path=queue_dir, recursive=False)
    observer.start()

    try:
        while True:
            process_queue() # Polling fallback
            time.sleep(1) 
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_executor()
