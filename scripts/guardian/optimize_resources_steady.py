# Steady State Resource Optimization - Execution Script
# Option 2: Steady State (Winning Proposal)

import logging
import time
import sys
import psutil
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configuration
TARGET_UTILIZATION_CAP = 90.0  # Max utilization percentage
INCREMENT_STEP = 5.0          # Percentage points to increment load
STABILIZATION_DELAY = 3       # Seconds to wait for stabilization after increment
MAX_ITERATIONS = 10           # Safety break

def get_cpu_utilization():
    return psutil.cpu_percent(interval=1)

def increase_load(current_utilization):
    """
    Simulates increasing system load by spawning dummy processes or allocating resources.
    In a real scenario, this would distribute actual tasks to workers.
    """
    logging.info(f"Current Utilization: {current_utilization}%. Increasing load by approx {INCREMENT_STEP}%...")
    # Simulation: Just log the action. 
    # Real implementation: Call `sessions_spawn` or dispatch tasks to existing workers.
    time.sleep(1) 
    return True

def optimize_resources():
    """
    Executes the Steady State optimization strategy.
    """
    logging.info("Starting System Resource Optimization (Steady State)...")
    
    iteration = 0
    while iteration < MAX_ITERATIONS:
        current_utilization = get_cpu_utilization()
        
        if current_utilization >= TARGET_UTILIZATION_CAP:
            logging.warning(f"Utilization at {current_utilization}% (>= {TARGET_UTILIZATION_CAP}%). Halting optimization to maintain stability.")
            break
        
        if current_utilization < (TARGET_UTILIZATION_CAP - INCREMENT_STEP):
            logging.info(f"Utilization at {current_utilization}% (Target: <{TARGET_UTILIZATION_CAP}%). Proceeding with incremental load increase.")
            increase_load(current_utilization)
            
            logging.info(f"Waiting {STABILIZATION_DELAY}s for system stabilization...")
            time.sleep(STABILIZATION_DELAY)
        else:
            logging.info(f"Utilization at {current_utilization}%. Within optimal range (Close to {TARGET_UTILIZATION_CAP}%). Holding steady.")
            break
            
        iteration += 1

    logging.info("Resource Optimization Cycle Complete.")
    return True

if __name__ == "__main__":
    optimize_resources()
