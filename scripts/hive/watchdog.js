const fs = require('fs');
const { execSync } = require('child_process');

const ACTION = process.argv[2]; // PREPARE, COMMIT, or ROLLBACK
const GIT_TAG = "watchdog_sync";

function log(msg) {
    console.log(`[Watchdog] ${new Date().toISOString()} - ${msg}`);
}

try {
    if (ACTION === 'PREPARE') {
        log("Creating safety snapshot...");
        // Ensure no leftover tag
        try { execSync(`git tag -d ${GIT_TAG}`, { stdio: 'ignore' }); } catch(e) {}
        execSync('git add .');
        try {
            execSync('git commit -m "Watchdog pre-action snapshot"', { stdio: 'ignore' });
        } catch (e) {
            log("No changes to commit, proceeding with current HEAD.");
        }
        execSync(`git tag ${GIT_TAG}`);
        log("Snapshot created and tagged.");
    } else if (ACTION === 'ROLLBACK') {
        log("CRITICAL ERROR DETECTED. Starting rollback...");
        // Reset code/config but keep memory/ and logs/
        // Stash memory first
        execSync('git add memory/ logs/ data/state/');
        execSync('git stash push -m "Watchdog preserved data"');
        // Rollback to tag
        execSync(`git reset --hard ${GIT_TAG}`);
        // Pop memory back
        try { execSync('git stash pop'); } catch(e) { log("Note: No data stash to pop."); }
        log("Rollback complete. System state restored (Memory preserved).");
    } else if (ACTION === 'COMMIT') {
        log("Action successful. Finalizing commit...");
        execSync('git add .');
        execSync('git commit -m "HIVE Configuration Update: Success"');
        try { execSync(`git tag -d ${GIT_TAG}`); } catch(e) {}
        log("HIVE state synchronized.");
    }
} catch (error) {
    console.error(`[Watchdog Error] ${error.message}`);
    process.exit(1);
}
