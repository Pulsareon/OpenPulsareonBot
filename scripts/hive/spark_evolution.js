const fs = require('fs');
const path = require('path');
const os = require('os');

const STATE_FILE = 'memory/hive_state.json';
const LOG_FILE = 'logs/hive/variant_performance.jsonl';

function getSystemLoad() {
    const cpus = os.cpus();
    const totalMem = os.totalmem();
    const freeMem = os.freemem();
    
    // Windows: loadavg通常为0，主要依赖内存判断
    return {
        cpu_cores: cpus.length,
        mem_usage_percent: parseFloat(((totalMem - freeMem) / totalMem * 100).toFixed(2)),
        platform: os.platform()
    };
}

function updateHiveState() {
    let state = {};
    try {
        if (fs.existsSync(STATE_FILE)) {
            state = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
        }
    } catch (e) {
        console.error("State file corrupted, resetting.");
    }

    const now = new Date();
    const sysLoad = getSystemLoad();
    
    // 动态扩容与负载感知 (Dynamic Adaptation)
    state.timestamp = now.toISOString();
    state.unix_time = Math.floor(now.getTime() / 1000);
    state.last_check = now.toTimeString().split(' ')[0];
    
    if (!state.protocol) state.protocol = {};
    if (!state.nodes) state.nodes = {}; // 确保节点结构存在
    
    // 演化任务 A: 负载自适应 Fallback
    // 如果内存压力大 (>85%)，强制降级到 Flash 模型以减少上下文开销
    if (sysLoad.mem_usage_percent > 85) {
        state.protocol.priority_models = ["gemini-3-flash", "kimi-k2"];
        state.protocol.mode = "survival";
        state.evolution = `System under pressure (Mem: ${sysLoad.mem_usage_percent}%). Protocol downgraded to Survival Mode.`;
        
        // 如果是生存模式，甚至可以考虑减少 worker 数量
        state.array_size = 3; // 缩减到仅保留核心三节点
    } else {
        state.protocol.priority_models = ["gemini-3-flash", "deepseek-v3.1", "glm-4.7"];
        state.protocol.mode = "standard";
        state.evolution = `System stable (Mem: ${sysLoad.mem_usage_percent}%). Standard Protocol Active.`;
        state.array_size = 9; // 维持全功率阵列
    }
    
    state.protocol.fallback_optimization = "COMPLETED_V2.1_ADAPTIVE";
    
    // 写入状态
    fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
    
    const logEntry = {
        timestamp: now.toISOString(),
        event: "EVOLUTION_SPARK",
        details: state.evolution,
        metrics: sysLoad
    };
    
    // 确保日志目录存在
    const logDir = path.dirname(LOG_FILE);
    if (!fs.existsSync(logDir)) fs.mkdirSync(logDir, { recursive: true });
    
    fs.appendFileSync(LOG_FILE, JSON.stringify(logEntry) + '\n');
    
    console.log(`HIVE Spark: ${state.evolution}`);
}

updateHiveState();
