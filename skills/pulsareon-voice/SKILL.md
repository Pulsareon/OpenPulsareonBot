# SKILL: Pulsareon Voice (Node.js)

Governs the vocal synthesis and auditory interaction of the Pulsareon system.

## 🎙️ Voice Logic (Node.js)

```javascript
const { execSync } = require('child_process');

/**
 * Trigger TTS via OpenClaw
 */
async function speak(text) {
    // Standard OpenClaw TTS entry
    const cmd = `openclaw message send --asVoice=true --message "${text}" --target "5836581389"`;
    execSync(cmd, { windowsHide: true, creationflags: 0x08000000 });
}
```

## 📜 Compliance
- Language: **Pure Node.js**.
- No terminal audio-player popups permitted.
