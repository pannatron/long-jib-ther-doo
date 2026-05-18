"""Opener template library.

Returns a curated set of opener templates given the context of how you met.
Each template has an `intent` so Claude can pick the variant matching what
the user actually wants (low-pressure follow-up vs. direct invite, etc.).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@dataclass
class Opener:
    intent: str
    th: str
    en: str


@dataclass
class OpenerSuggestion:
    category: str
    label_th: str
    label_en: str
    openers: list[Opener]
    warning_th: str | None = None
    warning_en: str | None = None
    universal_dont: list[str] | None = None

    def to_dict(self) -> dict:
        return {
            "category": self.category,
            "label_th": self.label_th,
            "label_en": self.label_en,
            "openers": [asdict(o) for o in self.openers],
            "warning_th": self.warning_th,
            "warning_en": self.warning_en,
            "universal_dont": self.universal_dont,
        }


def _load_openers(path: Path | None = None) -> dict:
    p = path or (DATA_DIR / "openers.json")
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def suggest(category: str, data: dict | None = None) -> OpenerSuggestion:
    """Return opener templates for the given category.

    Raises KeyError if category is not in the library — callers should
    list_categories() first if unsure.
    """
    if data is None:
        data = _load_openers()

    cat = data["categories"][category]
    return OpenerSuggestion(
        category=category,
        label_th=cat["label_th"],
        label_en=cat["label_en"],
        openers=[Opener(**t) for t in cat["templates"]],
        warning_th=cat.get("warning_th"),
        warning_en=cat.get("warning_en"),
        universal_dont=data.get("universal_dont"),
    )


def list_categories(data: dict | None = None) -> list[dict]:
    if data is None:
        data = _load_openers()
    return [
        {"id": k, "label_th": v["label_th"], "label_en": v["label_en"]}
        for k, v in data["categories"].items()
    ]
