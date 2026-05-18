---
description: Get opener message templates by context (long-jib-ther-doo)
---

The user wants help opening a conversation with someone.

**Step 0 — confirm language (only if not obvious from `$ARGUMENTS`):**

If `$ARGUMENTS` includes a language hint or category id in a specific language, skip this. Otherwise ask in one line:

```
จะส่งข้อความเป็นภาษาอะไรครับ? (ไทย / English / Mix)
What language will the message be in? (Thai / English / Mix)
```

Use the chosen language for the rest of the interaction, including the customized templates.

**Step 1 — find the category:**

If `$ARGUMENTS` matches a known category id, jump to step 2. Otherwise list categories:

```bash
~/.claude/skills/long-jib-ther-doo/bin/opener --list
```

Show categories to the user in their language and ask which fits their situation. Examples:
- `class_workshop` — เจอกันในคลาส (โยคะ ภาษา ทำอาหาร)
- `mutual_friend` — เจอผ่านเพื่อน/งานเลี้ยง
- `dating_app` — Match จากแอป
- `gym_yoga_studio` — เจอที่ฟิตเนส (ระวังเรื่อง consent)

**Step 2 — get templates:**

```bash
~/.claude/skills/long-jib-ther-doo/bin/opener --category <id>
```

**Step 3 — customize, don't paste:**

Templates have `{context}` placeholders — the user must fill them with **a real detail** (something they actually noticed/discussed). Generic openers ("หวัดดี" / "hi") are a trap because they put all the work on the other person.

Ask the user:
- "What did you actually notice or talk about with them?"
- "Anything specific you can reference?"

Then rewrite each template using their real detail. Show 2-3 variants with different intents (low-pressure follow-up vs. direct invite vs. shared-curiosity question) — explain when each lands best.

**If a category has a warning (`warning_th` / `warning_en`):**
Show it. These exist for situations where the social context demands extra care (workplace boundaries, gym privacy norms).

**What NOT to do:**
- Don't hand over an opener verbatim with `{context}` still in it
- Don't suggest sending an unsolicited photo or pet-name greeting
- Don't pile on options — 2-3 is plenty; more becomes paralysis
