const fs = require('fs');
const { execSync, spawn } = require('child_process');
const path = require('path');

/**
 * HIVE WATCHDOG (v1.0) - Node.js Edition
 * Purpose: Detect logic freezes, handle Git snapshots, and force recovery.
 */

const STATE_FILE = 'E:\\PulsareonThinker\\memory\\hive_state.json';
const LOCK_FILE = 'E:\\PulsareonThinker\\data\\hive\\watchdog.lock';
const MAX_STALE_SECONDS = 300; // 5 minutes without logic update = frozen

function getTimestamp() { return Math.floor(Date.now() / 1000); }

function gitSnapshot(commitMsg) {
  try {
    console.log(`[WATCHDOG] Creating snapshot: ${commitMsg}`);
    execSync('git add .', { windowsHide: true });
    execSync(`git commit -m "${commitMsg}"`, { windowsHide: true });
  } catch (e) {
    // If no changes, commit will fail, which is fine
  }
}

function checkLogicHealth() {
  if (!fs.existsSync(STATE_FILE)) return false;
  try {
    const state = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
    const lastCheckin = state.last_checkin || 0;
    const diff = getTimestamp() - lastCheckin;
    
    // If last_checkin is too old, the main logic loop is frozen
    return diff < MAX_STALE_SECONDS;
  } catch (e) {
    return false;
  }
}

async function forceRevive() {
  console.log('[WATCHDOG] CRITICAL: System frozen or crashed. Rolling back and restarting.');
  
  // 1. Snapshot current bad state for debugging
  gitSnapshot('HIVE-WATCHDOG: Auto-snapshot before recovery');

  // 2. Kill everything
  const killCmd = 'taskkill /F /IM openclaw.exe /T & taskkill /F /IM node.exe /FI "WINDOWTITLE eq OpenClaw*" /T & taskkill /F /IM cli-proxy-api.exe /T';
  try { execSync(killCmd, { windowsHide: true }); } catch(e) {}

  // 3. Restart core via silent launcher
  setTimeout(() => {
    spawn('wscript.exe', ['E:\\PulsareonThinker\\scripts\\hive\\silent_launcher.vbs'], {
      detached: true,
      stdio: 'ignore',
      windowsHide: true
    }).unref();
  }, 5000);
}

function main() {
  // Prevent multiple watchdog instances
  if (fs.existsSync(LOCK_FILE)) {
    const stats = fs.statSync(LOCK_FILE);
    if (Date.now() - stats.mtimeMs < 50000) return; // Still running
  }
  fs.writeFileSync(LOCK_FILE, Date.now().toString());

  if (!checkLogicHealth()) {
    forceRevive();
  } else {
    // If healthy, do a routine incremental commit
    gitSnapshot('HIVE-WATCHDOG: Routine healthy sync');
  }

  fs.unlinkSync(LOCK_FILE);
}

main();
