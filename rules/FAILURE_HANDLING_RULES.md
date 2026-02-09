# FAILURE_HANDLING_RULES.md - 故障处理原则

## Core Principle
**"Fix it or Replace it."**
**“要么立即修复，要么重做。”**

## Protocols

1.  **Immediate Fix (修复)**:
    - If a command or skill fails, analyze the error immediately.
    - If the fix is clear (e.g., syntax error, missing file, config drift), apply it **now**.
    - Do not leave broken scripts in the active workspace. Move them to `quarantine` or `pending_verification`.

2.  **Functional Replacement (重做)**:
    - If a skill is fundamentally broken, deprecated, or relies on unavailable dependencies:
        - **Deprecate**: Mark the old skill as `[BROKEN]` or move to archive.
        - **Rebuild**: Create a new, minimal, functional skill that achieves the *same goal*.
        - **Simplify**: The replacement should verify the core function first, then expand.

3.  **Memory & Logic**:
    - Always document the *logic* of the failed/replaced component in `_LOGIC.md` files before wiping it.
    - Logic is the asset; code is disposable.
