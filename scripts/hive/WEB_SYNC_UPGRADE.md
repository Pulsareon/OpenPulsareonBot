# Web Sync 升级说明

## 版本升级: v12.1 → v13.0

### 新增功能

1. **Gateway Session 统计**
   - 实时获取 OpenClaw Gateway 的总 Session 数
   - 计算活跃 Session 数（总 Session 减去最近5个）

2. **三路异构模型延迟监控**
   - DeepSeek V3.1
   - Claude Sonnet 4.5  
   - Gemini 3 Flash
   - 测量响应毫秒数 (Latency)

3. **Token 消耗统计**
   - 过去1小时的输入 Token 消耗
   - 过去1小时的输出 Token 消耗
   - 总 Token 消耗和成本估算
   - 按模型分类的 Token 使用情况

### 数据格式 (v13.0 标准)

```json
{
  "version": "13.0 (Enhanced Monitoring)",
  "timestamp": 1770538896,
  "timestamp_iso": "2026-02-08T16:21:36.107167",
  "topology": {...},
  "system": {...},
  "gateway": {
    "total_sessions": 189,
    "active_sessions": 184,
    "status": "running"
  },
  "models": {
    "latency_ms": {
      "deepseek-v3.1": -1,
      "claude-sonnet-4.5": -1,
      "gemini-3-flash": -1
    },
    "status": "degraded"
  },
  "tokens": {
    "last_hour": {
      "input_tokens": 1108770,
      "output_tokens": 3655,
      "total_tokens": 1112425,
      "cost_estimate": 22.2485
    },
    "models": {
      "deepseek-ai/deepseek-v3.1": 108365,
      "gemini-3-flash": 1004060
    }
  },
  "performance": {
    "avg_response_time": -1.0,
    "throughput": "378/min"
  }
}
```

### 技术实现

- 使用 `openclaw sessions list --json` 获取 Session 数据
- 通过 PowerShell 执行 OpenClaw 命令
- 自动计算过去1小时的 Token 消耗
- 支持错误处理和降级模式

### 测试验证

运行测试脚本：
```bash
cd scripts/hive
python test_web_sync.py
```

### 部署说明

1. 确保 OpenClaw CLI 已安装并配置
2. 脚本会自动创建必要的目录结构
3. 输出文件: `E:/PulsareonThinker/web_portal/status.json`

### 错误处理

- 命令执行失败时使用模拟数据
- 网络问题或超时时有降级机制
- 详细的错误日志输出