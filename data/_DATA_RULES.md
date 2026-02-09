# 💾 Data Rules

> **⚠️ ATTENTION**: Any operation in this directory MUST comply with the rules defined below.

**用途**: 存放应用状态、数据库、配置文件和机密信息。
**规范**:
1. `secrets/`: 敏感信息（API Keys, Tokens）必须加密或限制访问。
2. `state/`: 运行时状态文件（JSON/YAML）。
3. 禁止存放临时文件。

---
*Updated: 2026-02-07*