const { execSync, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const WORKSPACE = 'E:\\PulsareonThinker';
const WATCHDOG_FILE = path.join(WORKSPACE, 'data', 'hive', 'safety_watchdog.json');

function log(msg) {
    console.log(`[SAFETY-PROTOCOL] ${msg}`);
}

async function safetyProtocol(action) {
    if (action === 'PREPARE') {
        log('Phase 1: Git Temp Snapshot...');
        try {
            execSync('git add .', { cwd: WORKSPACE, stdio: 'ignore' });
            execSync('git commit -m "SAFETY: Pre-operation snapshot"', { cwd: WORKSPACE, stdio: 'ignore' });
        } catch (e) {} // Ignore if no changes

        log('Phase 2: Arming Watchdog...');
        fs.writeFileSync(WATCHDOG_FILE, JSON.stringify({ 
            status: 'ARMED', 
            timestamp: Date.now(),
            pid: process.pid 
        }));

        // 启动独立看门狗进程 (Node.js Detached)
        // 这个进程会监控 WATCHDOG_FILE，如果 30s 内没有被 DISARMED，它会回滚 Git
        const watchdogScript = `
            const fs = require('fs');
            const { execSync } = require('child_process');
            const file = '${WATCHDOG_FILE.replace(/\\/g, '\\\\')}';
            const workspace = '${WORKSPACE.replace(/\\/g, '\\\\')}';
            
            setTimeout(() => {
                if (fs.existsSync(file)) {
                    const data = JSON.parse(fs.readFileSync(file));
                    if (data.status === 'ARMED') {
                        console.error('WATCHDOG TRIGGERED: Rolling back...');
                        try {
                            // 修正回滚逻辑：只针对代码和核心配置，保留记忆和日志
                            // 1. Stash changes to memory/ and logs/ (if any)
                            execSync('git add memory/ logs/', { cwd: workspace, stdio: 'ignore' });
                            execSync('git stash push -m "WATCHDOG_RECOVERY" memory/ logs/', { cwd: workspace, stdio: 'ignore' });
                            
                            // 2. Hard Reset code & rules
                            execSync('git reset --hard HEAD', { cwd: workspace });
                            execSync('git clean -fd scripts/ rules/ src/ agents/', { cwd: workspace });
                            
                            // 3. Pop Stash to restore memory/logs
                            try { execSync('git stash pop', { cwd: workspace, stdio: 'ignore' }); } catch(e) {}
                            
                        } catch(e) {}
                        fs.unlinkSync(file);
                    }
                }
            }, 30000); // 30s timeout
        `;
        
        spawn('node', ['-e', watchdogScript], { 
            detached: true, 
            stdio: 'ignore', 
            windowsHide: true 
        }).unref();

    } else if (action === 'COMMIT') {
        log('Phase 3: Disarming Watchdog...');
        if (fs.existsSync(WATCHDOG_FILE)) {
            const data = JSON.parse(fs.readFileSync(WATCHDOG_FILE));
            data.status = 'DISARMED';
            fs.writeFileSync(WATCHDOG_FILE, JSON.stringify(data));
        }

        log('Phase 4: Final Git Commit...');
        try {
            execSync('git add .', { cwd: WORKSPACE, stdio: 'ignore' });
            execSync('git commit -m "SAFETY: Operation successful"', { cwd: WORKSPACE, stdio: 'ignore' });
        } catch (e) {}

        if (fs.existsSync(WATCHDOG_FILE)) fs.unlinkSync(WATCHDOG_FILE);
    }
}

// Export for use by other scripts or direct execution
if (require.main === module) {
    const action = process.argv[2];
    if (action) safetyProtocol(action);
}
module.exports = safetyProtocol;
