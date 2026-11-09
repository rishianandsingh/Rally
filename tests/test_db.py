import sqlite3
from datetime import datetime
from pathlib import Path

import pytest

import db


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    path = tmp_path / "test.db"
    db.init_db(path)
    return path


@pytest.fixture
def student_id(db_path: Path) -> int:
    return db.add_student(
        "Asha", "B1", ["Python", "ML"], ["en", "hi"], "evenings", db_path=db_path
    )


@pytest.fixture
def event_id(db_path: Path) -> int:
    return db.create_event("Hackathon", "desc", 3, "2026-11-20", db_path=db_path)


def test_init_db_is_idempotent(db_path: Path) -> None:
    db.init_db(db_path)  # second call must not raise


def test_entry_round_trip_returns_decoded_lists(
    db_path: Path, student_id: int, event_id: int
) -> None:
    db.add_entry(student_id, event_id, "need a frontend dev", db_path=db_path)
    [(student, note)] = db.get_entries(event_id, db_path=db_path)
    assert student.skills == ["Python", "ML"]
    assert student.languages == ["en", "hi"]
    assert note == "need a frontend dev"


def test_name_with_apostrophe_is_stored_safely(db_path: Path, event_id: int) -> None:
    sid = db.add_student("O'Brien", "B1", [], [], "evenings", db_path=db_path)
    db.add_entry(sid, event_id, "", db_path=db_path)
    [(student, _)] = db.get_entries(event_id, db_path=db_path)
    assert student.name == "O'Brien"


def test_last_updated_is_timezone_aware_iso(
    db_path: Path, student_id: int, event_id: int
) -> None:
    db.add_entry(student_id, event_id, "", db_path=db_path)
    [(student, _)] = db.get_entries(event_id, db_path=db_path)
    assert datetime.fromisoformat(student.last_updated).tzinfo is not None


def test_duplicate_entry_raises_value_error(
    db_path: Path, student_id: int, event_id: int
) -> None:
    db.add_entry(student_id, event_id, "", db_path=db_path)
    with pytest.raises(ValueError, match="already entered"):
        db.add_entry(student_id, event_id, "", db_path=db_path)


def test_entry_for_nonexistent_student_is_rejected(
    db_path: Path, event_id: int
) -> None:
    with pytest.raises(sqlite3.IntegrityError):
        db.add_entry(999, event_id, "", db_path=db_path)


@pytest.mark.parametrize("team_size", [0, 1, -3])
def test_team_size_below_two_is_rejected(db_path: Path, team_size: int) -> None:
    with pytest.raises(ValueError, match="team_size"):
        db.create_event("T", "", team_size, "2026-11-20", db_path=db_path)


def test_non_iso_event_date_is_rejected(db_path: Path) -> None:
    with pytest.raises(ValueError):
        db.create_event("T", "", 3, "20/11/2026", db_path=db_path)


def test_blank_student_name_is_rejected(db_path: Path) -> None:
    with pytest.raises(ValueError, match="name"):
        db.add_student("   ", "B1", [], [], "evenings", db_path=db_path)


def test_get_entries_only_returns_requested_event(
    db_path: Path, student_id: int, event_id: int
) -> None:
    other_event = db.create_event("Other", "", 4, "2026-12-01", db_path=db_path)
    db.add_entry(student_id, other_event, "", db_path=db_path)
    assert db.get_entries(event_id, db_path=db_path) == []
