const fs = require('fs');
const { exec } = require('child_process');
const path = require('path');

const WORKSPACE = 'E:\\PulsareonThinker';
const TARGET_LOAD = 0.9; // 90%

function cpuIntensiveTask() {
    let x = 0;
    for (let i = 0; i < 10000000; i++) {
        x += Math.sqrt(Math.random());
    }
    return x;
}

function diskIntensiveTask() {
    const tempFile = path.join(WORKSPACE, `temp_stress_${process.pid}_${Date.now()}.tmp`);
    const data = Buffer.alloc(1024 * 1024 * 10, 'X'); // 10MB
    fs.writeFileSync(tempFile, data);
    fs.readFileSync(tempFile);
    fs.unlinkSync(tempFile);
}

function analysisTask() {
    // 模拟分析任务
    const files = fs.readdirSync(path.join(WORKSPACE, 'rules'));
    files.forEach(f => {
        const content = fs.readFileSync(path.join(WORKSPACE, 'rules', f), 'utf8');
        content.split('').reverse().join(''); // 消耗 CPU
    });
}

log("Starting System Stress & Analysis Evolution...");

// 启动大规模并发
const concurrency = 20;
for (let i = 0; i < concurrency; i++) {
    setInterval(() => {
        cpuIntensiveTask();
        diskIntensiveTask();
        analysisTask();
    }, 50);
}

function log(msg) {
    console.log(`[STRESS] ${new Date().toISOString()} - ${msg}`);
}

// 运行 2 分钟后自动退出（或被终止）
setTimeout(() => {
    log("Stress cycle complete.");
    process.exit(0);
}, 120000);
