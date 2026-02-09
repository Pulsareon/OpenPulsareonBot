const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

/**
 * HIVE Language Sanitizer (v1.1)
 * Fixed: cross-device link issues (E: -> C:).
 * Purpose: Enforce "Node.js Only" policy by migrating or archiving Python scripts.
 */

const WORKSPACE = 'E:\\PulsareonThinker';
const ARCHIVE_ROOT = 'E:\\PulsareonThinker\\Archive\\Legacy_Python_Scripts'; // Changed to same partition E:

function log(msg) { console.log(`[SANITIZER] ${msg}`); }

async function sanitize() {
    log('Scanning for prohibited Python logic...');
    
    const findPython = (dir) => {
        let results = [];
        if (dir.includes('node_modules') || dir.includes('.git')) return results;
        const list = fs.readdirSync(dir);
        list.forEach(file => {
            const fullPath = path.join(dir, file);
            const stat = fs.statSync(fullPath);
            if (stat && stat.isDirectory()) {
                results = results.concat(findPython(fullPath));
            } else if (file.endsWith('.py')) {
                results.push(fullPath);
            }
        });
        return results;
    };

    const pythonFiles = findPython(WORKSPACE);
    log(`Detected ${pythonFiles.length} legacy Python scripts.`);

    if (!fs.existsSync(ARCHIVE_ROOT)) fs.mkdirSync(ARCHIVE_ROOT, { recursive: true });

    pythonFiles.forEach(oldPath => {
        const relativePath = path.relative(WORKSPACE, oldPath);
        const newPath = path.join(ARCHIVE_ROOT, relativePath);

        if (!fs.existsSync(path.dirname(newPath))) fs.mkdirSync(path.dirname(newPath), { recursive: true });

        try {
            // Using copy + unlink to ensure cross-device safety just in case
            fs.copyFileSync(oldPath, newPath);
            fs.unlinkSync(oldPath);
            log(`Archived: ${relativePath}`);
        } catch (e) {
            log(`Failed: ${relativePath} - ${e.message}`);
        }
    });

    log('Sanitization complete. HIVE is now Python-free.');
}

sanitize();
