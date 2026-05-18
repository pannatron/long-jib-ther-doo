"""Parse pasted chat history into structured stats.

Supports common Thai/English chat formats — line-prefixed with name (e.g.
"Me: hi", "เขา: หวัดดี"). Stats feed into signals.calculate().
"""
from __future__ import annotations

import re
from datetime import datetime
from .signals import ChatStats

YOU_ALIASES = {"me", "you", "i", "เรา", "ผม", "ฉัน", "กู", "หนู"}
THEM_ALIASES = {"them", "her", "him", "they", "เขา", "เค้า", "อีกฝ่าย", "crush"}

QUESTION_PATTERN = re.compile(
    r"[?？]|ไหม|มั้ย|เหรอ|รึเปล่า|หรือเปล่า|รึยัง|ป่ะ|ปะ",
    re.I,
)

LINE_PATTERNS = [
    re.compile(r"^\[?(?P<time>\d{1,2}:\d{2}(?:\s?[AP]M)?)\]?\s*(?P<name>[^:]+?):\s*(?P<msg>.+)$", re.I),
    re.compile(r"^(?P<name>[^:]+?):\s*(?P<msg>.+)$"),
]


def _classify_speaker(name: str) -> str | None:
    name_lower = name.strip().lower()
    if name_lower in YOU_ALIASES:
        return "you"
    if name_lower in THEM_ALIASES:
        return "them"
    return None


def _parse_time(s: str | None) -> datetime | None:
    if not s:
        return None
    for fmt in ("%H:%M", "%I:%M %p", "%I:%M%p"):
        try:
            return datetime.strptime(s.strip().upper(), fmt.upper())
        except ValueError:
            continue
    return None


def parse_chat(raw: str, *, your_name: str | None = None, their_name: str | None = None) -> ChatStats:
    """Parse a raw chat transcript into ChatStats."""
    if your_name:
        YOU_ALIASES.add(your_name.lower())
    if their_name:
        THEM_ALIASES.add(their_name.lower())

    your_msgs: list[str] = []
    their_msgs: list[str] = []
    your_q = 0
    their_q = 0
    reply_gaps_minutes: list[float] = []
    consecutive_short = 0

    last_you_time: datetime | None = None
    last_speaker: str | None = None
    their_initiations = 0
    last_short_streak_them = 0

    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue

        match = None
        for pattern in LINE_PATTERNS:
            match = pattern.match(line)
            if match:
                break
        if not match:
            continue

        gd = match.groupdict()
        speaker = _classify_speaker(gd["name"])
        if speaker is None:
            continue

        msg = gd["msg"].strip()
        time_obj = _parse_time(gd.get("time"))

        if speaker == "you":
            your_msgs.append(msg)
            if QUESTION_PATTERN.search(msg):
                your_q += 1
            last_you_time = time_obj
            if last_speaker is None:
                pass
        else:
            their_msgs.append(msg)
            if QUESTION_PATTERN.search(msg):
                their_q += 1
            if last_speaker is None or last_speaker == "them":
                if last_speaker is None:
                    their_initiations += 1
            if last_speaker == "you" and last_you_time and time_obj:
                gap = (time_obj - last_you_time).total_seconds() / 60
                if gap < 0:
                    gap += 24 * 60
                reply_gaps_minutes.append(gap)
            if len(msg) < 15:
                last_short_streak_them += 1
                consecutive_short = max(consecutive_short, last_short_streak_them)
            else:
                last_short_streak_them = 0

        last_speaker = speaker

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
