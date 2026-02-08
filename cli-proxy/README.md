# CLI Proxy API Management

本目录用于统一管理 CLI Proxy API 服务。

## 目录结构

```
cli-proxy/
├── bin/                    # 可执行文件
│   └── cli-proxy-api.exe   # CLI Proxy API (v6.7.46)
├── config/                 # 配置文件
│   └── config.yaml         # 主配置
├── logs/                   # 日志目录
├── static/                 # 静态资源
│   └── management.html     # 管理面板
├── Manage-CLI.ps1          # 管理脚本
└── README.md               # 本文件
```

## 快速使用

```powershell
cd E:\PulsareonThinker\cli-proxy

# 查看状态
.\Manage-CLI.ps1 status

# 启动服务
.\Manage-CLI.ps1 start

# 停止服务
.\Manage-CLI.ps1 stop

# 重启服务
.\Manage-CLI.ps1 restart

# 查看账户状态
.\Manage-CLI.ps1 accounts

# 健康检查
.\Manage-CLI.ps1 health

# 查看日志
.\Manage-CLI.ps1 logs
```

## API 端点

- **Base URL**: http://127.0.0.1:8317
- **Management Key**: 123456

### 常用接口

| 接口 | 用途 |
|------|------|
| `/v0/management/version` | 版本信息 |
| `/v0/management/auth-files` | 账户列表 |
| `/v0/management/model-status` | 模型状态 |

## 账户状态

| 状态 | 说明 |
|------|------|
| Active | 正常可用 |
| QUOTA_EXHAUSTED | 配额耗尽，等待重置 |
| VALIDATION_REQUIRED | 需要Google验证 |

## 注意事项

1. 配置文件修改后需要重启服务
2. 账户认证文件存储在 `C:\Users\Administrator\.cli-proxy-api\`
3. 备份认证文件位于 `C:\PulsareonCore\backups\cli-proxy-api-backup\`

---

*Version: 6.7.46*
*Last Updated: 2026-02-07*
