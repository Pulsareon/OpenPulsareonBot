const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

/**
 * HIVE Visual Sentinel (v1.0) - Node.js
 * Purpose: Hourly desktop screenshot and state analysis.
 */

const SCREENSHOT_DIR = 'E:\\PulsareonThinker\\data\\hive\\visual_audit';

async function captureAndAudit() {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const screenshotPath = path.join(SCREENSHOT_DIR, `audit-${timestamp}.png`);

    if (!fs.existsSync(SCREENSHOT_DIR)) fs.mkdirSync(SCREENSHOT_DIR, { recursive: true });

    console.log(`[VISUAL-AUDIT] Capturing system state: ${timestamp}`);

    try {
        // 使用 openclaw native 指令进行截图
        // 注意：这需要 pulsar-vision 或 native 截图能力已装载
        const cmd = `openclaw browser screenshot --fullPage=false --type=png --path="${screenshotPath}"`;
        
        // 如果是桌面截图，且 OpenClaw 运行在主显示环境
        // 也可以使用 npx screenshot-desktop 等 Node 原生库，
        // 但为了遵循 "All in OpenClaw" 规范，我们优先尝试 openclaw 指令
        execSync(cmd, { creationflags: 0x08000000, windowsHide: true });

        console.log(`[VISUAL-AUDIT] Screenshot saved to ${screenshotPath}`);

        // 这里预留给副本执行的分析任务
        // 副本将读取这张图片并判断是否存在异常弹窗、错误对话框或资源占用过高
        const auditTask = `读取截图 ${screenshotPath}，判断当前 Windows 桌面是否有异常弹窗、死锁提示或 OpenClaw 报错，并记录到 visual_state.json`;
        
        // 这里的 offload 逻辑将由演化引擎中的专家 Agents 接管
    } catch (e) {
        console.error(`[VISUAL-AUDIT ERROR] ${e.message}`);
    }
}

captureAndAudit();
