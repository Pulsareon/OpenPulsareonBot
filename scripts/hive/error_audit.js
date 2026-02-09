const fs = require('fs');
const path = require('path');

/**
 * HIVE Error Auditor (v1.0) - Node.js
 * Purpose: Collect logs from the last 5 minutes for Overmind judgment.
 */

const LOG_FILES = [
    'E:\\PulsareonThinker\\logs\\hive\\executor.log',
    'E:\\PulsareonThinker\\logs\\hive\\security.log',
    'E:\\PulsareonThinker\\logs\\hive\\variant_performance.jsonl'
];

const LOOKBACK_MS = 5 * 60 * 1000; // 5 minutes

function audit() {
    const now = Date.now();
    let report = '';

    LOG_FILES.forEach(logPath => {
        if (!fs.existsSync(logPath)) return;
        
        try {
            const stats = fs.statSync(logPath);
            // Optimization: Only read if modified recently
            if (now - stats.mtimeMs > LOOKBACK_MS + 10000) return;

            const content = fs.readFileSync(logPath, 'utf8');
            const lines = content.split('\n');
            
            const recentErrors = lines.filter(line => {
                // Check if line contains common error keywords
                const isError = /ERROR|CRITICAL|failed|Exception|FAIL|Crashed/i.test(line);
                if (!isError) return false;

                // Attempt to parse ISO timestamp or just use file modification if parsing fails
                const timestampMatch = line.match(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/);
                if (timestampMatch) {
                    const lineTime = new Date(timestampMatch[0]).getTime();
                    return (now - lineTime) <= LOOKBACK_MS;
                }
                return true; // Fallback to including it if keywords match
            });

            if (recentErrors.length > 0) {
                report += `\n--- SOURCE: ${path.basename(logPath)} ---\n`;
                // Only take last 10 errors per file to keep context small
                report += recentErrors.slice(-10).join('\n') + '\n';
            }
        } catch (e) {
            // Silence log read errors to prevent recursion
        }
    });

    if (report) {
        console.log(`⚡ [HIVE ERROR AUDIT] Detection found:\n${report}\n\nOvermind, please judge the severity and execute self-healing if required.`);
    } else {
        console.log('HEARTBEAT_OK: No critical errors detected in the last 5 minutes.');
    }
}

audit();
