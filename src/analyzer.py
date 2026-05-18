"""Pushiness analyzer for draft messages.

Scores a draft 0.0-1.0 on how likely it is to come across as pushy,
guilt-trippy, or otherwise off-putting. Returns flagged phrases with
explanations so Claude can talk the user through specific issues.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@dataclass
class Flag:
    rule_id: str
    category: str
    matched_text: str
    weight: float
    explanation: str


@dataclass
class AnalysisResult:
    draft: str
    pushiness: float
    verdict: str
    flags: list[Flag] = field(default_factory=list)
    length_warning: str | None = None

    def to_dict(self) -> dict:
        return {
            "draft": self.draft,
            "pushiness": round(self.pushiness, 3),
            "verdict": self.verdict,
            "flags": [asdict(f) for f in self.flags],
            "length_warning": self.length_warning,
        }


def _load_rules(rules_path: Path | None = None) -> dict:
    path = rules_path or (DATA_DIR / "rules.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _verdict_from_score(score: float) -> str:
    if score >= 0.7:
        return "red"
    if score >= 0.4:
        return "yellow"
    return "green"


def analyze(draft: str, rules: dict | None = None) -> AnalysisResult:
    """Analyze a draft message for pushiness signals."""
    if rules is None:
        rules = _load_rules()

    flags: list[Flag] = []
    for rule in rules["rules"]:
        for pattern in rule["patterns"]:
            match = re.search(pattern, draft, re.IGNORECASE)
            if match:
                flags.append(
                    Flag(
                        rule_id=rule["id"],
                        category=rule["category"],
                        matched_text=match.group(0),
                        weight=rule["weight"],
                        explanation=rule["explanation"],
                    )
                )
                break

    if flags:
        product = 1.0
        for f in flags:
            product *= 1.0 - f.weight
        pushiness = 1.0 - product
    else:
        pushiness = 0.0

    length_warning = None
    max_len = rules.get("length_thresholds", {}).get("opener_max_chars", 200)
    if len(draft) > max_len:
        length_warning = rules["length_thresholds"]["opener_warning"]
        pushiness = min(1.0, pushiness + 0.15)

    return AnalysisResult(
        draft=draft,
        pushiness=pushiness,
        verdict=_verdict_from_score(pushiness),
        flags=flags,
        length_warning=length_warning,
    )
