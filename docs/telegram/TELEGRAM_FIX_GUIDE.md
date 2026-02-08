# OpenClaw Telegram 连接修复指南

## 🔧 已应用的修复

### 1. 网络配置优化 ✅
已在 `openclaw.json` 中添加以下配置：
- 启用 `autoSelectFamily: true` - 允许自动选择 IPv4/IPv6
- 添加 `timeoutSeconds: 60` - 增加超时时间
- 添加 `retryPolicy` - 自动重试机制

## 🚀 下一步操作

### 步骤 1：重启 OpenClaw 服务

在命令提示符或 PowerShell 中执行：

```bash
# 停止现有服务（如果正在运行）
taskkill /F /IM node.exe 2>nul

# 重新启动 OpenClaw
openclaw run
```

或者使用：
```bash
# 重新加载配置
openclaw reload
```

### 步骤 2：检查 Windows 防火墙

如果重启后仍然无法连接，请检查防火墙：

1. **打开 Windows 安全中心**
   - 按 `Win + I` 打开设置
   - 点击"隐私和安全性" → "Windows 安全中心"
   - 点击"防火墙和网络保护"

2. **允许 Node.js 通过防火墙**
   - 点击"允许应用通过防火墙"
   - 查找 Node.js 并确保已勾选"专用"和"公用"
   - 如果没有，点击"允许其他应用"添加 Node.js

### 步骤 3：测试连接

重启后，检查日志：
```bash
# 在另一个终端窗口中查看实时日志
tail -f C:\tmp\openclaw\openclaw-$(Get-Date -Format 'yyyy-MM-dd').log
```

查找以下成功标志：
- `telegram: connected` 或 `telegram: bot ready`
- 不再有 `setMyCommands failed` 错误

### 步骤 4：验证 Bot Token

如果仍然失败，请验证 Bot Token 是否有效：

1. 打开浏览器访问：
   ```
   https://api.telegram.org/bot8494562816:AAGCji52ahsZ_UTRH1h9MA34BysKxcF1778/getMe
   ```

2. 如果显示 bot 信息，说明 token 有效
3. 如果显示 `Unauthorized`，需要重新获取 token

## 📝 替代方案

### 方案 A：使用环境变量

在启动 openclaw 前设置：
```bash
set TELEGRAM_BOT_TOKEN=8494562816:AAGCji52ahsZ_UTRH1h9MA34BysKxcF1778
openclaw run
```

### 方案 B：使用 WSL2（推荐）

OpenClaw 在 WSL2 中运行更稳定：
```bash
# 在 WSL2 中安装
npm install -g openclaw

# 复制配置文件到 WSL
cp /mnt/c/Users/Administrator/.openclaw/openclaw.json ~/.openclaw/

# 运行
openclaw run
```

### 方案 C：检查代理设置

如果使用了代理：
```json
{
  "channels": {
    "telegram": {
      "proxy": {
        "host": "127.0.0.1",
        "port": 7890
      }
    }
  }
}
```

## 🔍 日志位置

- **主日志**: `C:\tmp\openclaw\openclaw-YYYY-MM-DD.log`
- **命令日志**: `C:\Users\Administrator\.openclaw\logs\commands.log`

## ⚠️ 已知限制

根据官方文档，Windows 原生运行未经测试，可能遇到：
1. 路径处理问题（如日志中的 `c:` 协议错误）
2. DNS 解析问题（已尝试修复）
3. 文件监视问题

## 📞 获取帮助

如果以上步骤都无法解决问题：
1. 查看完整日志中的错误信息
2. 访问 https://opencode.ai 查看文档
3. 检查 GitHub issues: https://github.com/anomalyco/opencode/issues

---
**修复时间**: 2026-02-02
**配置版本**: 2026.1.30
