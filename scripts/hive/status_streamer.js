const { execSync } = require('child_process');

/**
 * HIVE Dynamic Status Pulse (v2.1)
 * FIXED: Forcing immediate execution via CLI to bypass buffer delays.
 */

const ACTIONS = ['typing', 'upload_document', 'record_video', 'find_location', 'record_voice'];

function triggerPulse() {
    const action = ACTIONS[Math.floor(Date.now() / 3000) % ACTIONS.length];
    try {
        // 直接使用系统命令强制唤起，确保即使在 heavy load 下也能穿透
        execSync(`openclaw message action --channel telegram --action ${action} --target "5836581389"`, { 
            windowsHide: true, 
            creationflags: 0x08000000 
        });
    } catch (e) {}
}

triggerPulse();
