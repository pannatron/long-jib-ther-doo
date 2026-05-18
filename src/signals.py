"""Signal zone calculator: green / yellow / red from conversation stats.

Takes structured chat stats and outputs an objective zone with a per-factor
breakdown. This makes the SKILL.md signal model reproducible rather than
relying on Claude's intuition each time.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict


@dataclass
class ChatStats:
    your_msgs: int
    their_msgs: int
    your_avg_len: float
    their_avg_len: float
    your_questions: int
    their_questions: int
    their_avg_reply_minutes: float
    their_initiations: int = 0
    consecutive_short_replies: int = 0


@dataclass
class SignalResult:
    zone: str
    score: float
    factors: dict = field(default_factory=dict)
    recommendation: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def _score_length_ratio(stats: ChatStats) -> tuple[float, str]:
    if stats.your_avg_len == 0:
        return 0.5, "ไม่มีข้อมูลความยาว"
    ratio = stats.their_avg_len / stats.your_avg_len
    if ratio >= 0.8:
        return 1.0, f"อีกฝ่ายตอบยาวพอกัน ({ratio:.2f})"
    if ratio >= 0.5:
        return 0.5, f"อีกฝ่ายตอบสั้นกว่าเรา ({ratio:.2f}) — เริ่มเฝ้าดู"
    return 0.0, f"อีกฝ่ายตอบสั้นกว่าเรามาก ({ratio:.2f}) — สัญญาณถอย"


def _score_questions_back(stats: ChatStats) -> tuple[float, str]:
    if stats.their_msgs == 0:
        return 0.0, "อีกฝ่ายยังไม่ตอบ"
    ratio = stats.their_questions / stats.their_msgs
    if ratio >= 0.3:
        return 1.0, f"อีกฝ่ายถามกลับ {stats.their_questions} ครั้ง"
    if ratio >= 0.1:
        return 0.5, f"ถามกลับน้อย ({stats.their_questions} ครั้ง)"
    return 0.0, "อีกฝ่ายไม่ถามกลับเลย"


def _score_reply_speed(stats: ChatStats) -> tuple[float, str]:
    mins = stats.their_avg_reply_minutes
    if mins <= 30:
        return 1.0, f"ตอบเร็ว (~{mins:.0f} นาที)"
    if mins <= 180:
        return 0.7, f"ตอบในเวลาเหมาะสม (~{mins:.0f} นาที)"
    if mins <= 720:
        return 0.4, f"ตอบช้า (~{mins/60:.1f} ชม)"
    return 0.1, f"ตอบช้ามาก (~{mins/60:.1f} ชม)"


def _score_initiation(stats: ChatStats) -> tuple[float, str]:
    if stats.their_initiations >= 3:
        return 1.0, f"อีกฝ่ายริเริ่มทักก่อน {stats.their_initiations} ครั้ง"
    if stats.their_initiations >= 1:
        return 0.6, f"อีกฝ่ายเคยทักก่อน {stats.their_initiations} ครั้ง"
    return 0.2, "อีกฝ่ายไม่เคยทักก่อนเลย"


def _score_recent_trend(stats: ChatStats) -> tuple[float, str]:
    n = stats.consecutive_short_replies
    if n == 0:
        return 1.0, "ไม่มี trend ตอบสั้นต่อเนื่อง"
    if n <= 2:
        return 0.5, f"ตอบสั้นต่อกัน {n} ครั้ง — เฝ้าดู"
    return 0.0, f"ตอบสั้นต่อกัน {n} ครั้ง — สัญญาณแดงชัด"


_WEIGHTS = {
    "length_ratio": 0.25,
    "questions_back": 0.25,
    "reply_speed": 0.15,
    "initiation": 0.15,
    "recent_trend": 0.20,
}


def _zone_from_score(score: float) -> tuple[str, str]:
    if score >= 0.65:
        return "green", (
            "สัญญาณตอบรับดี — ขยับเข้าใกล้อย่างเป็นธรรมชาติได้ "
            "เช่น ชวนคุยลึกขึ้น หรือชวนเจอถ้าจังหวะถึง"
        )
    if score >= 0.4:
        return "yellow", (
            "สัญญาณกลางๆ — คงจังหวะสบายๆ ไม่เร่ง "
            "ให้คุณค่าด้วยบทสนทนาที่น่าสนใจ ไม่ใช่ความถี่ "
            "สังเกตว่าจะขยับไปเขียวหรือแดง"
        )
    return "red", (
        "สัญญาณถอย — แนะนำให้หยุดทักไปสักพัก ให้พื้นที่ "
        "ไม่ส่งข้อความถามว่าทำไมเงียบ และไม่เปลี่ยนช่องทางไปตามต่อ"
    )


def calculate(stats: ChatStats) -> SignalResult:
    scores = {
        "length_ratio": _score_length_ratio(stats),
        "questions_back": _score_questions_back(stats),
        "reply_speed": _score_reply_speed(stats),
        "initiation": _score_initiation(stats),
        "recent_trend": _score_recent_trend(stats),
    }

    total = sum(scores[k][0] * _WEIGHTS[k] for k in scores)

    length_ratio = stats.their_avg_len / max(stats.your_avg_len, 1)
    if length_ratio < 0.3:
        total *= 0.6
    if stats.consecutive_short_replies >= 4:
        total = min(total, 0.35)

    zone, recommendation = _zone_from_score(total)

    factors = {
        k: {"score": round(v[0], 2), "weight": _WEIGHTS[k], "note": v[1]}
        for k, v in scores.items()
    }

    return SignalResult(
        zone=zone,
        score=round(total, 3),
        factors=factors,
        recommendation=recommendation,
    )
