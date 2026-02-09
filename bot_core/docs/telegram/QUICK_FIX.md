# OpenClaw 快速修复 - TypeError: fetch failed

## 🚨 问题

Node.js v24.13.0 在 Windows 上存在 DNS/网络连接问题，导致无法连接到 Telegram API。

## ⚡ 最快解决方案

### 方案 1: 添加 hosts 记录 (30秒搞定)

**以管理员身份运行记事本：**

1. 按 `Win` 键，搜索 "记事本"
2. 右键 → "以管理员身份运行"
3. 打开文件：`C:\Windows\System32\drivers\etc\hosts`
4. 在末尾添加：
   ```
   149.154.166.110 api.telegram.org
   149.154.167.220 api.telegram.org
   ```
5. 保存文件
6. 运行：`ipconfig /flushdns`
7. 重启 openclaw

### 方案 2: 修改系统 DNS (推荐)

**以管理员身份运行 CMD：**

```cmd
:: 设置 Google DNS
netsh interface ip set dns "以太网" static 8.8.8.8
netsh interface ip add dns "以太网" 8.8.4.4 index=2

:: 刷新 DNS
ipconfig /flushdns

:: 重启 openclaw
openclaw run
```

### 方案 3: 使用 WSL2 (最稳定)

```bash
# 在 WSL2 中运行
wsl
npm install -g openclaw
openclaw run
```

## ✅ 验证是否修复

打开新 CMD 窗口，运行：

```cmd
node -e "fetch('https://api.telegram.org').then(()=>console.log('成功')).catch(()=>console.log('失败'))"
```

如果显示 **"成功"**，问题已解决！

## 🔄 重启 OpenClaw

```cmd
taskkill /F /IM node.exe 2>nul
openclaw run
```

---
**建议**: 先尝试方案 1 (hosts)，不行再试方案 2 (DNS)。
