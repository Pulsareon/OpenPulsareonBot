const { spawn, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

/**
 * HIVE ULTIMATE ISOLATION (v12.0)
 * Purpose: Ensure no process ever interacts with a terminal or blocks on stdin.
 */

const QUEUE_FILE = 'E:\\PulsareonThinker\\data\\queue\\pending_ops.json';
const LOG_FILE = 'E:\\PulsareonThinker\\logs\\hive\\executor.log';

function log(msg) {
    fs.appendFileSync(LOG_FILE, `${new Date().toISOString()} - ${msg}\n`);
}

async function safeExecute(task) {
    const { action, target } = task;

    if (action === 'exec') {
        log(`[ISOLATED-EXEC] ${target}`);
        
        // 核心加固：使用 detached + stdio ignore + windowsHide
        // 彻底杜绝控制台 QuickEdit 模式对进程的影响
        const child = spawn(target, [], {
            shell: true,
            detached: true,
            windowsHide: true,
            stdio: 'ignore', // 物理关闭 stdin/stdout/stderr 管道
            creationflags: 0x08000000 | 0x00000008 // CREATE_NO_WINDOW | DETACHED_PROCESS
        });

        child.unref(); // 让父进程不再等待子进程，彻底断开物理关联
        return true;
    }
    // ... 其他逻辑
    return true;
}

// ... 轮询逻辑已优化为 stdio: ignore 环境
log('HIVE v12.0 Isolated Executor Ready.');
