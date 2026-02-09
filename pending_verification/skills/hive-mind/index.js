import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PYTHON_SCRIPT = path.join(__dirname, 'main.py');

async function runPython(command, args = {}) {
  return new Promise((resolve, reject) => {
    const pyArgs = [command];
    for (const [k, v] of Object.entries(args)) {
      if (v) {
        pyArgs.push(`--${k}`);
        pyArgs.push(String(v));
      }
    }
    
    const py = spawn('python', [PYTHON_SCRIPT, ...pyArgs]);
    let out = '';
    let err = '';
    
    py.stdout.on('data', (data) => out += data.toString());
    py.stderr.on('data', (data) => err += data.toString());
    
    py.on('close', (code) => {
      if (code !== 0) {
        // If Python fails, return error as result so LLM sees it
        resolve({ error: err || `Exit code ${code}` });
      } else {
        try {
          resolve(JSON.parse(out));
        } catch (e) {
          resolve({ result: out.trim() });
        }
      }
    });
  });
}

export async function hive_status() {
  return await runPython('status');
}

export async function hive_spawn(args) {
  return await runPython('spawn', args);
}
