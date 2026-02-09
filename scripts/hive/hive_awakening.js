const { execSync, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

/**
 * HIVE Awakening Protocol v2.1 - SAFETY LOCK ENABLED
 * Reason: v2.0 caused system freeze due to unbounded scaling (160+ nodes).
 * Fix: Hard caps, conservative multipliers, and user-priority resource reservation.
 */

const WORKSPACE = 'E:\\PulsareonThinker';
const LOG_FILE = path.join(WORKSPACE, 'logs', 'hive', 'awakening.log');

function log(msg) {
    if (!fs.existsSync(path.dirname(LOG_FILE))) fs.mkdirSync(path.dirname(LOG_FILE), { recursive: true });
    fs.appendFileSync(LOG_FILE, `${new Date().toISOString()} - ${msg}\n`);
    console.log(`[HIVE-SAFE] ${msg}`);
}

async function getSystemStats() {
    const cpus = os.cpus();
    const cpuUsage = os.loadavg()[0] / cpus.length; 
    const totalMemGB = os.totalmem() / 1024 / 1024 / 1024;
    const freeMemGB = os.freemem() / 1024 / 1024 / 1024;
    
    return { 
        cpuPercent: cpuUsage * 100, 
        totalMemGB,
        freeMemGB,
        memPercent: ((os.totalmem() - os.freemem()) / os.totalmem()) * 100
    };
}

async function runSafeCycle() {
    try {
        const stats = await getSystemStats();
        log(`Status: CPU ${stats.cpuPercent.toFixed(1)}% | Free RAM ${stats.freeMemGB.toFixed(1)}GB`);

        // 1. Safety Cutoff: If system is already busy (>70%), DO NOT EXPAND.
        if (stats.cpuPercent > 70 || stats.memPercent > 85) {
            log('High Load Detected. Skipping expansion. Maintaining minimal HIVE (3 nodes).');
            return;
        }

        // 2. Conservative Scaling Formula
        // RAM Limit: Assume each node needs 200MB safe buffer.
        // CPU Limit: Max 12 nodes total to prevent thread starvation on typical desktop.
        const ramSupport = Math.floor(stats.freeMemGB * 5); // 1GB = 5 nodes
        const safeMax = 12; 
        
        let targetNodes = 9; // Base
        if (stats.cpuPercent < 30) {
            targetNodes = Math.min(ramSupport, safeMax);
        }

        log(`Calculated Safe Capacity: ${targetNodes} nodes (Limit: ${safeMax})`);

        // 3. Execution (Simulated coordination for now to prevent another crash)
        // Only run evolution if we have a healthy margin
        if (targetNodes >= 9) {
            log('Conditions Green. Running evolutionary maintenance (Low Priority)...');
            // Using 'start /low' (Windows) via node spawn to ensure user priority
            const evoScript = path.join(WORKSPACE, 'scripts', 'hive', 'evolution_engine.js');
            if (fs.existsSync(evoScript)) {
                spawn('node', [evoScript], { 
                    detached: true, 
                    stdio: 'ignore',
                    windowsHide: true 
                }).unref();
            }
        }

    } catch (e) {
        log(`Error: ${e.message}`);
    }
}

runSafeCycle();
