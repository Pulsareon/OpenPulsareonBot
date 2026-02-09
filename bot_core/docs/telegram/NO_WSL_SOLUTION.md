# OpenClaw Telegram 修复 - 无WSL方案

## 🚫 WSL 不可用

尝试其他方案：
1. ✅ 重启电脑（推荐）
2. ✅ 降级 Node.js 到 LTS 版本
3. ✅ 检查网络代理
4. ✅ 尝试直接使用 curl

---

## 方案 1: 重启电脑（当前最简单）

系统 DNS 已改为 Google DNS (8.8.8.8)
重启后再测试

---

## 方案 2: 降级 Node.js 到 v20 LTS

### 步骤 1: 安装 nvm-windows
下载: https://github.com/coreybutler/nvm-windows/releases

### 步骤 2: 安装 Node.js v20
```batch
nvm install 20.11.1
nvm use 20.11.1
```

### 步骤 3: 重新安装 OpenClaw
```batch
npm uninstall -g openclaw
npm install -g openclaw
```

---

## 方案 3: 检查网络代理

如果公司网络需要代理，需要配置：

### CMD 临时设置
```batch
set HTTP_PROXY=http://proxy-server:port
set HTTPS_PROXY=http://proxy-server:port
openclaw run
```

### 或配置 OpenClaw
在 `.openclaw/openclaw.json` 中：
```json
{
  "channels": {
    "telegram": {
      "proxy": {
        "host": "代理地址",
        "port": 端口
      }
    }
  }
}
```

---

## 当前状态

- ✅ DNS 已改到 Google (8.8.8.8)
- ✅ 配置 timeoutSeconds: 120
- ✅ hosts 文件已配置
- ❌ Node.js v24.13.0 无法连接

**最可能有效的是: 重启电脑 或 降级 Node.js**
