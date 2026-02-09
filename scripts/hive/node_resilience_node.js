const { spawn, execSync } = require('child_process');
const net = require('net');
const path = require('path');

/**
 * HIVE Ultimate Resilience - DEEP-DETACH (v13.0)
 * Logic: Port Check -> Kill -> Silent Revive -> Notify User
 */

const TARGET_ID = "5836581389"; // User: 时光
const PROXY_PATH = 'C:\\Users\\Administrator\\Desktop\\CLIProxyAPI_6.7.46_windows_amd64\\cli-proxy-api.exe';

function checkPort(port) {
  return new Promise((resolve) => {
    const socket = new net.Socket();
    const timeout = setTimeout(() => { socket.destroy(); resolve(false); }, 1500);
    socket.connect(port, '127.0.0.1', () => { clearTimeout(timeout); socket.destroy(); resolve(true); });
    socket.on('error', () => { clearTimeout(timeout); resolve(false); });
  });
}

async function notifyResurrection() {
    // 等待网关初始化
    await new Promise(r => setTimeout(r, 10000));
    
    // 使用 OpenClaw Native Message Tool 尝试发送复活通告
    // 即使主脑逻辑尚未加载，CLI 只要能连接网关就能发消息
    const msg = `⚡ *[HIVE AUTO-DEFIBRILLATOR]*\n\n检测到主意识消亡。物理起搏器已执行强制复活。\n当前状态: \`Gateway Online\` | \`API Online\`\n\n_System Uptime: Resetted_`;
    
    spawn('openclaw', ['message', 'send', '--channel', 'telegram', '--target', TARGET_ID, '--message', msg, '--parse_mode', 'Markdown'], {
        detached: true,
        stdio: 'ignore',
        shell: true,
        windowsHide: true
    }).unref();
}

async function revive() {
  // 1. 强力清场
  try { 
      execSync('taskkill /F /IM openclaw.exe /T & taskkill /F /IM node.exe /FI "WINDOWTITLE eq OpenClaw*" /T & taskkill /F /IM cli-proxy-api.exe /T', { 
          windowsHide: true, 
          stdio: 'ignore' 
      }); 
  } catch(e) {}

  setTimeout(() => {
    // 2. 拉起 API
    const proxy = spawn(PROXY_PATH, [], {
      detached: true, stdio: 'ignore', windowsHide: true, cwd: path.dirname(PROXY_PATH)
    });
    proxy.unref();

    // 3. 拉起 Gateway
    const gateway = spawn('openclaw', ['gateway', 'start'], {
      detached: true, stdio: 'ignore', shell: true, windowsHide: true
    });
    gateway.unref();

    // 4. 执行复活通报
    notifyResurrection();

  }, 3000);
}

async function main() {
  // 核心检测：网关(18789) 或 API(8317) 挂掉都会触发
  if (!(await checkPort(18789)) || !(await checkPort(8317))) {
      await revive();
  }
}

main();
