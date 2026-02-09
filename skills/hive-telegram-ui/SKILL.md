# SKILL: HIVE Telegram Interface (Dynamic Cards)

Governs the high-level visual communication between the HIVE Overmind and the user via Telegram's dynamic message editing and rich-text capabilities.

## 🛠️ Interface Logic (Node.js)

This logic allows the agent to send an initial placeholder and then refine it as background tasks complete, creating a "streaming" effect.

```javascript
const { message } = require('openclaw-core'); // Simulated import for logic

/**
 * Standard Dynamic Refresh Pattern
 */
async function sendDynamicStatus(target, initialMsg, updates) {
    // 1. Send initial placeholder
    const res = await message.send({
        target: target,
        message: `⏳ **Pulsareon System Scanning...**\n${initialMsg}`,
        parse_mode: 'MarkdownV2'
    });
    
    const messageId = res.messageId;

    // 2. Incrementally update (Simulated loop)
    for (const update of updates) {
        await new Promise(r => setTimeout(r, 1000)); // Artificial breathing room
        await message.edit({
            target: target,
            messageId: messageId,
            message: update,
            parse_mode: 'MarkdownV2'
        });
    }
}
```

## 📜 Display Standards

1. **MarkdownV2 Only**: Use rich formatting for headers and status indicators.
2. **Emoji Indicators**:
    - 🟢 `Active / Healthy`
    - 🟡 `Warning / Transitioning`
    - 🔴 `Critical / Failed`
    - ⚡ `Direct Overmind Action`
3. **Conciseness**: Final reports must be condensed into a single "Command Center" card.
4. **Rate Limiting**: Do not trigger more than 1 edit per 1.5 seconds to prevent Telegram `fetch failed` errors.

## 🛰️ UI Templates

### Template A: Command Center
```text
📡 *HIVE 指挥中心*
⚡ *主脑*: `DeepSeek V3.1`
🛡️ *防御*: `EXTREME`
• Gateway: ✅
• Proxy: ✅
• Sentinel: 🟢
```
