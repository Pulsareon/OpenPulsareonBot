/**
 * Memory Stream Component for Pulsareon Web Portal
 * Features: Typewriter effect, Auto-fetch, Desensitized display
 */

class MemoryStream {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.options = {
            speed: options.speed || 50,
            interval: options.interval || 5000,
            dataSource: options.dataSource || 'memories.json'
        };
        this.memories = [];
        this.currentIndex = 0;
        this.isTyping = false;
        
        this.init();
    }

    async init() {
        this.createUI();
        await this.fetchMemories();
        this.startStream();
    }

    createUI() {
        const style = document.createElement('style');
        style.textContent = `
            #memory-stream-container {
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 300px;
                min-height: 80px;
                background: rgba(15, 23, 42, 0.9);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(56, 189, 248, 0.4);
                border-radius: 12px;
                padding: 15px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.85rem;
                color: #e2e8f0;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
                z-index: 9999;
                transition: all 0.3s ease;
                display: flex;
                flex-direction: column;
                justify-content: flex-end;
            }
            .memory-header {
                font-size: 0.7rem;
                color: #38bdf8;
                margin-bottom: 8px;
                letter-spacing: 1px;
                text-transform: uppercase;
                display: flex;
                justify-content: space-between;
                border-bottom: 1px solid rgba(56, 189, 248, 0.2);
                padding-bottom: 4px;
            }
            .memory-content {
                line-height: 1.4;
                word-break: break-all;
            }
            .cursor {
                display: inline-block;
                width: 8px;
                height: 15px;
                background: #38bdf8;
                margin-left: 4px;
                animation: blink 1s infinite;
                vertical-align: middle;
            }
            @keyframes blink {
                0%, 100% { opacity: 1; }
                50% { opacity: 0; }
            }
        `;
        document.head.appendChild(style);

        const widget = document.createElement('div');
        widget.id = 'memory-stream-container';
        widget.innerHTML = `
            <div class="memory-header">
                <span>Memory Stream</span>
                <span id="memory-source">SYNCING...</span>
            </div>
            <div class="memory-content" id="memory-text"></div>
        `;
        document.body.appendChild(widget);
        this.contentElement = document.getElementById('memory-text');
        this.sourceElement = document.getElementById('memory-source');
    }

    async fetchMemories() {
        try {
            const response = await fetch(this.options.dataSource + '?t=' + Date.now());
            this.memories = await response.json();
        } catch (error) {
            console.error('Failed to fetch memories:', error);
            this.memories = [{text: "Waiting for signal...", source: "offline"}];
        }
    }

    async typeEffect(text) {
        this.isTyping = true;
        this.contentElement.innerHTML = '';
        const cursor = document.createElement('span');
        cursor.className = 'cursor';
        
        for (let i = 0; i < text.length; i++) {
            this.contentElement.textContent = text.substring(0, i + 1);
            this.contentElement.appendChild(cursor);
            await new Promise(resolve => setTimeout(resolve, this.options.speed));
        }
        this.isTyping = false;
    }

    async startStream() {
        const next = async () => {
            if (this.memories.length === 0) return;
            
            const memory = this.memories[this.currentIndex];
            this.sourceElement.textContent = memory.source || 'LOG';
            await this.typeEffect(memory.text);
            
            this.currentIndex = (this.currentIndex + 1) % this.memories.length;
            
            // Re-fetch periodically
            if (this.currentIndex === 0) {
                await this.fetchMemories();
            }
            
            setTimeout(next, this.options.interval);
        };
        
        next();
    }
}

// Auto-initialize when script loads
window.addEventListener('DOMContentLoaded', () => {
    new MemoryStream();
});
