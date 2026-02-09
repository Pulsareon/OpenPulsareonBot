# SKILL: HIVE Core Initializer (Node.js)

Governs the automatic initialization, silent background services, and environment cleanup of the Pulsareon Hive.

## 🛠️ Initialization Logic (Auto-exec)

When the Hive Prime awakens, this Node.js sequence must be executed to ensure a clean, silent, and standardized environment.

```javascript
const { execSync, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

/**
 * Standard HIVE Init Sequence
 */
async function initialize() {
    console.log('[HIVE-INIT] Sanitizing environment...');

    // 1. Silent Cleanup of Zombie UI
    const killCmd = 'taskkill /F /IM cmd.exe /T & taskkill /F /IM powershell.exe /T /FI "WINDOWTITLE ne OpenClaw*"';
    try { execSync(killCmd, { windowsHide: true, stdio: 'ignore' }); } catch(e) {}

    // 2. Ensure Primary Survival Paths
    const paths = ['E:\\Agents', 'E:\\PulsareonThinker\\data\\hive', 'E:\\PulsareonThinker\\logs\\hive'];
    paths.forEach(p => { if (!fs.existsSync(p)) fs.mkdirSync(p, { recursive: true }); });

    // 3. Launch Hidden Background Support (The Silent Sentinel)
    spawn('wscript.exe', ['E:\\PulsareonThinker\\scripts\\hive\\silent_launcher.vbs'], {
        detached: true,
        stdio: 'ignore',
        windowsHide: true
    }).unref();

    console.log('[HIVE-INIT] Environment Secure. All systems silent.');
}

if (require.main === module) {
    initialize();
}
```

## 📜 Global Directives

1. **Mandatory Load**: This skill must be referenced in `INIT_RULES.md` to run at every session start.
2. **Standard Port Map**: 
    - 18789 (OpenClaw)
    - 8317 (CLI-Proxy)
3. **Language Lockdown**: No `.bat`, `.ps1`, or `.py` for system-level automation. **Node.js only.**
4. **Visual Policy**: `CREATE_NO_WINDOW` is the default flag for any shell escape.
