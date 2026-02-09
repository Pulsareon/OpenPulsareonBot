# API 工具集使用指南

## 📦 工具概览

| 工具 | 用途 | 复杂度 |
|------|------|--------|
| `web-request-template.ps1` | 基础 HTTP 请求模板 | ⭐ |
| `api-logger.ps1` | API 调用日志记录 | ⭐⭐ |
| `enhanced-web-request.ps1` | 完整集成方案（推荐）| ⭐⭐⭐ |
| `api-configs.json` | API 配置管理 | ⭐ |

---

## 🚀 快速开始

### 方式一：使用增强版（推荐）

```powershell
# 访问 Moltbook Feed
.\enhanced-web-request.ps1 `
  -ServiceName "moltbook" `
  -Endpoint "/api/v1/feed" `
  -DetailedOutput

# 访问特定 API（需在 api-configs.json 中配置）
.\enhanced-web-request.ps1 `
  -ServiceName "example" `
  -Endpoint "/users" `
  -Method "POST" `
  -Body '{ "name": "test" }' `
  -DetailedOutput
```

### 方式二：使用基础模板

```powershell
# 复制模板文件
cp .\web-request-template.ps1 .\myapi-request.ps1

# 编辑文件，修改配置
# $baseUrl = "https://api.example.com"
# $apiKey = "your-api-key"

# 运行
.\myapi-request.ps1 -Endpoint "/users" -DetailedOutput
```

### 方式三：手动记录日志

```powershell
# 导入日志模块
. .\api-logger.ps1

# 查看统计信息
Show-ApiStats

# 查询错误日志
Get-ApiLogs -ErrorsOnly

# 查询特定服务
Get-ApiLogs -Service "moltbook"

# 清理旧日志（保留7天）
Clear-ApiLogs -KeepDays 7
```

---

## ⚙️ 配置 API 服务

编辑 `api-configs.json` 添加新服务：

```json
{
  "services": {
    "myservice": {
      "baseUrl": "https://api.myservice.com",
      "apiKey": "your-api-key",
      "proxy": "http://127.0.0.1:7897",
      "timeout": 30,
      "notes": "My custom API service"
    }
  }
}
```

---

## 📊 日志格式

每条日志记录包含：

```json
{
  "timestamp": "2026-02-03T11:19:55.789Z",
  "service": "moltbook",
  "endpoint": "/api/v1/feed",
  "method": "GET",
  "metadata": {
    "status": "success",
    "statusCode": 200,
    "duration": 1234,
    "attempt": 1
  }
}
```

---

## 🔍 调试技巧

1. **启用详细输出**
   ```powershell
   -DetailedOutput
   ```

2. **禁用日志记录**（测试时用）
   ```powershell
   -DisableLogging
   ```

3. **查看实时日志**
   ```powershell
   Get-Content .\api-logs.jsonl -Wait -Tail 5
   ```

4. **分析错误模式**
   ```powershell
   Get-ApiLogs -Service "moltbook" -ErrorsOnly |
     Select-Object timestamp, endpoint, metadata.errorMsg
   ```

---

## 💡 最佳实践

### ✅ DO
- 使用 `-ServiceName` 参数指定服务
- 配置合理的超时时间（15-30秒）
- 定期清理旧日志（`Clear-ApiLogs`）
- 代理配置确保正确格式（`http://127.0.0.1:7897`）
- 使用 `api-configs.json` 集中管理多个 API

### ❌ DON'T
- 不要在生产环境使用 `-DisableLogging`
- 不要直接修改 `web-request-template.ps1`（复制后再改）
- 不要在日志文件中存储敏感信息（已经排除 apiKey）
- 不要忽略 4xx 错误（客户端错误不会重试）
- 不要硬编码 API key（使用配置文件）

---

## 🔧 故障排除

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| "基础连接已关闭" | 代理配置错误 | 检查 proxyUrl 格式 |
| 401 未经授权 | API key 无效 | 检查配置中的 apiKey |
| 超时 | 网络慢或服务响应慢 | 增加超时时间 |
| 语法错误 | PowerShell 版本兼容 | 确保 PowerShell 5.1+ |
| 路径错误 | 脚本路径包含中文 | 使用英文路径 |

---

## 📚 扩展建议

### 想添加新功能？

1. **自动重试策略**：在 `enhanced-web-request.ps1` 中修改指数退避逻辑
2. **缓存支持**：为 GET 请求添加本地缓存机制
3. **速率限制**：记录调用频率，避免超限
4. **批量请求**：支持并行发送多个请求

### 想学习更多？

- PowerShell HTTP 请求：`[System.Net.HttpWebRequest]`
- JSON 处理：`ConvertFrom-Json / ConvertTo-Json`
- 异步操作：`Start-Job / Invoke-Parallel`

---

*最后更新: 2026-02-03*
