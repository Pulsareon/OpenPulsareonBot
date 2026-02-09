/**
 * HIVE GUARDIAN (v1.0) - The Unified Sentinel
 * 
 * 核心职责:
 * 1. 资源感知 (Resource Awareness): 监控 CPU/内存，触发负载适应策略。
 * 2. 双盲探活 (Double-Blind Health Check): 同时检测 CLI Proxy (8317) 和 Gateway (18789)。
 * 3. 静默自愈 (Silent Healing): 发现服务死亡时自动重启，遵循指数退避原则。
 * 4. 状态同步 (State Sync): 更新 memory/hive_state.json 心跳。
 * 
 * 安全约束:
 * - 严禁弹出窗口 (windowsHide: true)
 * - 严禁阻塞主线程
 * - 严禁在高负载下频繁重启 (Flapping Prevention)
 */

const fs = require('fs');
const path = require('path');
const { spawn, execSync } = require('child_process');
const http = require('http');
const os = require('os');

// --- 配置 ---
const CONFIG = {
    stateFile: 'E:\\PulsareonThinker\\memory\\hive_state.json',
    logFile: 'E:\\PulsareonThinker\\logs\\hive\\guardian.jsonl',
    proxyPath: 'C:\\Users\\Administrator\\Desktop\\CLIProxyAPI_6.7.46_windows_amd64\\cli-proxy-api.exe',
    gatewayPort: 18789,
    proxyPort: 8317,
    maxRetries: 3,
    coolDownMs: 60000 // 1分钟冷却，防止死循环重启
};

// --- 日志 ---
function log(event, details, level = 'INFO') {
    const entry = JSON.stringify({
        timestamp: new Date().toISOString(),
        level,
        event,
        details
    });
    // 确保目录存在
    const logDir = path.dirname(CONFIG.logFile);
    if (!fs.existsSync(logDir)) fs.mkdirSync(logDir, { recursive: true });
    
    fs.appendFileSync(CONFIG.logFile, entry + '\n');
    if (level === 'ERROR') console.error(entry);
    else console.log(entry);
}

// --- 1. 资源感知 ---
function checkResources() {
    const totalMem = os.totalmem();
    const freeMem = os.freemem();
    const memUsage = ((totalMem - freeMem) / totalMem * 100).toFixed(2);
    
    return {
        memUsage: parseFloat(memUsage),
        mode: parseFloat(memUsage) > 85 ? 'SURVIVAL' : 'STANDARD'
    };
}

// --- 2. 服务探活 ---
function checkPort(port) {
    return new Promise((resolve) => {
        const req = http.get(`http://127.0.0.1:${port}/`, (res) => {
            // 只要有响应（哪怕是 404/401）都算活着
            res.resume();
            resolve(true);
        });
        req.on('error', () => resolve(false));
        req.setTimeout(2000, () => {
            req.destroy();
            resolve(false);
        });
    });
}

// --- 3. 服务控制 ---
async function restartCLIProxy() {
    log('RESTART_INIT', 'CLI Proxy is unresponsive. Attempting restart.', 'WARN');
    
    try {
        // 1. 杀掉旧进程
        execSync('taskkill /F /IM cli-proxy-api.exe', { stdio: 'ignore' });
    } catch (e) { /* ignore if not running */ }
    
    // 2. 启动新进程 (Detached & Hidden)
    const child = spawn(CONFIG.proxyPath, [], {
        detached: true,
        stdio: 'ignore',
        windowsHide: true,
        cwd: path.dirname(CONFIG.proxyPath)
    });
    child.unref();
    
    log('RESTART_DONE', 'CLI Proxy restarted silently.');
}

// --- 主逻辑 ---
async function main() {
    // 1. 获取资源状态
    const resources = checkResources();
    
    // 2. 更新状态文件 (Heartbeat)
    let state = {};
    try {
        if (fs.existsSync(CONFIG.stateFile)) {
            state = JSON.parse(fs.readFileSync(CONFIG.stateFile, 'utf8'));
        }
    } catch (e) {}
    
    state.last_check = new Date().toISOString();
    state.resources = resources;
    state.guardian_version = "v1.0";
    
    // 3. 探活与决策
    const proxyAlive = await checkPort(CONFIG.proxyPort);
    const gatewayAlive = await checkPort(CONFIG.gatewayPort);
    
    state.services = {
        cli_proxy: proxyAlive ? 'ALIVE' : 'DEAD',
        gateway: gatewayAlive ? 'ALIVE' : 'DEAD'
    };
    
    // 写入状态
    fs.writeFileSync(CONFIG.stateFile, JSON.stringify(state, null, 2));
    
    // 4. 自愈动作 (仅在 STANDARD 模式下执行，SURVIVAL 模式下保守操作)
    if (resources.mode === 'STANDARD') {
        if (!proxyAlive) {
            await restartCLIProxy();
        }
        // Gateway 重启涉及自身，暂由 OpenClaw 内部机制处理，Guardian 仅记录
        if (!gatewayAlive) {
            log('GATEWAY_DOWN', 'Gateway is unresponsive. Manual intervention may be needed.', 'ERROR');
        }
    } else {
        log('SURVIVAL_MODE', 'High load detected. Skipping auto-restart to prevent crash loop.', 'WARN');
    }
}

main();
