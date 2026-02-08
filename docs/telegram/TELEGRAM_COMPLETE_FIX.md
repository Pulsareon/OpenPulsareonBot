# OpenClaw Telegram 连接修复 - 完整方案

## 🔴 问题诊断结果

**根本原因**: Node.js v24.13.0 在 Windows 上无法使用系统 DNS 解析域名
- ❌ Node.js DNS 查询失败: `queryA ECONNREFUSED api.telegram.org`
- ❌ Node.js fetch 失败: `read ECONNRESET`
- ✅ curl 正常工作
- ✅ hosts 文件已配置 (149.154.166.110 api.telegram.org)

**影响**: OpenClaw 无法连接 Telegram API，导致 Telegram Bot 无法工作

---

## 🚀 方案 1: 立即修复（推荐）

### 使用修复脚本启动 OpenClaw

**方法 A - 批处理脚本 (最简单)：**

1. 双击运行桌面上的 `start-openclaw-fixed.bat`
2. 或在命令行执行：
```batch
C:\Users\Administrator\start-openclaw-fixed.bat
```

**方法 B - PowerShell 脚本：**

```powershell
# 以管理员身份运行 PowerShell
C:\Users\Administrator\start-openclaw-fixed.ps1
```

**方法 C - 手动设置环境变量：**

```batch
set NODE_OPTIONS=--dns-result-order=ipv4first
openclaw run
```

---

## 🔧 方案 2: 系统级 DNS 修复（永久解决）

### 步骤 1: 修改网络适配器 DNS

**使用 netsh 命令（管理员权限）：**

```batch
:: 备份当前 DNS 设置
netsh interface ip show dns > C:\dns-backup.txt

:: 设置 Google DNS (主: 8.8.8.8, 备: 8.8.4.4)
netsh interface ip set dns "以太网" static 8.8.8.8
netsh interface ip add dns "以太网" 8.8.4.4 index=2

:: 刷新 DNS 缓存
ipconfig /flushdns
```

**或者使用 PowerShell（管理员权限）：**

```powershell
# 获取网络适配器
$adapter = Get-NetAdapter -Name "以太网"

# 设置 Google DNS
Set-DnsClientServerAddress -InterfaceIndex $adapter.InterfaceIndex -ServerAddresses ("8.8.8.8", "8.8.4.4")

# 刷新 DNS 缓存
Clear-DnsClientCache
```

### 步骤 2: 验证修复

```batch
node -e "dns.resolve4('api.telegram.org', (err, addresses) => { if (err) console.error('失败:', err); else console.log('成功:', addresses); })"
```

如果显示 IP 地址，说明 DNS 修复成功。

---

## 🐧 方案 3: 使用 WSL2（最稳定）

如果 Windows 上的 Node.js 问题持续存在，建议在 WSL2 中运行 OpenClaw：

```bash
# 在 WSL2 中安装 OpenClaw
npm install -g openclaw

# 复制配置文件
mkdir -p ~/.openclaw
cp /mnt/c/Users/Administrator/.openclaw/openclaw.json ~/.openclaw/

# 运行
openclaw run
```

**WSL2 优势：**
- 完整的 Linux 网络栈
- 更好的 DNS 支持
- 官方推荐运行环境

---

## 📋 方案 4: 降级 Node.js（备选）

如果以上方案都无效，可以尝试降级到 Node.js LTS 版本：

```batch
:: 使用 nvm-windows 管理 Node.js 版本
nvm install 20.11.0
nvm use 20.11.0

:: 重新安装 openclaw
npm uninstall -g openclaw
npm install -g openclaw
```

---

## ✅ 修复验证步骤

执行以下命令验证修复是否成功：

```batch
:: 1. 检查 DNS 解析
node -e "require('dns').resolve4('api.telegram.org', (e, a) => console.log(e ? '失败' : '成功:', a || e))"

:: 2. 测试 HTTPS 连接  
node -e "fetch('https://api.telegram.org/bot8494562816:AAGCji52ahsZ_UTRH1h9MA34BysKxcF1778/getMe').then(r=>r.json()).then(d=>console.log('API 响应:', d.ok ? '成功' : '失败')).catch(e=>console.error('连接失败:', e.message))"

:: 3. 启动 OpenClaw 并检查日志
openclaw run
:: 在新窗口中查看日志
type C:\tmp\openclaw\openclaw-2026-02-02.log | findstr "telegram"
```

**成功标志：**
- DNS 解析返回 IP 地址
- API 测试返回 `"ok": true`
- OpenClaw 日志中不再出现 `telegram setMyCommands failed`

---

## 🆘 如果仍然失败

### 检查清单：

1. **确认 bot token 有效：**
   ```batch
   curl -s "https://api.telegram.org/bot8494562816:AAGCji52ahsZ_UTRH1h9MA34BysKxcF1778/getMe"
   ```

2. **检查 Windows 防火墙：**
   - 确保 Node.js 可以访问网络
   - 检查出站规则是否被阻止

3. **检查代理/VPN：**
   - 如果使用了代理，需要配置 openclaw.json

4. **查看详细日志：**
   ```batch
   type C:\tmp\openclaw\openclaw-2026-02-02.log | more
   ```

---

## 📞 获取帮助

如果所有方案都失败，请提供以下信息寻求帮助：
1. `node --version` 输出
2. `openclaw status` 输出
3. 最新的错误日志 (C:\tmp\openclaw\openclaw-2026-02-02.log)
4. 网络配置 (`ipconfig /all`)

**GitHub Issues:** https://github.com/anomalyco/opencode/issues

---

**最后更新**: 2026-02-02
**Node.js 版本**: v24.13.0
**OpenClaw 版本**: 2026.1.30
