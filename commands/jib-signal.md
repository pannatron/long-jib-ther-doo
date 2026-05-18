---
description: Read green/yellow/red signal zone from a conversation (long-jib-ther-doo)
---

The user wants to know what zone the conversation is in.

**Language:** Reply in the language of the chat data itself. If you need to ask the user a clarifying question and you haven't seen any of their messages yet, ask in *both* languages so non-English speakers can answer comfortably:

> "วางแชตที่อยากวิเคราะห์ หรือชี้ไฟล์ LINE export มาได้ครับ
> Paste the chat you want analyzed, or point me to a LINE export file."

**Figure out the input format from `$ARGUMENTS` and context:**

1. **LINE export file path** (e.g. `/path/to/[LINE]Chat.txt`) — use parse-line:
   ```bash
   ~/.claude/skills/long-jib-ther-doo/bin/parse-line --file "<path>" --your-name "<their LINE name>"
   ```
   Ask for `--your-name` if the user's LINE display name isn't "Me" or "เรา".

2. **Raw chat snippet pasted in** (lines like `Me: hi\nHer: hey`) — use parse-chat:
   ```bash
   echo "<chat>" | ~/.claude/skills/long-jib-ther-doo/bin/parse-chat
   ```

3. **User describes stats verbally** ("she replies in 30 min, I message twice as much...") — translate into bin/signal flags directly.

If unclear, ask one short clarifying question.

**Translate the JSON into a signal read:**

1. State the zone in 1 sentence — green / yellow / red — with the score
2. Walk through the **factors that mattered most** (top 2-3, not all 5)
3. Highlight any contradictions in the data — e.g. "she initiates often (good) but reply length is dropping (bad)" — the calculator gives a single score, but real situations often have mixed signals worth naming
4. Give a clear action level: lean in / hold steady / give space — pick one, don't hedge
5. Explain *why* in 1-2 sentences — the user should learn to read this themselves next time

**Calibration warning:**
The calculator was designed for *early-stage* texting. For long-established conversations (1000+ messages, already dating), some factors (like "questions back ratio") matter less. Apply judgment — don't read a "red" verdict on a chat that's clearly working as a stable relationship.

**Tone:**
Direct and specific. Avoid "it depends" — the user has data, give them a read.
