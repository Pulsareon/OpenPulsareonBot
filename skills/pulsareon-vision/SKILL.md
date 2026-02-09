# SKILL: Pulsareon Vision (Node.js)

Governs the visual perception and environmental analysis of the Pulsareon system.

## 👁️ Visual Logic (Node.js)

```javascript
const { execSync } = require('child_process');
const path = require('path');

/**
 * Capture and Analyze
 */
async function captureDesktop() {
    const timestamp = Date.now();
    const savePath = `E:\\PulsareonThinker\\data\\hive\\visual_audit\\shot-${timestamp}.png`;
    
    // Native OpenClaw command for silent capture
    const cmd = `openclaw browser screenshot --path="${savePath}"`;
    execSync(cmd, { windowsHide: true, creationflags: 0x08000000 });
    
    return savePath;
}
```

## 📜 Directives
- Adheres to [[HIVE_SAFETY_CORE.md]]
- All captures must be stored in `data/hive/visual_audit/`.
- Logic: **Pure Node.js**.
