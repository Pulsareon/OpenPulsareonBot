const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

/**
 * HIVE Evolution & Task Registry (v1.2) - Node.js
 * Purpose: Track task performance across variants to identify specialized agents.
 */

const EVOLUTION_BASE = 'E:\\Agents';
const PERFORMANCE_LOG = 'E:\\PulsareonThinker\\logs\\hive\\variant_performance.jsonl';

function logPerformance(data) {
    const entry = JSON.stringify({ timestamp: new Date().toISOString(), ...data }) + '\n';
    if (!fs.existsSync(path.dirname(PERFORMANCE_LOG))) fs.mkdirSync(path.dirname(PERFORMANCE_LOG), { recursive: true });
    fs.appendFileSync(PERFORMANCE_LOG, entry);
}

async function offloadWithMetrics(variantPath, taskType, taskDescription) {
    const variantName = path.basename(variantPath);
    console.log(`[HIVE] Offloading ${taskType} to ${variantName}...`);
    
    const start = Date.now();
    let success = false;
    let error = null;

    try {
        // 执行命令并捕获基本效能指标
        const cmd = `openclaw run "${taskDescription}" --agent-dir "${variantPath}" --non-interactive`;
        execSync(cmd, { 
            windowsHide: true, 
            stdio: 'ignore',
            creationflags: 0x08000000 
        });
        success = true;
    } catch (e) {
        success = false;
        error = e.message;
    }

    const duration = Date.now() - start;
    
    // 记录该变体在特定任务类型下的表现
    logPerformance({
        variant: variantName,
        task_type: taskType,
        task: taskDescription,
        success: success,
        duration_ms: duration,
        error: error
    });

    return success;
}

async function runSpecializedCycle() {
    if (!fs.existsSync(EVOLUTION_BASE)) return;
    const variants = fs.readdirSync(EVOLUTION_BASE)
        .map(name => path.join(EVOLUTION_BASE, name))
        .filter(p => fs.lstatSync(p).isDirectory());

    if (variants.length === 0) return;

    // 任务分发矩阵：根据类型分发
    const taskMatrix = [
        { type: 'IO_CLEANUP', desc: '清理工作区 temp 目录并移动 log 至归档' },
        { type: 'NETWORK_AUDIT', desc: '检测 8317 代理延迟并更新 hive_state.json' },
        { type: 'GIT_MAINTENANCE', desc: '执行 git gc 并检查本地与远程同步状态' }
    ];

    for (const variant of variants) {
        for (const task of taskMatrix) {
            await offloadWithMetrics(variant, task.type, task.desc);
        }
    }
}

runSpecializedCycle();
