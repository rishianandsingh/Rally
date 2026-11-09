from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass

STYLE_TO_SLOTS: dict[str, frozenset[str]] = {
    "late nights": frozenset({"weekday_night", "weekend_night"}),
    "weekends": frozenset({"weekend_am", "weekend_pm", "weekend_night"}),
    "weekday evenings": frozenset({"weekday_eve", "weekday_night"}),
}


@dataclass(frozen=True)
class Candidate:
    student_id: int
    skills: frozenset[str]
    availability: frozenset[str]


def _skills(raw: str) -> frozenset[str]:
    try:
        items = json.loads(raw)
    except json.JSONDecodeError:
        return frozenset()
    return frozenset(str(s).strip().lower() for s in items if str(s).strip())


def from_row(row: sqlite3.Row) -> Candidate:
    style = row["availability_style"].strip().lower()
    slots = STYLE_TO_SLOTS.get(style)
    if slots is None:
        raise ValueError(f"Unknown availability style: {style!r}")
    return Candidate(
        student_id=row["id"],
        skills=_skills(row["skills"]),
        availability=slots,
    )


COMPLEMENTARITY_WEIGHT = 0.6
OVERLAP_WEIGHT = 0.4


def _jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    union = a | b
    if not union:
        return 0.0
    return len(a & b) / len(union)


def score_pair(a: Candidate, b: Candidate) -> float:
    """Higher = better teammates. Symmetric: score_pair(a, b) == score_pair(b, a)."""
    complementarity = 1.0 - _jaccard(a.skills, b.skills)
    overlap = _jaccard(a.availability, b.availability)
    return COMPLEMENTARITY_WEIGHT * complementarity + OVERLAP_WEIGHT * overlap