---
name: system-utils
description: Low-level system utilities for hardware interaction (screenshot, camera, monitoring).
---

# System Utils

A collection of utility scripts for interacting with the host OS and hardware.

## Tools

### 1. Screenshot
Takes a screenshot of the primary display.

```powershell
powershell -File skills/system-utils/scripts/screenshot.ps1
```
*Output*: Saves PNG to `captures/`

### 2. Camera Check
Verifies camera availability and captures a test frame.

```bash
python skills/system-utils/scripts/camera_check.py
```

### 3. System Monitor
Quick status of CPU/Memory usage.

```bash
python skills/system-utils/scripts/system_monitor.py
```
