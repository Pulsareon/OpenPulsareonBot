const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

/**
 * HIVE Workspace Organizer (Node.js Edition) - v1.1
 * Fixed: UTF-8 encoding and character errors.
 */

function cleanupDesktop() {
    const desktopPath = path.join(process.env.USERPROFILE, 'Desktop');
    const targetFolder = 'C:\\Users\\Administrator\\Desktop\\Archive\\Clutter_Cleanup';
    
    if (!fs.existsSync(targetFolder)) fs.mkdirSync(targetFolder, { recursive: true });

    const files = fs.readdirSync(desktopPath);
    files.forEach(file => {
        // Only move specific non-critical files
        if (file.endsWith('.txt') || file.endsWith('.log') || file.endsWith('.tmp')) {
            try {
                fs.renameSync(path.join(desktopPath, file), path.join(targetFolder, file));
            } catch (e) {}
        }
    });
}

function killZombieProcesses() {
    const targets = ['cmd.exe', 'powershell.exe', 'python.exe', 'pythonw.exe'];
    targets.forEach(proc => {
        try {
            // Use taskkill with silent flags
            execSync(`taskkill /F /IM ${proc} /T`, { stdio: 'ignore' });
        } catch (e) {}
    });
}

function main() {
    try {
        cleanupDesktop();
        console.log('HIVE Cleanup complete.');
    } catch (e) {
        console.error('Cleanup failed:', e.message);
    }
}

main();
