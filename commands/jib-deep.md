---
description: Comprehensive 5-dimensional relationship deep-dive (long-jib-ther-doo)
---

Run a thorough, multi-dimensional read on the user's situation — not just signal scoring.

**Step 0 — confirm language first (don't skip this):**

Before asking *any* coaching questions, ask the user which language to use for the whole session. This matters because `/jib-deep` is a long back-and-forth — switching language mid-session is jarring.

If `$ARGUMENTS` includes a language hint (`th`, `ไทย`, `en`, `english`, `both`, `mix`), use it directly. Otherwise ask:

```
ก่อนเริ่ม — สะดวกคุยภาษาอะไรครับ?
Before we start — what language do you want to use?

1) ไทย — Thai only
2) English — English only
3) ผสม / Mix — สลับได้

(ตอบ 1/2/3 หรือพิมพ์ภาษาที่จะใช้)
```

Lock the chosen language for the rest of the session. Any sample drafts you write must also be in that language (or the language the user would actually send — ask if unclear).

**Step 1 — ask for the chat FIRST (before any context questions):**

Most of the context you need (channel, history length, who initiates, reply patterns, momentum) can be read directly from the chat. Don't interrogate the user for things the data will tell you.

Open with a single short prompt in the chosen language, e.g.:

```
มีแชทให้ดูไหมครับ? เลือกแบบที่สะดวก:
1) อัพโหลดไฟล์ LINE export (.txt) — อ่านได้ละเอียดสุด
2) ก็อปวางข้อความช่วงล่าสุดมาให้ดู (สัก 20-50 ข้อความก็พอ)
3) ไม่มีแชท / ไม่อยากแชร์ — เล่าปากเปล่าก็ได้
```

Wait for their answer. Don't ask context questions yet.

**Step 2 — collect & parse data:**

- LINE export file → run `parse-line` on the path
- Pasted snippet → run `parse-chat`
- Pending draft only → run `analyze` on it
- Verbal-only (option 3) → skip to Step 3 with what you have

After parsing, you should now know: message counts, who initiates, reply timing, length ratio, momentum trend. **Do not re-ask the user for any of these.**

**Step 3 — fill ONLY the gaps the chat can't show you:**

The chat won't tell you the offline reality or the user's internal state. Ask 1-2 questions at a time, max 3 total, and only the ones still unknown:

- **Offline context** — Have they met in person? How often? Any non-chat interaction (e.g. work, rides, mutual friends)?
- **Why now** — What triggered them to ask today? Specific incident, or a slow feeling?
- **Desired outcome** — Clarity? Closer? Define the relationship? Space? Move on?

If `$ARGUMENTS` or earlier conversation already answered any of these, skip it. Never re-ask what the user already volunteered.

**Step 4 — analyze across 5 dimensions:**

| # | Dimension | What to look at |
|---|---|---|
| 1 | **Investment balance** | Who sends more? Who asks more questions? Who initiates? |
| 2 | **Engagement quality** | Reply speed, message length ratio, depth of responses, callbacks to earlier topics |
| 3 | **Momentum direction** | Compared to a few weeks ago — improving, stable, or declining? |
| 4 | **Action signals** | Opportunities (their initiations, questions back, invitations) vs warning signs (short streaks, deflection, slow replies) |
| 5 | **Trajectory** | If nothing changes, where does this go? What action would actually shift it? |

For each dimension, give 1-2 sentences of read, not a wall of text.

**Step 5 — synthesize honestly:**

Don't just dump tool output. Look across dimensions and call out:
- **Contradictions** — e.g. "she initiates often but reply quality is declining" matters more than either signal alone
- **The real bottleneck** — is it her interest, the user's strategy, lack of escalation, or external context?
- **Calibration** — if the calculator says "red" but the conversation has 3000+ messages and dates, name that the calculator is mis-calibrated for established relationships

**Step 6 — one specific action:**

End with ONE specific thing the user can do in the next 24-72 hours. Not three options — one. Picked because it addresses the actual bottleneck identified in step 5.

Include:
- *What* exactly (concrete enough to do tomorrow)
- *Why* this and not something else
- *What signal to watch for* afterward — how the user will know it landed

**Step 7 — offer a printable action-plan PDF (opt-in):**

After delivering steps 5 + 6 in chat, ask the user once (in the session language) whether they want a structured PDF version they can keep:

```
อยากได้ action plan แบบ PDF ที่ print เก็บไว้ดูได้ปะ?
(สรุปทั้งหมดนี้เป็นคู่มือเดียวที่อ่านทบทวนได้)
```

(In English: `Want a printable PDF of this action plan to keep?`)

If they say yes:
1. Build a JSON object matching the schema in `templates/action-plan-example.json`. Mirror **everything you just said** in chat — same dimensions, same one specific action, same scenarios. Don't invent new content. Translate the analysis structure into the fields. Use the session language for all visible text (`labels`, headings, body).
2. Save it as `plans/<slug>.json` (create the `plans/` directory if needed). Pick a slug the user will recognize — initials, a placeholder, or the date are all fine.
3. Run the generator:
   ```bash
   ./bin/gen-plan plans/<slug>.json --out-dir plans --open
   ```
   This produces `plans/action-plan-<slug>.html` + `.pdf` and opens the PDF.
4. If Chrome isn't available, the script prints a warning and skips PDF — tell the user the HTML version is still ready (`open plans/action-plan-<slug>.html`).

If the user declines, just stop. The chat summary is the deliverable.

**Tone:**
Direct. Honest. The user came here because their gut isn't enough — they need a clearer read than "it depends." If the data shows they're chasing, say so. If the data shows mutual interest they're underestimating, say that. Sugarcoating wastes everyone's time.

**What NOT to do:**
- Don't give 5 action options — pick one
- Don't refuse to interpret because "every relationship is different" — interpret with the data you have, name your confidence level
- Don't recommend pressuring, guilt-tripping, surveillance, or chasing someone who's clearly disengaged
