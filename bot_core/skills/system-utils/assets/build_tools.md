# OpenClaw Build Helpers (Windows)

这些工具是从 OpenClaw 官方源码构建过程中提取并适配的 Windows 兼容脚本。

## Bundle A2UI (Windows)
用于在 Windows 环境下构建 Canvas A2UI 组件。

```powershell
./scripts/bundle-a2ui.ps1
```

依赖：
- `compute-a2ui-hash.mjs` (同目录)
- Node.js 环境
- `pnpm`
