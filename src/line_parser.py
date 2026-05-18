"""Parse LINE chat export (.txt) into structured stats.

LINE mobile/desktop "Send chat history" produces a text file roughly like:

    [LINE] Chat with John Doe
    Saved on: 2024/01/15 14:30

    2024/01/15 (Mon)
    10:23\tJohn Doe\tสวัสดี
    10:25\tMe\tหวัดดี
    11:00\tJohn Doe\tไปกินข้าวยัง?

    2024/01/16 (Tue)
    09:15\tMe\tไปทำงาน

Fields are typically tab-separated; falls back to multi-space split.
Date headers re-anchor the timestamp so we can compute real reply gaps
across multi-day conversations.
"""
from __future__ import annotations

import re
from datetime import datetime
from .signals import ChatStats

DATE_PATTERN = re.compile(r"^(\d{4})[/-](\d{1,2})[/-](\d{1,2})(?:\s*\([^)]+\))?\s*$")
MSG_PATTERN_TAB = re.compile(r"^(\d{1,2}):(\d{2})\t([^\t]+)\t(.+)$")
MSG_PATTERN_SPACES = re.compile(r"^(\d{1,2}):(\d{2})\s{2,}(\S(?:.*?\S)?)\s{2,}(.+)$")

QUESTION_PATTERN = re.compile(
    r"[?？]|ไหม|มั้ย|เหรอ|รึเปล่า|หรือเปล่า|รึยัง|ป่ะ|ปะ",
    re.I,
)

YOU_DEFAULT_ALIASES = {"me", "you", "i", "เรา", "ผม", "ฉัน", "กู", "หนู"}

SKIP_CONTENT_MARKERS = {
    "[Photo]", "[Sticker]", "[Video]", "[Audio]", "[File]", "[Voice]",
    "[รูปภาพ]", "[สติกเกอร์]", "[วิดีโอ]", "[เสียง]", "[ไฟล์]",
    "☎ Missed call", "Unsent a message",
}


def _is_skip_content(msg: str) -> bool:
    msg_strip = msg.strip()
    return any(msg_strip.startswith(m) for m in SKIP_CONTENT_MARKERS)


def parse_line_export(
    raw: str,
    *,
    your_name: str | None = None,
    their_name: str | None = None,
) -> ChatStats:
    you_aliases = set(YOU_DEFAULT_ALIASES)
    if your_name:
        you_aliases.add(your_name.lower())

    your_msgs: list[str] = []
    their_msgs: list[str] = []
    your_q = 0
    their_q = 0
    reply_gaps_minutes: list[float] = []

    current_date: datetime | None = None
    last_you_time: datetime | None = None
    last_speaker: str | None = None
    their_initiations = 0
    last_their_streak = 0
    consecutive_short = 0

    for line in raw.splitlines():
        line = line.rstrip()
        if not line:
            continue

        m_date = DATE_PATTERN.match(line)
        if m_date:
            try:
                current_date = datetime(
                    int(m_date.group(1)),
                    int(m_date.group(2)),
                    int(m_date.group(3)),
                )
            except ValueError:
                pass
            continue

        m = MSG_PATTERN_TAB.match(line) or MSG_PATTERN_SPACES.match(line)
        if not m:
            continue

        hh, mm, name, msg = m.groups()
        name = name.strip()
        msg = msg.strip()

        if _is_skip_content(msg):
            continue

        msg_time: datetime | None = None
        if current_date is not None:
            try:
                msg_time = current_date.replace(hour=int(hh), minute=int(mm))
            except ValueError:
                msg_time = None

        is_you = name.lower() in you_aliases or (
            their_name is not None and name.lower() != their_name.lower()
            and name.lower() in you_aliases
        )

        if is_you:
            your_msgs.append(msg)
            if QUESTION_PATTERN.search(msg):
                your_q += 1
            last_you_time = msg_time
        else:
            their_msgs.append(msg)
            if QUESTION_PATTERN.search(msg):
                their_q += 1
            if last_speaker is None:
                their_initiations += 1
            if last_you_time and msg_time:
                gap = (msg_time - last_you_time).total_seconds() / 60
                if gap > 0:
                    reply_gaps_minutes.append(gap)
            if len(msg) < 15:
                last_their_streak += 1
                consecutive_short = max(consecutive_short, last_their_streak)
            else:
                last_their_streak = 0

        last_speaker = "you" if is_you else "them"

    avg_reply = (
        sum(reply_gaps_minutes) / len(reply_gaps_minutes)
        if reply_gaps_minutes
        else 60.0
    )

    return ChatStats(
        your_msgs=len(your_msgs),
        their_msgs=len(their_msgs),
        your_avg_len=sum(len(m) for m in your_msgs) / max(len(your_msgs), 1),
        their_avg_len=sum(len(m) for m in their_msgs) / max(len(their_msgs), 1),
        your_questions=your_q,
        their_questions=their_q,
        their_avg_reply_minutes=avg_reply,
        their_initiations=their_initiations,
        consecutive_short_replies=consecutive_short,
    )
