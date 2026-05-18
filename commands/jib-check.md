---
description: Analyze a draft message for pushiness before sending (long-jib-ther-doo)
---

The user wants to sanity-check a draft message before sending it.

**Get the draft:**
- If `$ARGUMENTS` contains the draft text, use it directly.
- If empty, ask the user briefly: "ส่งข้อความที่จะร่างมาได้เลย" / "What's the draft?"

**Run the analyzer:**
```bash
~/.claude/skills/long-jib-ther-doo/bin/analyze "<the draft>"
```

**Translate the JSON output into natural coaching:**

1. State the verdict in plain language — green (ส่งได้), yellow (ปรับนิดหน่อย), red (อย่าส่งแบบนี้)
2. For each flag, explain in 1 sentence: what pattern it caught + why it backfires (use the `explanation` field, not the rule ID)
3. If yellow or red, **rewrite the draft** in a version that conveys the same intent without the flagged patterns
4. Show the rewritten version + 1 short explanation of the change

**Tone rules:**
- Reply in the language the user used (Thai → Thai, English → English, mixed → mixed)
- Be direct, not preachy. The user already knows their draft might be off — they want to know *why* and *what to send instead*
- If verdict is green, say so quickly and move on. Don't pad praise.

**What NOT to do:**
- Don't dump the raw JSON
- Don't lecture about communication theory
- Don't refuse a borderline-yellow draft outright — explain the trade-off and let the user decide
