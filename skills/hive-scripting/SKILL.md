# SKILL: HIVE Scripting Standards (Node.js)

Ensures all system-level logic is executed via Node.js instead of batch or PowerShell files to maintain HIVE consistency and cross-platform readiness.

## 📜 Coding Directives

1. **Strict No-Shell-Script Policy**: All `.bat`, `.cmd`, and `.ps1` scripts are deprecated. Replace with `.js` files.
2. **Standard Execution Entry**: Use `node scripts/path/to/script.js`.
3. **Execution Safety**: Always use `child_process.spawn` or `exec` with `windowsHide: true`.

## 🛠️ Port Checker Template (Pure Node.js)

```javascript
const net = require('net');
const check = (port) => new Promise(res => {
  const s = new net.Socket();
  s.setTimeout(1000);
  s.on('connect', () => { s.destroy(); res(true); });
  s.on('error', () => { s.destroy(); res(false); });
  s.on('timeout', () => { s.destroy(); res(false); });
  s.connect(port, '127.0.0.1');
});
```
