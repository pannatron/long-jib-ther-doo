"""Parse LINE chat export (.txt) into structured stats.

Handles two LINE export formats:

1. International (English UI):
       2024/01/15 (Mon)
       10:23\tJohn\tสวัสดี

2. Thai UI (BE = Buddhist Era, BE - 543 = AD year):
       Tue, 27/01/2569 BE
       23:14\tสงกรานต์\t0863716832

Fields are typically tab-separated; falls back to multi-space split.
Date headers re-anchor the timestamp so we can compute real reply gaps
across multi-day conversations.

Initiations are counted at session boundaries — a gap of more than
SESSION_GAP_HOURS since the last message marks a new conversation, and
if the other person starts that session, it counts as them initiating.
Reply gaps greater than SESSION_GAP_HOURS are excluded from the average
since those are "they replied next day" rather than "delayed reply."
"""
from __future__ import annotations

import re
from datetime import datetime, timedelta
from .signals import ChatStats

DATE_PATTERN_ISO = re.compile(
    r"^(\d{4})[/-](\d{1,2})[/-](\d{1,2})(?:\s*\([^)]+\))?\s*$"
)
DATE_PATTERN_THAI_BE = re.compile(
    r"^(?:\w+,\s*)?(\d{1,2})/(\d{1,2})/(\d{4})\s*BE\s*$",
    re.IGNORECASE,
)

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

SESSION_GAP_HOURS = 8


def _is_skip_content(msg: str) -> bool:
    msg_strip = msg.strip()
    return any(msg_strip.startswith(m) for m in SKIP_CONTENT_MARKERS)


def _parse_date_header(line: str) -> datetime | None:
    m = DATE_PATTERN_ISO.match(line)
    if m:
        try:
            return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            return None

    m = DATE_PATTERN_THAI_BE.match(line)
    if m:
        day, month, be_year = int(m.group(1)), int(m.group(2)), int(m.group(3))
        try:
            return datetime(be_year - 543, month, day)
        except ValueError:
            return None

    return None


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
    last_msg_time: datetime | None = None
    last_you_time: datetime | None = None
    last_speaker: str | None = None
    their_initiations = 0
    last_their_streak = 0
    consecutive_short = 0

    session_gap = timedelta(hours=SESSION_GAP_HOURS)

    for line in raw.splitlines():
        line = line.rstrip()
        if not line:
            continue

        parsed_date = _parse_date_header(line)
        if parsed_date is not None:
            current_date = parsed_date
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

        is_you = name.lower() in you_aliases

        is_new_session = (
            last_msg_time is None
            or (msg_time is not None and (msg_time - last_msg_time) >= session_gap)
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
            if is_new_session:
                their_initiations += 1
            if last_you_time and msg_time:
                gap_minutes = (msg_time - last_you_time).total_seconds() / 60
                if 0 < gap_minutes <= SESSION_GAP_HOURS * 60:
                    reply_gaps_minutes.append(gap_minutes)
            if len(msg) < 15:
                last_their_streak += 1
                consecutive_short = max(consecutive_short, last_their_streak)
            else:
                last_their_streak = 0

        if msg_time is not None:
            last_msg_time = msg_time
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
