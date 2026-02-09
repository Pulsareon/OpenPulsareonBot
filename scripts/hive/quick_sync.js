const fs = require('fs');
const now = new Date();
const statePath = 'memory/hive_state.json';
const state = JSON.parse(fs.readFileSync(statePath, 'utf8'));

state.timestamp = now.toISOString();
state.unix_time = Math.floor(now.getTime() / 1000);
state.last_check = now.toLocaleTimeString('zh-CN', { hour12: false });
state.consensus_log = `HIVE Consensus: Pulse anchored at ${state.last_check}. Status: VIBRANT.`;

fs.writeFileSync(statePath, JSON.stringify(state, null, 2));
console.log(`Updated hive_state.json to ${state.last_check}`);

const alivePath = 'logs/HIVE_ALIVE.txt';
const aliveMsg = `${state.last_check}|ALIVE|HIVE_SPARK|STABLE`;
fs.writeFileSync(alivePath, aliveMsg);
console.log(`Updated HIVE_ALIVE.txt: ${aliveMsg}`);
