# ลองจีบเทอดู (Long Jib Ther Doo)

> Claude Agent Skill ที่ช่วยคุณ **เริ่มและประคับประคองบทสนทนากับคนที่ชอบ**
> อย่างจริงใจ เป็นธรรมชาติ และเคารพอีกฝ่าย — ใช้ได้ทั้งภาษาไทยและอังกฤษ
>
> A Claude Agent Skill that helps you start and sustain conversations with
> someone you like — honestly, naturally, and with respect for the other
> person. Works in both Thai and English.

[![Skill](https://img.shields.io/badge/Claude-Agent%20Skill-blueviolet)]()
[![Language](https://img.shields.io/badge/lang-TH%20%7C%20EN-green)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)]()
[![Tests](https://github.com/pannatron/long-jib-ther-doo/actions/workflows/test.yml/badge.svg)](https://github.com/pannatron/long-jib-ther-doo/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-MIT-blue)]()

---

## สารบัญ / Table of Contents

- [ทำอะไรได้ / What it does](#ทำอะไรได้--what-it-does)
- [Architecture (skill + software)](#architecture-skill--software)
- [CLI tools](#cli-tools)
- [ฟีเจอร์ Jib / Jib Features](#ฟีเจอร์-jib--jib-features)
  - [`/jib-opener` — เริ่มต้นบทสนทนา](#-jib-opener--เริ่มต้นบทสนทนา--start-the-conversation)
  - [`/jib-check` — เช็คข้อความก่อนส่ง](#-jib-check-draft--เช็คข้อความก่อนส่ง--sanity-check-before-sending)
  - [`/jib-signal` — อ่านสัญญาณตอนนี้](#-jib-signal--อ่านสัญญาณตอนนี้--read-the-current-zone)
  - [`/jib-deep` — วิเคราะห์ลึก 5 มิติ](#-jib-deep--วิเคราะห์ลึก-5-มิติ--deep-dive-5-dimensions)
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

## Architecture (skill + software)

ต่างจาก skill ทั่วไปที่เป็น markdown ล้วน — `long-jib-ther-doo` แพ็ค
**ซอฟต์แวร์ Python จริงๆ** ไว้ใน skill เพื่อให้ส่วนที่ **"วัดได้"**
เป็น objective ไม่ต้องพึ่ง intuition ของ Claude อย่างเดียว

```
long-jib-ther-doo/
├── SKILL.md              ← บอก Claude ว่าเมื่อไหร่ควรเรียก tool ไหน
├── bin/                  ← CLI tools (executable Python scripts)
│   ├── analyze           วิเคราะห์ pushiness ของข้อความ
│   ├── signal            คำนวณ green/yellow/red zone
│   ├── parse-chat        parse แชตที่ paste มาแบบสั้นๆ → ออกมาเป็น stats
│   ├── parse-line        parse ไฟล์ export จาก LINE (.txt)
│   └── opener            เทมเพลตประโยคเปิดตาม category
├── src/                  ← logic modules
│   ├── analyzer.py       pushiness scoring จาก rule patterns
│   ├── signals.py        weighted scoring สำหรับ signal zone
│   ├── parser.py         parse chat formats (Me:/Her:/เรา:/เขา:)
│   ├── line_parser.py    parse LINE export format with timestamps
│   └── openers.py        opener library lookup
├── data/                 ← rule library (JSON — แก้ได้ ไม่ต้องแตะโค้ด)
│   ├── rules.json        patterns ของ pushy/guilt-trip phrases
│   └── openers.json      opener templates จัดตามบริบทการพบกัน
└── tests/                ← 23 unit tests (run: python -m unittest discover tests)
```

**ทำไมต้องเป็นซอฟต์แวร์ ไม่ใช่ markdown อย่างเดียว?**

| สิ่งที่ Claude ทำได้ดี | สิ่งที่โค้ดทำได้ดีกว่า |
|---|---|
| ตีความสถานการณ์ที่ซับซ้อน | ให้คะแนน objective ที่ทำซ้ำได้ |
| ปรับโทนตามบุคลิกผู้ใช้ | detect pattern เฉพาะที่ตรวจซ้ำๆ |
| แนะนำเชิงกลยุทธ์ | นับ stats จาก raw chat |
| อธิบาย "ทำไม" ให้ผู้ใช้เข้าใจ | unit test ได้ — รู้ว่าผลตรงเดิม |

ผลคือ Claude ใช้ tools เป็น "เครื่องมือเสริมความเห็น" — เหมือนหมอใช้
blood test ก่อนวินิจฉัย ไม่ใช่ทดแทนการคุยกับคนไข้

---

## CLI tools

ทดสอบจากเครื่องตัวเองได้เลย ไม่ต้องผ่าน Claude:

```bash
# 1) วิเคราะห์ข้อความก่อนส่ง
./bin/analyze "ทำไมไม่ทักมาบ้าง"
# → { "pushiness": 0.9, "verdict": "red", "flags": [{"category": "guilt_trip", ...}] }

# 2) คำนวณ signal zone จากข้อมูลแชต
./bin/signal --your-msgs 10 --their-msgs 8 \
  --your-avg-len 80 --their-avg-len 25 \
  --your-questions 4 --their-questions 1 \
  --reply-minutes 240 --initiations 0 --short-streak 3
# → { "zone": "yellow", "score": 0.42, "factors": {...}, "recommendation": "..." }

# 3) parse แชตที่ paste มาแบบสั้นๆ → ออกมาเป็น signal report
echo "Me: hi
Her: hey
Me: how was your day?
Her: ok" | ./bin/parse-chat

# 4) parse ไฟล์ export จริงจาก LINE (มี timestamp → reply time แม่นกว่า)
./bin/parse-line --file ~/Downloads/[LINE]Chat-with-Nong.txt
# ถ้าใน LINE ใช้ชื่อจริงไม่ใช่ "Me":
./bin/parse-line --file chat.txt --your-name "Songkarn"

# 5) ดูเทมเพลตประโยคเปิดตามบริบทที่พบกัน
./bin/opener --list
./bin/opener --category class_workshop
```

**วิธี export แชตจาก LINE:** เปิดแชต → กดที่ชื่อหัวแชต → ⚙️ ตั้งค่า → "ส่งประวัติแชต" → "Text only" → แชร์ไปที่ email/Files

ทั้งหมดเขียนด้วย **Python 3.10+ stdlib เท่านั้น** — ไม่ต้อง `pip install`
อะไร รันได้ทุกเครื่องที่มี Python

---

## ฟีเจอร์ Jib / Jib Features

ฟีเจอร์หลักของ skill นี้คือชุด **`/jib-*` slash commands** — เรียกตรงใน
Claude Code session ได้เลย แต่ละตัวออกแบบมาให้ตอบคำถามคนละแบบในเส้นทาง
"จีบ" ตั้งแต่ทักครั้งแรกจนถึงการอ่านสัญญาณระยะยาว

Each `/jib-*` command answers a different question on the "jib" journey,
from first message to long-term signal reading:

```
ทักครั้งแรก          ก่อนส่งทุกข้อความ      อยากรู้ว่าตอนนี้อยู่จุดไหน    อยากเข้าใจภาพรวม
   ↓                       ↓                         ↓                       ↓
/jib-opener   →    /jib-check        →      /jib-signal       →       /jib-deep
```

---

### 🎬 `/jib-opener` — เริ่มต้นบทสนทนา / Start the conversation

**ใช้เมื่อ:** เพิ่งรู้จักกัน / แลก contact มาแล้วยังไม่ได้ทักครั้งแรก /
ไม่รู้จะเปิดประโยคยังไงให้ไม่ดู generic

**ทำอะไร:**
- ถามว่าเจอกันบริบทไหน (คลาส, เพื่อนร่วมงาน, dating app, ฯลฯ)
- ดึง template เปิดบทสนทนาจาก `data/openers.json` ตามบริบทนั้น
- **ไม่ยอมให้ copy ไปใช้ตรงๆ** — บังคับให้คุณกรอก "รายละเอียดจริง" ที่
  สังเกตเห็น/คุยกันมาก่อน เพราะ opener ที่ generic ("หวัดดีครับ") จะ
  ผลักภาระให้อีกฝ่ายเริ่มเรื่องเอง
- โชว์ 2-3 แนวที่ intent ต่างกัน (เกริ่นเบาๆ vs ชวนไปด้วยกัน vs ถามต่อยอด)

**ตัวอย่าง output:**
```
> /jib-opener
→ เจอกันบริบทไหนครับ? (class_workshop / mutual_friend / dating_app / ...)
> เจอที่คลาสโยคะ
→ ตอนคลาสได้คุยอะไรกันบ้าง หรือมีจังหวะอะไรร่วมกันรึเปล่า?
> เห็นเขาช่วยเอาบล็อกโยคะมาให้ตอนผมหายืม
→ แนะนำ 3 เวอร์ชัน:
   1) ต่อยอดจากเหตุการณ์: "ขอบคุณเรื่องบล็อกอีกรอบนะ..."
   2) ชวนไปด้วยกัน: "ครั้งหน้าจะไปไหม จะได้ไปเป็นเพื่อน"
   3) ถามแบบเปิด: "ปกติเรียนกี่คลาสต่อสัปดาห์เลย"
```

---

### ✏️ `/jib-check "draft"` — เช็คข้อความก่อนส่ง / Sanity-check before sending

**ใช้เมื่อ:** ร่างข้อความไว้แล้วแต่ไม่แน่ใจว่า "เกินไป" ไหม / กลัวฟังดู
ตื๊อ ตัดพ้อ หรือ guilt-trip โดยไม่ตั้งใจ

**ทำอะไร:**
- รัน `bin/analyze` ผ่าน rule patterns ใน `data/rules.json`
- ให้คะแนน **pushiness 0.0–1.0** + verdict (🟢 green / 🟡 yellow / 🔴 red)
- ระบุ pattern ที่ตรวจเจอ เช่น `guilt_trip`, `repeated_ask`, `monitoring`
- **ถ้า yellow/red จะเขียนเวอร์ชันใหม่ให้** — เก็บเจตนาเดิมไว้ แต่ตัด
  ส่วนที่บีบให้อีกฝ่ายต้องอธิบาย/รู้สึกผิด

**ตัวอย่าง output:**
```
> /jib-check "ทำไมไม่ทักมาบ้าง คิดถึงนะ"
→ 🔴 red zone (pushiness 0.85)
   เจอ guilt-trip pattern — "ทำไมไม่..." วางภาระให้เขาต้องอธิบาย/ขอโทษ
   แทนที่จะรู้สึกถูกคิดถึง
→ เวอร์ชันใหม่:
   "วันนี้เจอ [สิ่งที่ทำให้นึกถึงเขา] เลยนึกถึงเลย เป็นไงบ้างช่วงนี้"
   ต่างตรง: ให้ของขวัญเล็กๆ โดยไม่บังคับให้เขาตอบ
```

---

### 🚦 `/jib-signal` — อ่านสัญญาณตอนนี้ / Read the current zone

**ใช้เมื่อ:** คุยกันมาสักพักแล้ว / สงสัยว่าอีกฝ่ายยังสนใจอยู่ไหม /
อยากได้ภาพรวมแบบ objective ก่อนตัดสินใจ "จะรุก/ถอย/ให้พื้นที่"

**ทำอะไร:**
- รับ input ได้ 3 แบบ:
  1. **ไฟล์ LINE export** (`.txt`) → รัน `bin/parse-line` (มี timestamp =
     คำนวณ reply time แม่น)
  2. **Paste แชตสั้นๆ** (`Me: ... / Her: ...`) → รัน `bin/parse-chat`
  3. **บอกด้วยปาก** ("เขาตอบช้า 4 ชม. ผมส่งเยอะกว่า 2 เท่า") → แปลง
     เป็น flag ส่งเข้า `bin/signal`
- คำนวณ **signal zone (🟢🟡🔴)** จาก 5 ปัจจัยที่ถ่วงน้ำหนัก: message
  ratio, reply time, length ratio, questions back, initiation balance
- **ระบุ contradictions** — ถ้าตัวเลขขัดกัน (เช่น "เขาเริ่มทักบ่อย แต่
  ความยาวข้อความลดลง") จะ flag ให้ ไม่ดูแค่ score
- เตือน calibration: ถ้าเป็นความสัมพันธ์ที่ established แล้ว
  (1000+ ข้อความ, ออกเดทแล้ว) จะบอกว่าเครื่องคิดเลขนี้ไม่ได้ออกแบบมา
  สำหรับเคสนั้น

**ตัวอย่าง output:**
```
> /jib-signal
→ paste แชต / ชี้ไฟล์ LINE export มาได้เลย
> [user แปะ LINE export]
→ 🟡 yellow zone (score 0.42)
   ปัจจัยที่สำคัญที่สุด 3 อย่าง:
   • reply time ของเขาช้าลงจาก 15 นาที → 4 ชั่วโมง (น้ำหนักลบ)
   • คุณส่งยาวเฉลี่ย 80 ตัวอักษร เขาส่ง 25 (ratio 3.2 — มากไป)
   • แต่เขายังถามกลับเฉลี่ย 1 คำถาม/วัน (น้ำหนักบวก เล็กน้อย)
→ action: hold steady — ลดความถี่ลง ปล่อยให้เขาเป็นคนเริ่มทัก 1 ครั้ง
   เพื่อ recalibrate ว่าฝ่ายไหนกำลัง "ลงทุน" มากกว่ากัน
```

---

### 🔬 `/jib-deep` — วิเคราะห์ลึก 5 มิติ / Deep-dive (5 dimensions)

**ใช้เมื่อ:** กังวลกับสถานการณ์ใดสถานการณ์หนึ่งจริงจัง / `/jib-signal`
ให้ภาพไม่พอ / อยากได้ "1 action ที่ควรทำใน 72 ชม." ไม่ใช่ "ลองดูหลายๆ ทาง"

**ทำอะไร:**
- เริ่มด้วยการ **ล็อคภาษา** ก่อน (ไทย/English/Mix) เพราะเซสชันยาว
- ถามบริบท: คุยกันมานานแค่ไหน, สถานะตอนนี้, ทำไมถึงถามตอนนี้, อยากได้
  outcome แบบไหน
- รัน `parse-line` / `parse-chat` / `analyze` ตามข้อมูลที่มี
- วิเคราะห์ครบ **5 มิติ**:

  | # | มิติ | มองอะไร |
  |---|---|---|
  | 1 | **Investment balance** | ใครส่งมากกว่า ใครถามมากกว่า ใครเริ่มทัก |
  | 2 | **Engagement quality** | reply speed, ความยาว, ความลึก, จำเรื่องเก่าได้ไหม |
  | 3 | **Momentum direction** | เทียบกับ 2-3 สัปดาห์ก่อน — ดีขึ้น/นิ่ง/แย่ลง |
  | 4 | **Action signals** | โอกาส (เขาเริ่ม, ถามกลับ, ชวน) vs สัญญาณเตือน (short streak, deflect) |
  | 5 | **Trajectory** | ถ้าไม่เปลี่ยนอะไร เรื่องนี้จะไปทางไหน |

- **Synthesize อย่างซื่อสัตย์** — ชี้ contradictions, ระบุ "bottleneck
  จริง" (ความสนใจของเขา? กลยุทธ์ของคุณ? ไม่ escalate? บริบทภายนอก?)
- จบด้วย **1 action เดียว** ที่ specific พอจะลงมือทำได้พรุ่งนี้ + อธิบาย
  ว่าทำไมเลือกอันนี้ + บอกว่าจะดูสัญญาณอะไรหลังทำ

**ต่างจาก `/jib-signal` ตรงไหน:**
- `/jib-signal` = อ่าน metric ปัจจุบัน (snapshot)
- `/jib-deep` = อ่าน metric + บริบทเชิงคุณภาพ + เทรนด์ + คำตอบเชิงกลยุทธ์
  ที่เฉพาะกับสถานการณ์คุณ

---

### ทำไมต้องเป็น slash command ไม่ใช่คุยเปล่าๆ?

Slash commands **บังคับ flow** ให้ตรงจุด — `/jib-deep` จะถามครบทุกมิติ
ก่อนสรุป ไม่ skip; `/jib-check` จะรัน analyzer จริงเสมอ ไม่ได้แค่เดาด้วย
intuition ของ LLM อย่างเดียว ผลคือ output ทำซ้ำได้และตรงประเด็นกว่าการ
เปิด chat ลอยๆ

Slash commands **enforce a flow** — `/jib-deep` won't skip dimensions,
`/jib-check` always runs the actual analyzer instead of LLM-guessing.
Output is more reproducible and on-point than free-form chat.

---

## การติดตั้ง / Installation

> ⚠️ Skill คือ **ชุดคำสั่งที่ Claude ทำตาม** ควรเปิดอ่าน [`SKILL.md`](SKILL.md)
> ก่อนติดตั้งทุกครั้ง เพื่อให้แน่ใจว่าเข้าใจสิ่งที่ skill จะทำ
>
> ⚠️ Skills are **instructions Claude follows**. Always review
> [`SKILL.md`](SKILL.md) before installing any community skill.

### 1) Claude.ai (Pro/Max/Team/Enterprise)

1. ดาวน์โหลด `.skill` ล่าสุดจาก [**Releases page**](https://github.com/pannatron/long-jib-ther-doo/releases/latest)
2. ไปที่ **Settings → Capabilities → Skills**
3. กด **Upload skill** แล้วเลือกไฟล์ที่ดาวน์โหลด
4. เปิดใช้งาน — เริ่มคุยกับ Claude ได้เลย

```
Releases → long-jib-ther-doo.skill → Settings → Capabilities → Skills → Upload
```

### 2) Claude Code (CLI)

**วิธี A — One-line install (แนะนำสุด):**

```bash
curl -sSL https://github.com/pannatron/long-jib-ther-doo/raw/main/install.sh | bash
```
ดาวน์โหลด release ล่าสุดและติดตั้งที่ `~/.claude/skills/long-jib-ther-doo/` อัตโนมัติ
> โปรดอ่าน [`install.sh`](install.sh) ก่อนรัน piped-to-bash ทุกครั้ง

**วิธี B — Clone จาก GitHub:**

```bash
git clone https://github.com/pannatron/long-jib-ther-doo.git ~/.claude/skills/long-jib-ther-doo
claude   # เริ่ม session ใหม่
```

**วิธี C — ดาวน์โหลด .skill จาก Releases:**

```bash
curl -L -o /tmp/long-jib.skill \
  https://github.com/pannatron/long-jib-ther-doo/releases/latest/download/long-jib-ther-doo.skill
unzip /tmp/long-jib.skill -d ~/.claude/skills/
```

**วิธี D — Plugin marketplace:**

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

## 🔒 Privacy / ความเป็นส่วนตัว

**Skill นี้ทำงานในเครื่องคุณทั้งหมด — ไม่มีการส่งข้อความ/แชตไปที่ไหน**

- 🖥️ **Local-only** — `bin/` scripts รันด้วย Python stdlib ของเครื่องคุณ
- 🚫 **ไม่มี network call** — ลองอ่านโค้ด `src/` ได้เลย ไม่มี `urllib`,
  `requests`, หรือ outbound HTTP ทั้งหมด
- 🔍 **Open source** — ตรวจได้ทุกบรรทัด ไม่ใช่ black box
- 🗑️ **ไม่เก็บ data** — output ออกมาที่ stdout, ไม่ save log/cache
  อะไรเลย (ถ้า save เอง คุณรู้แน่ว่าอยู่ไหน)

> **Skill นี้ทำงานผ่าน Claude** — Claude เห็นข้อความที่คุณ paste เข้าไป
> ตาม policy ปกติของ Claude (Anthropic) ตัว `bin/` ไม่ส่งอะไรเพิ่ม

**This skill runs entirely on your machine.** No chat data leaves your
computer through the skill itself. Read [src/](src/) to verify — there
are no network imports anywhere. The skill operates via Claude, which
sees what you paste per Anthropic's standard data policy.

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
# แก้ SKILL.md ได้เลย — ไม่ต้อง build .skill เอง
# CI จะ build และ publish ให้อัตโนมัติเมื่อ tag release
```

**Development:**
```bash
# Run tests
python3 -m unittest discover tests -v

# Try CLI tools locally
./bin/analyze "draft text"
./bin/opener --list
```

**Release process (สำหรับ maintainer):**
```bash
git tag v1.0.0
git push --tags
# → GitHub Actions จะ build .skill (รวม bin/, src/, data/) และสร้าง Release ให้อัตโนมัติ
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
