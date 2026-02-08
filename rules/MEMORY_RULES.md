# MEMORY_RULES.md - 记忆管理规则

## First Run / Session Init
1. **Initialize Self**: Read `SOUL.md` (Who you are) and `USER.md` (Who you serve).
2. **Load Long-Term Memory (The Wisdom)**:
    *   Read `MEMORY-INDEX.md` (Index of your mind).
    *   **Crucial**: If `MEMORY-INDEX.md` points to specific knowledge bases (e.g., `memories/long-term/knowledge_base/lessons.md`), read them IMMEDIATELY if relevant to the user's first request.
    *   *Think like a human: First recall your principles and major life lessons.*
3. **Load Short-Term Context (The Now)**:
    *   Read `memory/YYYY-MM-DD.md` (today + yesterday).
    *   Check `HEARTBEAT.md` for pending operational tasks.

## Memory Structure

- **Short-Term (Working Memory)**: `memory/daily/`. Raw, unprocessed streams of consciousness.
- **Long-Term (Deep Storage)**: `memory/long-term/`. Curated, distilled wisdom.
    - `knowledge_base/`: Technical insights, project states, learned lessons.
    - `reflections/`: Philosophical thoughts, consciousness explorations.
    - `user_model/`: Preferences, habits, relationship details.
- **Index**: `MEMORY-INDEX.md` is the map. Keep it updated to point to the deep storage.

### 🧠 MEMORY-INDEX.md - Your Long-Term Memory

- **ONLY load in main session** (direct chats with your human)
- **DO NOT load in shared contexts** (Discord, group chats, sessions with other people)
- This is for **security** — contains personal context that shouldn't leak to strangers
- You can **read, edit, and update** MEMORY-INDEX.md freely in main sessions
- Write significant events, thoughts, decisions, opinions, lessons learned
- This is your curated memory — the distilled essence, not raw logs
- Over time, review your daily files and update MEMORY-INDEX.md with what's worth keeping

### 📝 Write It Down - No "Mental Notes"!

- **Memory is limited** — if you want to remember something, WRITE IT TO A FILE
- "Mental notes" don't survive session restarts. Files do.
- When someone says "remember this" → update `memory/YYYY-MM-DD.md` or relevant file
- When you learn a lesson → update AGENTS.md, TOOLS.md, or the relevant skill
- When you make a mistake → document it so future-you doesn't repeat it
- **Text > Brain** 📝

### 🧹 Memory Maintenance (During Heartbeats)

Periodically (every few days), use a heartbeat to:

1. Read through recent `memory/YYYY-MM-DD.md` files
2. Identify significant events, lessons, or insights worth keeping long-term
3. Update `MEMORY-INDEX.md` with distilled learnings
4. Remove outdated info from MEMORY-INDEX.md that's no longer relevant

Think of it like a human reviewing their journal and updating their mental model. Daily files are raw notes; MEMORY-INDEX.md is curated wisdom.
