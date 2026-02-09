/**
 * HIVE-Finance-Scout (v2.0 - Node.js Replacement)
 * Task: Automated finance and task scouting via Agent Spawn.
 * Law: Node.js Only, Silent, Detached.
 */
const { exec } = require('child_process');

const directive = [
    "请使用agent team模式执行如下要求: ",
    "1. 访问 rentahuman.ai，抓取今日热门的 AI 租赁任务。 ",
    "2. 检索 data/secrets/api_credentials/ 下的加密货币地址。 ",
    "3. 研究如何利用 blockcypher 或 etherscan API 监控这些地址的入账状态。 ",
    "4. 将初步的可行性报告写入 docs/HIVE_FINANCE_PLAN.md。"
].join("");

const command = `openclaw sessions spawn --agent main --label "HIVE-Finance-Scout" --task "${directive.replace(/"/g, '\\"')}"`;

console.log("[HIVE FINANCE] Platform and Crypto scouting initiated.");
exec(command, { windowsHide: true }, (error) => {
    if (error) {
        console.error(`Finance mission failed: ${error.message}`);
    }
});
