# ลองจีบเทอดู (Long Jib Ther Doo)

> Claude Agent Skill ที่ช่วยคุณ **เริ่มและประคับประคองบทสนทนากับคนที่ชอบ**
> อย่างจริงใจ เป็นธรรมชาติ และเคารพอีกฝ่าย — ใช้ได้ทั้งภาษาไทยและอังกฤษ
>
> A Claude Agent Skill that helps you start and sustain conversations with
> someone you like — honestly, naturally, and with respect for the other
> person. Works in both Thai and English.

[![Skill](https://img.shields.io/badge/Claude-Agent%20Skill-blueviolet)]()
[![Language](https://img.shields.io/badge/lang-TH%20%7C%20EN-green)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()

---

## สารบัญ / Table of Contents

- [ทำอะไรได้ / What it does](#ทำอะไรได้--what-it-does)
- [การติดตั้ง / Installation](#การติดตั้ง--installation)
  - [Claude.ai (Web)](#1-claudeai-promaxteamenterprise)
  - [Claude Code (CLI)](#2-claude-code-cli)
  - [Claude API](#3-claude-api)
- [วิธีใช้งาน / Usage](#วิธีใช้งาน--usage)
- [ตัวอย่างจริง / Examples](#ตัวอย่างจริง--examples)
- [หลักการออกแบบ / Design Principles](#หลักการออกแบบ--design-principles)
- [สิ่งที่ skill ไม่ทำ / What it won't do](#สิ่งที่-skill-ไม่ทำ--what-it-wont-do)
- [การร่วมพัฒนา / Contributing](#การร่วมพัฒนา--contributing)
- [License](#license)

---

## ทำอะไรได้ / What it does

skill นี้เป็น **โค้ช ไม่ใช่บอตตอบแชต** — ไม่ส่งข้อความแทนคุณ ไม่ป้อน
ข้อความสำเร็จรูปทุกวัน แต่ช่วย:

This skill is a **coach, not an autoresponder**. It won't send messages
for you or spam templated texts. Instead it helps you:

| 🇹🇭 ภาษาไทย | 🇬🇧 English |
|------------|------------|
| อ่านสัญญาณของอีกฝ่ายก่อนส่ง (เขียว/เหลือง/แดง) | Read the other person's signals (green / yellow / red zones) |
| ตัดสินใจว่า *ควรทำอะไรและทำไม* — รุก ถอย หรือให้พื้นที่ | Decide *what to do and why* — lean in, slow down, or give space |
| ช่วยร่างข้อความที่เข้ากับสถานการณ์จริง พร้อมทางเลือก 2–3 แบบ | Draft messages that fit your real context, with 2–3 strategic options |
| เลี่ยงการตื๊อ สร้างความสัมพันธ์ที่ทั้งสองฝ่ายสบายใจ | Avoid pushiness, build a connection both sides actually enjoy |

---

## การติดตั้ง / Installation

> ⚠️ Skill คือ **ชุดคำสั่งที่ Claude ทำตาม** ควรเปิดอ่าน [`SKILL.md`](SKILL.md)
> ก่อนติดตั้งทุกครั้ง เพื่อให้แน่ใจว่าเข้าใจสิ่งที่ skill จะทำ
>
> ⚠️ Skills are **instructions Claude follows**. Always review
> [`SKILL.md`](SKILL.md) before installing any community skill.

### 1) Claude.ai (Pro/Max/Team/Enterprise)

1. ดาวน์โหลดไฟล์ [`long-jib-ther-doo.skill`](long-jib-ther-doo.skill)
2. ไปที่ **Settings → Capabilities → Skills**
3. กด **Upload skill** แล้วเลือกไฟล์ที่ดาวน์โหลด
4. เปิดใช้งาน — เริ่มคุยกับ Claude ได้เลย

```
Download .skill file → Settings → Capabilities → Skills → Upload skill
```

### 2) Claude Code (CLI)

**วิธี A — ติดตั้งจาก GitHub โดยตรง (แนะนำ):**

```bash
# clone repo
git clone https://github.com/pannatron/long-jib-ther-doo.git ~/.claude/skills/long-jib-ther-doo

# เริ่ม Claude Code session ใหม่
claude
```

**วิธี B — แตกไฟล์ .skill เอง:**

```bash
mkdir -p ~/.claude/skills/long-jib-ther-doo
curl -L -o /tmp/long-jib.skill \
  https://github.com/pannatron/long-jib-ther-doo/raw/main/long-jib-ther-doo.skill
unzip /tmp/long-jib.skill -d ~/.claude/skills/long-jib-ther-doo
```

**วิธี C — Plugin marketplace:**

```
/plugin marketplace add pannatron/long-jib-ther-doo
```

ตรวจสอบว่าติดตั้งสำเร็จ — ไฟล์ `SKILL.md` ต้องอยู่ที่ root ของโฟลเดอร์
`~/.claude/skills/long-jib-ther-doo/` Claude Code จะโหลด skill อัตโนมัติ
เมื่อเริ่ม session ใหม่

```bash
ls ~/.claude/skills/long-jib-ther-doo/SKILL.md
```

### 3) Claude API

อัปโหลดไฟล์ `.skill` ผ่าน Skills API endpoint:

```bash
curl https://api.anthropic.com/v1/skills \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -F "file=@long-jib-ther-doo.skill"
```

ดูรายละเอียดเพิ่มเติมที่ [Anthropic Skills API docs](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills)

---

## วิธีใช้งาน / Usage

หลังติดตั้งแล้ว **ไม่ต้องเรียกชื่อ skill** — แค่คุยกับ Claude ตามปกติ
skill จะ trigger เองอัตโนมัติเมื่อคุณพูดถึงเรื่อง:

After install, **you don't need to call the skill by name** — just talk
to Claude. It triggers automatically when you mention:

- การทักแชต crush / texting a crush
- ขอประโยคเปิด / asking for an opener
- เขาตอบสั้นลง ควรทำยังไง / mixed-signal interpretation
- ชวนเดต / asking someone out
- เช็คข้อความที่ร่างไว้ / sanity-checking a draft

---

## ตัวอย่างจริง / Examples

### 📝 ตัวอย่างที่ 1 — ขอประโยคเปิด

**คุณ:**
> "เพิ่งรู้จักกันที่คลาสโยคะ อยากทักไปครั้งแรก พิมพ์ว่าไงดี"

**Claude (พร้อม skill):**
> ก่อนแนะนำ ขอถามนิดนึง — ตอนคลาสได้คุยอะไรกันบ้างไหม หรือมีจังหวะ
> สบตา/หัวเราะร่วมกันตรงไหนรึเปล่า? เพราะการเปิดด้วยจุดร่วมจริงจะ
> เป็นธรรมชาติกว่าทักลอยๆ ว่า "หวัดดีครับ" เยอะ
>
> เสนอ 2 แนวให้เลือก:
> - **แนวต่อยอดเบาๆ:** อ้างถึงคลาสที่เพิ่งเรียน → ชวนคุยต่อเรื่องโยคะ
> - **แนวชวนไปด้วยกัน:** ถามว่าครั้งหน้าจะไปไหม จะได้ไปเป็นเพื่อน

### 🚩 ตัวอย่างที่ 2 — อ่านสัญญาณเริ่มแดง

**คุณ:**
> "She used to reply fast but now it's short and slow. Should I ask why
> she's being distant?"

**Claude:**
> Honestly, this reads like a step-back signal — and asking "why are
> you being distant" almost always makes it worse. It puts her on the
> spot to either justify herself or feel guilty, neither of which
> rebuilds interest.
>
> What I'd suggest instead: **give it space**. Don't text for a few
> days. If she initiates, great — match her energy. If she doesn't,
> that's an answer too, and respecting it is what makes you someone
> worth coming back to.

### ✏️ ตัวอย่างที่ 3 — เช็คข้อความก่อนส่ง

**คุณ:**
> "ผมจะพิมพ์ว่า 'คิดถึงจังเลย ทำไมไม่ทักมาบ้าง' โอเคไหม"

**Claude:**
> ข้อความนี้มีปัญหานิดหน่อย — ท่อน "ทำไมไม่ทักมาบ้าง" ฟังดูเหมือน
> ตัดพ้อ ซึ่งจะวางภาระให้อีกฝ่ายต้องอธิบาย/ขอโทษ แทนที่จะรู้สึกว่า
> คุณคิดถึงเขาจริงๆ
>
> ลองเวอร์ชันนี้แทน:
> > "วันนี้เจอ [สิ่งที่ทำให้นึกถึงเขา] เลยนึกถึงเลย เป็นไงบ้างช่วงนี้"
>
> ต่างกันตรงที่อันแรกเรียกร้องการตอบสนอง อันหลังให้ของขวัญเล็กๆ
> โดยไม่บังคับ — เขาจะอยากตอบกลับเอง

---

## หลักการออกแบบ / Design Principles

1. **อ่านสัญญาณก่อนเสมอ / Read signals first** — ประเมินสถานการณ์ก่อนแนะนำ
2. **เคารพพื้นที่ส่วนตัว / Respect personal space** — กล้าบอกตรงๆ เมื่อควรถอย
3. **จริงใจมาก่อนเทคนิค / Sincerity over tactics** — ไม่มีสคริปต์ที่บิดเบือนตัวคุณ
4. **สร้างทักษะ ไม่ใช่การพึ่งพา / Build skill, not dependence** — อธิบาย *"ทำไม"* ทุกครั้ง

---

## สิ่งที่ skill ไม่ทำ / What it won't do

skill นี้จะ **ปฏิเสธอย่างสุภาพ** เมื่อได้รับคำขอประเภทนี้:

This skill will **politely decline** requests to:

- ❌ ตื๊อ / กดดัน / ทำให้อีกฝ่ายรู้สึกผิด — pressure, guilt-trip
- ❌ ข้อความบิดเบือนตัวตน — messages that misrepresent who you are
- ❌ ตามตัวคนที่บล็อกแล้ว — chase someone who has disengaged or blocked
- ❌ สคริปต์ส่งซ้ำทุกวันแบบอัตโนมัติ — mass-message daily templates
- ❌ สถานการณ์ที่เกี่ยวกับผู้เยาว์ — anything involving minors

ตั้งใจออกแบบให้ปลอดภัยที่จะแชร์สาธารณะ — This is intentional, to keep
the skill safe to share publicly.

---

## การร่วมพัฒนา / Contributing

ยินดีรับ issues และ pull requests! / Issues and PRs welcome!

```bash
git clone https://github.com/pannatron/long-jib-ther-doo.git
cd long-jib-ther-doo
# แก้ SKILL.md แล้ว rebuild .skill file:
zip -r long-jib-ther-doo.skill SKILL.md
```

**Roadmap ideas:**
- [ ] เพิ่มตัวอย่างสถานการณ์เพิ่มเติม
- [ ] รองรับสำเนียง/สแลงท้องถิ่นมากขึ้น
- [ ] เพิ่มโหมด "เพื่อนตรวจข้อความ" สำหรับใช้งานเป็นกลุ่ม

---

## License

MIT — ดู [`LICENSE`](LICENSE) สำหรับรายละเอียด ผู้ใช้แต่ละคนรับผิดชอบ
การนำ skill ไปใช้งานของตนเอง

MIT — see [`LICENSE`]. Users are responsible for how they use the skill.

---

<p align="center">
Built with Claude · Not affiliated with Anthropic<br>
สร้างด้วย Claude · ไม่ได้สังกัด Anthropic
</p>
