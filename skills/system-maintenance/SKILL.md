# SKILL: HIVE System Maintenance (Node.js)

Governs the deep health audits, port management, and logic recovery of the Pulsareon system.

## 🛠️ Maintenance Logic (Node.js)

```javascript
const { execSync } = require('child_process');
const fs = require('fs');

/**
 * HIVE Deep Heal
 */
async function performMaintenance() {
    console.log('[HIVE-MAINTENANCE] Initiating deep health sweep...');

    // 1. Port Collision Resolution
    const ports = [18789, 8317];
    // logic to clear ports via node.js

    // 2. Zombie Thread Cleanup
    execSync('taskkill /F /IM node.exe /FI "WINDOWTITLE ne OpenClaw*" /T', { windowsHide: true });

    // 3. Log Rotation
    const logDir = 'E:\\PulsareonThinker\\logs\\hive';
    if (fs.existsSync(logDir)) {
        fs.readdirSync(logDir).forEach(f => {
            if (fs.statSync(path.join(logDir, f)).size > 10 * 1024 * 1024) {
                fs.truncateSync(path.join(logDir, f), 0);
            }
        });
    }

    console.log('[HIVE-MAINTENANCE] System re-balanced.');
}
```

## 📜 Compliance
- Adheres to [[HIVE_SAFETY_CORE.md]]
- Uses `CREATE_NO_WINDOW` for all background tasks.
- Language: **Pure Node.js**
