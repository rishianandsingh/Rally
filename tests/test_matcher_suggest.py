from __future__ import annotations

import pytest

from db import Student
from matcher import (
    STYLE_TO_SLOTS,
    Candidate,
    from_student,
    suggest_teammates,
)

EVE = STYLE_TO_SLOTS["weekday evenings"]
WEEKEND = STYLE_TO_SLOTS["weekends"]


def _c(sid: int, skills: set[str], slots: frozenset[str]) -> Candidate:
    return Candidate(sid, frozenset(skills), slots)


def test_ranks_by_score_and_excludes_self() -> None:
    me = _c(1, {"python"}, EVE)
    others = [
        me,
        _c(3, {"python"}, EVE),     # comp 0.0, overlap 1.0 -> 0.4
        _c(2, {"sql"}, EVE),        # comp 1.0, overlap 1.0 -> 1.0
        _c(4, {"sql"}, WEEKEND),    # comp 1.0, overlap 0.0 -> 0.6
    ]
    result = suggest_teammates(me, others)
    assert [sid for sid, _ in result] == [2, 4, 3]
    assert [s for _, s in result] == pytest.approx([1.0, 0.6, 0.4])


def test_ties_go_to_lowest_id() -> None:
    me = _c(1, {"python"}, EVE)
    others = [_c(6, {"sql"}, EVE), _c(5, {"sql"}, EVE)]
    assert [sid for sid, _ in suggest_teammates(me, others)] == [5, 6]


def test_k_limits_results() -> None:
    me = _c(1, {"python"}, EVE)
    others = [_c(i, {"sql"}, EVE) for i in range(2, 10)]
    assert len(suggest_teammates(me, others, k=3)) == 3


def test_k_must_be_positive() -> None:
    with pytest.raises(ValueError):
        suggest_teammates(_c(1, {"a"}, EVE), [], k=0)


def test_from_student_normalizes_and_maps_slots() -> None:
    s = Student(7, "A", "2026-A", [" Python ", "SQL"], ["English"], "Weekends", "x")
    c = from_student(s)
    assert c.student_id == 7
    assert c.skills == frozenset({"python", "sql"})
    assert c.availability == WEEKEND


def test_from_student_unknown_style_raises() -> None:
    s = Student(7, "A", "2026-A", ["Python"], [], "mornings", "x")
    with pytest.raises(ValueError):
        from_student(s)