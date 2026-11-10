from __future__ import annotations

from pathlib import Path

import pytest

import db


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    path = tmp_path / "test.db"
    db.init_db(path)
    return path


def _add(name: str, path: Path) -> int:
    return db.add_student(name, "2026", ["python"], ["en"], "evenings", db_path=path)


def test_list_students_sorted_by_name(db_path: Path) -> None:
    _add("Zoya", db_path)
    _add("Aman", db_path)
    assert [s.name for s in db.list_students(db_path=db_path)] == ["Aman", "Zoya"]


def test_get_student_missing_returns_none(db_path: Path) -> None:
    assert db.get_student(999, db_path=db_path) is None


def test_update_student_changes_fields_and_bumps_last_updated(
    db_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(db, "_utc_now_iso", lambda: "2026-01-01T00:00:00+00:00")
    sid = _add("Aman", db_path)
    monkeypatch.setattr(db, "_utc_now_iso", lambda: "2026-02-01T00:00:00+00:00")
    db.update_student(sid, "Aman K", "2027", ["sql"], ["hi"], "weekends", db_path=db_path)

    s = db.get_student(sid, db_path=db_path)
    assert s is not None
    assert (s.name, s.batch, s.skills, s.languages) == ("Aman K", "2027", ["sql"], ["hi"])
    assert s.availability_style == "weekends"
    assert s.last_updated == "2026-02-01T00:00:00+00:00"


def test_update_student_missing_raises(db_path: Path) -> None:
    with pytest.raises(ValueError):
        db.update_student(999, "X", "2026", [], [], "evenings", db_path=db_path)


def test_update_student_empty_name_raises(db_path: Path) -> None:
    sid = _add("Aman", db_path)
    with pytest.raises(ValueError):
        db.update_student(sid, "  ", "2026", [], [], "evenings", db_path=db_path)


def test_list_events_ordered_by_date(db_path: Path) -> None:
    db.create_event("Later", "", 3, "2026-12-01", db_path=db_path)
    db.create_event("Sooner", "", 3, "2026-11-20", db_path=db_path)
    assert [e.title for e in db.list_events(db_path=db_path)] == ["Sooner", "Later"]