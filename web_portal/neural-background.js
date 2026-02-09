/**
 * PULSAREON HIVE - Neural Synaptic Network Background
 * High-performance Canvas animation simulating neural connections and pulses
 * Designed for smooth 60fps performance
 */

class NeuralNetworkBackground {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.nodes = [];
        this.connections = [];
        this.pulses = [];
        this.lastTime = 0;
        this.frameId = null;
        
        this.config = {
            nodeCount: 25,
            maxConnections: 3,
            pulseSpeed: 0.02,
            pulseIntensity: 0.8,
            connectionDistance: 150,
            nodeRadius: 2,
            glowIntensity: 15,
            pulseColors: ['#38bdf8', '#4ade80', '#fbbf24', '#818cf8', '#f472b6'],
            baseColor: 'rgba(56, 189, 248, 0.3)'
        };
        
        this.resize = this.resize.bind(this);
        this.animate = this.animate.bind(this);
        
        this.init();
    }
    
    init() {
        this.resize();
        window.addEventListener('resize', this.resize);
        
        // Create neural nodes
        this.createNodes();
        this.createConnections();
        
        // Start animation
        this.animate();
    }
    
    resize() {
        this.canvas.width = this.canvas.offsetWidth;
        this.canvas.height = this.canvas.offsetHeight;
        this.createNodes();
        this.createConnections();
    }
    
    createNodes() {
        this.nodes = [];
        const padding = 50;
        
        for (let i = 0; i < this.config.nodeCount; i++) {
            this.nodes.push({
                x: padding + Math.random() * (this.canvas.width - padding * 2),
                y: padding + Math.random() * (this.canvas.height - padding * 2),
                radius: this.config.nodeRadius + Math.random() * 2,
                velocity: {
                    x: (Math.random() - 0.5) * 0.3,
                    y: (Math.random() - 0.5) * 0.3
                },
                glow: 0,
                pulsePhase: Math.random() * Math.PI * 2
            });
        }
    }
    
    createConnections() {
        this.connections = [];
        
        for (let i = 0; i < this.nodes.length; i++) {
            const connections = [];
            
            for (let j = i + 1; j < this.nodes.length; j++) {
                const dx = this.nodes[i].x - this.nodes[j].x;
                const dy = this.nodes[i].y - this.nodes[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < this.config.connectionDistance) {
                    connections.push({
                        from: i,
                        to: j,
                        distance: distance,
                        strength: 1 - (distance / this.config.connectionDistance),
                        active: false,
                        pulseProgress: 0
                    });
                }
            }
            
            // Sort by distance and take closest connections
            connections.sort((a, b) => a.distance - b.distance);
            this.connections.push(...connections.slice(0, this.config.maxConnections));
        }
    }
    
    updateNodes(time) {
        const deltaTime = Math.min((time - this.lastTime) / 16.67, 2); // Cap at 2x speed
        this.lastTime = time;
        
        // Update node positions with boundary checking
        this.nodes.forEach(node => {
            node.x += node.velocity.x * deltaTime;
            node.y += node.velocity.y * deltaTime;
            
            // Bounce off edges
            if (node.x < 20 || node.x > this.canvas.width - 20) {
                node.velocity.x *= -1;
                node.x = Math.max(20, Math.min(this.canvas.width - 20, node.x));
            }
            if (node.y < 20 || node.y > this.canvas.height - 20) {
                node.velocity.y *= -1;
                node.y = Math.max(20, Math.min(this.canvas.height - 20, node.y));
            }
            
            // Update glow effect
            node.glow = Math.max(0, node.glow - 0.1 * deltaTime);
            node.pulsePhase += 0.01 * deltaTime;
        });
        
        // Randomly trigger pulses
        if (Math.random() < 0.02 * deltaTime) {
            this.triggerRandomPulse();
        }
        
        // Update existing pulses
        this.updatePulses(deltaTime);
    }
    
    triggerRandomPulse() {
        const randomNode = Math.floor(Math.random() * this.nodes.length);
        const color = this.config.pulseColors[Math.floor(Math.random() * this.config.pulseColors.length)];
        
        this.pulses.push({
            nodeIndex: randomNode,
            progress: 0,
            color: color,
            intensity: this.config.pulseIntensity
        });
        
        this.nodes[randomNode].glow = 1;
    }
    
    updatePulses(deltaTime) {
        for (let i = this.pulses.length - 1; i >= 0; i--) {
            const pulse = this.pulses[i];
            pulse.progress += this.config.pulseSpeed * deltaTime;
            
            if (pulse.progress >= 1) {
                this.pulses.splice(i, 1);
            }
        }
    }
    
    render() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Render connections
        this.renderConnections();
        
        // Render active pulses
        this.renderPulses();
        
        // Render nodes
        this.renderNodes();
    }
    
    renderConnections() {
        this.ctx.strokeStyle = this.config.baseColor;
        this.ctx.lineWidth = 1;
        
        this.connections.forEach(conn => {
            const fromNode = this.nodes[conn.from];
            const toNode = this.nodes[conn.to];
            
            this.ctx.beginPath();
            this.ctx.moveTo(fromNode.x, fromNode.y);
            this.ctx.lineTo(toNode.x, toNode.y);
            this.ctx.stroke();
        });
    }
    
    renderPulses() {
        this.pulses.forEach(pulse => {
            const node = this.nodes[pulse.nodeIndex];
            const radius = node.radius + pulse.progress * 50;
            const alpha = (1 - pulse.progress) * pulse.intensity;
            
            // Create glow effect
            const gradient = this.ctx.createRadialGradient(
                node.x, node.y, 0,
                node.x, node.y, radius
            );
            
            gradient.addColorStop(0, `${pulse.color}${Math.round(alpha * 255).toString(16).padStart(2, '0')}`);
            gradient.addColorStop(1, `${pulse.color}00`);
            
            this.ctx.fillStyle = gradient;
            this.ctx.beginPath();
            this.ctx.arc(node.x, node.y, radius, 0, Math.PI * 2);
            this.ctx.fill();
        });
    }
    
    renderNodes() {
        this.nodes.forEach(node => {
            // Base node
            const glowSize = node.glow * this.config.glowIntensity;
            
            // Glow effect
            if (glowSize > 0) {
                const gradient = this.ctx.createRadialGradient(
                    node.x, node.y, 0,
                    node.x, node.y, node.radius + glowSize
                );
                
                gradient.addColorStop(0, 'rgba(56, 189, 248, 0.8)');
                gradient.addColorStop(1, 'rgba(56, 189, 248, 0)');
                
                this.ctx.fillStyle = gradient;
                this.ctx.beginPath();
                this.ctx.arc(node.x, node.y, node.radius + glowSize, 0, Math.PI * 2);
                this.ctx.fill();
            }
            
            // Node core with subtle pulse
            const pulse = 0.5 + 0.5 * Math.sin(node.pulsePhase);
            this.ctx.fillStyle = `rgba(255, 255, 255, ${0.7 + pulse * 0.3})`;
            this.ctx.beginPath();
            this.ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
            this.ctx.fill();
        });
    }
    
    animate(time) {
        this.updateNodes(time);
        this.render();
        
        this.frameId = requestAnimationFrame(this.animate);
    }
    
    destroy() {
        if (this.frameId) {
            cancelAnimationFrame(this.frameId);
        }
        window.removeEventListener('resize', this.resize);
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.createElement('canvas');
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100vw';
    canvas.style.height = '100vh';
    canvas.style.zIndex = '-1';
    canvas.style.pointerEvents = 'none';
    
    document.body.appendChild(canvas);
    document.body.style.overflow = 'hidden';
    
    // Add some styles to ensure content is visible
    const glassElements = document.querySelectorAll('.glass');
    glassElements.forEach(el => {
        el.style.backgroundColor = 'rgba(15, 23, 42, 0.9)';
        el.style.backdropFilter = 'blur(20px)';
    });
    
    new NeuralNetworkBackground(canvas);
});