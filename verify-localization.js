// 验证外部资源本地化
const fs = require('fs');
const path = require('path');

console.log('🔍 验证外部资源本地化...\n');

// 检查文件是否存在
const filesToCheck = [
    'web_portal/assets/js/chart.min.js',
    'web_portal/assets/css/fonts.css',
    'web_portal/assets/fonts/JetBrainsMono-Regular.woff2',
    'web_portal/assets/fonts/Orbitron-Regular.woff2',
    'web_portal/assets/fonts/Orbitron-Bold.woff2'
];

let allFilesExist = true;
filesToCheck.forEach(file => {
    const exists = fs.existsSync(file);
    console.log(`${exists ? '✅' : '❌'} ${file} ${exists ? '存在' : '缺失'}`);
    if (!exists) allFilesExist = false;
});

console.log('\n📄 检查 HTML 文件外部引用...');

// 检查 HTML 文件中的外部引用
const htmlFiles = [
    'web_portal/neural-index.html',
    'web_portal/index.html',
    'Pulsareon-Web/index.html'
];

const externalPatterns = [
    'https://cdn.jsdelivr.net',
    'https://fonts.googleapis.com',
    'https://api.countapi.xyz'
];

htmlFiles.forEach(file => {
    if (fs.existsSync(file)) {
        const content = fs.readFileSync(file, 'utf8');
        externalPatterns.forEach(pattern => {
            if (content.includes(pattern)) {
                console.log(`❌ ${file} 包含外部引用: ${pattern}`);
                allFilesExist = false;
            }
        });
    }
});

console.log('\n📊 性能分析:');

// 计算总文件大小
let totalSize = 0;
filesToCheck.forEach(file => {
    if (fs.existsSync(file)) {
        const stats = fs.statSync(file);
        totalSize += stats.size;
        console.log(`📦 ${file}: ${(stats.size / 1024).toFixed(2)} KB`);
    }
});

console.log(`\n📈 总资源大小: ${(totalSize / 1024).toFixed(2)} KB`);

// 估算加载时间 (假设 10Mbps 网络)
const estimatedLoadTime = (totalSize * 8) / (10 * 1024 * 1024) * 1000; // ms
console.log(`⏱️ 预估加载时间: ${estimatedLoadTime.toFixed(2)} ms`);

if (estimatedLoadTime < 500) {
    console.log('🎯 性能目标达成: 加载时间 < 500ms');
} else {
    console.log('⚠️ 性能目标未达成');
}

console.log('\n' + '='.repeat(50));
if (allFilesExist && estimatedLoadTime < 500) {
    console.log('✅ 所有外部资源已成功本地化！');
    console.log('✅ 预估加载性能在目标范围内！');
} else {
    console.log('❌ 本地化未完成或性能未达标');
}
console.log('='.repeat(50));