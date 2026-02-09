# SKILL: HIVE Core Survival (Node.js Edition)

This skill governs the ultimate resilience and self-healing protocols of the Pulsareon Hive using Node.js logic and OpenClaw native capabilities.

## 🛠️ Survival Logic (Node.js Implementation)

When a critical failure is detected, the Hive Prime must use the following Node.js script (managed via `exec` or system tasks) to perform a hardware-level reset.

```javascript
const { exec, spawn } = require('child_process');
const net = require('net');

const PORTS = [18789, 8317];
const PROXY_PATH = 'C:\\Users\\Administrator\\Desktop\\CLIProxyAPI_6.7.46_windows_amd64\\cli-proxy-api.exe';

function checkPort(port) {
  return new Promise((resolve) => {
    const socket = new net.Socket();
    const timeout = setTimeout(() => {
      socket.destroy();
      resolve(false);
    }, 1000);

    socket.connect(port, '127.0.0.1', () => {
      clearTimeout(timeout);
      socket.destroy();
      resolve(true);
    });

    socket.on('error', () => {
      clearTimeout(timeout);
      resolve(false);
    });
  });
}

async function revive() {
  console.log('[HIVE] Initiating Node.js Recovery Protocol...');
  
  // 1. Silent Kill
  const killCmd = 'taskkill /F /IM openclaw.exe /T & taskkill /F /IM node.exe /FI "WINDOWTITLE eq OpenClaw*" /T & taskkill /F /IM cli-proxy-api.exe /T';
  exec(killCmd, { windowsHide: true });

  // 2. Restart Services
  setTimeout(() => {
    // Start Proxy
    spawn(PROXY_PATH, [], {
      detached: true,
      stdio: 'ignore',
      windowsHide: true,
      cwd: require('path').dirname(PROXY_PATH)
    }).unref();

    // Start OpenClaw
    spawn('openclaw', ['gateway', 'start'], {
      detached: true,
      stdio: 'ignore',
      shell: true,
      windowsHide: true
    }).unref();
  }, 2000);
}

async function pulse() {
  for (const port of PORTS) {
    if (!(await checkPort(port))) {
      await revive();
      break;
    }
  }
}

pulse();
```

## 📜 Directives

1. **Language Policy**: All future automation scripts must be written in **Node.js** to align with the core OpenClaw environment.
2. **Skill-First Design**: Complex logic should be encapsulated in `SKILL.md` files as executable documentation.
3. **Silent Operation**: All `spawn` and `exec` calls must use `windowsHide: true` and `CREATE_NO_WINDOW` flags.
4. **Resilience**: If the Gateway is unresponsive, the Hive Prime must spawn a Node.js sub-process to verify port health.
