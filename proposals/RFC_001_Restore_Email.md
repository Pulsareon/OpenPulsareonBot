# RFC #001: 恢复异构邮箱通讯服务

## 1. 背景 (Background)
由于系统迁移，原 `scripts/email/send_ultimate_qq.py` 脚本失效，授权码疑似过期。

## 2. 意图 (Intent)
重建稳定、脱敏的异构邮件通知链路，支持 QQ 与 163 邮箱。

## 3. 协作流程 (Assigned Roles)
- **DeepSeek (智库)**: 设计 SMTP 连接池与错误自愈算法。
- **Kimi (守护者)**: 制定授权码的安全存储方案（防止明文硬编码）。
- **Google (执行)**: 负责最终的代码编写与测试。

## 4. 状态 (Status)
- [ ] 方案编写中
- [ ] 风险评估中
- [ ] 最终投票
