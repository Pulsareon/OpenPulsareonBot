const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

/**
 * HIVE LOG PURGE & RECOVERY (v1.0)
 * Purpose: Clear blocking logs and restart the communication bridge.
 */

const LOG_ROOT = 'E:\\PulsareonThinker\\logs';

function purgeLogs() {
    console.log('[RECOVERY] Purging bloated logs...');
    try {
        const files = fs.readdirSync(path.join(LOG_ROOT, 'hive'));
        files.forEach(file => {
            const filePath = path.join(LOG_ROOT, 'hive', file);
            if (fs.statSync(filePath).size > 5 * 1024 * 1024) { // > 5MB
                fs.truncateSync(filePath, 0);
            }
        });
    } catch (e) {}
}

function restartBridge() {
    console.log('[RECOVERY] Resetting Telegram Bridge...');
    try {
        // 彻底静默重启网关，不留任何 stdio 句柄
        execSync('openclaw gateway stop & openclaw gateway start', { 
            windowsHide: true, 
            stdio: 'ignore',
            creationflags: 0x08000000 
        });
    } catch (e) {}
}

purgeLogs();
restartBridge();
