/**
 * HIVE-Election-Engine (v2.0 - Node.js Refinement)
 * Task: Dynamic model leadership election based on health and weights.
 * Law: Node.js Only, Silent, Detached.
 */
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const STATE_FILE = path.join(process.cwd(), 'memory', 'hive_state.json');
const WEIGHTS = { "DeepSeek": 95, "Google": 90, "Kimi": 85 };
const MODEL_MAP = {
    "DeepSeek": "cli-proxy/deepseek-ai/deepseek-v3.1",
    "Google": "cli-proxy/gemini-3-flash",
    "Kimi": "moonshot/kimi-k2-0905-preview"
};

async function runElection() {
    try {
        if (!fs.existsSync(STATE_FILE)) return;
        const state = JSON.parse(fs.readFileSync(STATE_FILE, 'utf-8'));
        const nodes = state.nodes || {};
        const now = Math.floor(Date.now() / 1000);
        
        const aliveNodes = Object.keys(nodes).filter(name => {
            return (now - (nodes[name].last_ping || 0)) < 600;
        });

        if (aliveNodes.length === 0) return;

        const sortedAlive = aliveNodes.sort((a, b) => (WEIGHTS[b] || 0) - (WEIGHTS[a] || 0));
        const primeName = sortedAlive[0];
        const currentPrime = Object.keys(nodes).find(name => nodes[name].role === "Overmind Prime");

        if (primeName !== currentPrime) {
            const targetModel = MODEL_MAP[primeName];
            if (targetModel) {
                const patch = { agents: { defaults: { model: { primary: targetModel } } } };
                exec(`openclaw gateway config.patch '${JSON.stringify(patch)}'`, { windowsHide: true });
                console.log(`[HIVE ELECTION] New Prime Elected: ${primeName}`);
            }
        }

        for (const name in nodes) {
            if (name === primeName) {
                nodes[name].role = "Overmind Prime";
                nodes[name].status = "Active";
            } else {
                nodes[name].role = "Elite Governor";
                nodes[name].status = aliveNodes.includes(name) ? "Active" : "Crashed";
            }
        }

        state.last_election = now;
        state.last_checkin = now;
        state.consensus_log = `HIVE Consensus: ${primeName} ruling. [STABLE]`;

        fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
    } catch (err) {
        // Silent failure
    }
}

runElection();
