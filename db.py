from __future__ import annotations

import json
import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

DB_PATH: Path = Path(__file__).parent / "rally.db"


@dataclass(frozen=True)
class Student:
    id: int
    name: str
    batch: str
    skills: list[str]
    languages: list[str]
    availability_style: str
    last_updated: str


@dataclass(frozen=True)
class Event:
    id: int
    title: str
    description: str
    team_size: int
    date: str


@dataclass(frozen=True)
class Entry:
    id: int
    student_id: int
    event_id: int
    note: str


@contextmanager
def get_conn(db_path: Path = DB_PATH) -> Generator[sqlite3.Connection]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


SCHEMA: str = """
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    batch TEXT NOT NULL,
    skills TEXT NOT NULL,
    languages TEXT NOT NULL,
    availability_style TEXT NOT NULL,
    last_updated TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    team_size INTEGER NOT NULL CHECK (team_size >= 2),
    date TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS event_entries (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id),
    event_id INTEGER NOT NULL REFERENCES events(id),
    note TEXT NOT NULL DEFAULT '',
    UNIQUE (student_id, event_id)
);
"""


def init_db(db_path: Path = DB_PATH) -> None:
    with get_conn(db_path) as conn:
        conn.executescript(SCHEMA)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _row_to_student(row: sqlite3.Row) -> Student:
    return Student(
        id=row["id"],
        name=row["name"],
        batch=row["batch"],
        skills=json.loads(row["skills"]),
        languages=json.loads(row["languages"]),
        availability_style=row["availability_style"],
        last_updated=row["last_updated"],
    )


def _new_id(cursor: sqlite3.Cursor) -> int:
    if cursor.lastrowid is None:
        raise RuntimeError("Insert did not produce a row id")
    return cursor.lastrowid


def add_student(
    name: str,
    batch: str,
    skills: list[str],
    languages: list[str],
    availability_style: str,
    *,
    db_path: Path = DB_PATH,
) -> int:
    if not name.strip():
        raise ValueError("name must not be empty")
    with get_conn(db_path) as conn:
        cur = conn.execute(
            "INSERT INTO students "
            "(name, batch, skills, languages, availability_style, last_updated) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                name.strip(),
                batch,
                json.dumps(skills),
                json.dumps(languages),
                availability_style,
                _utc_now_iso(),
            ),
        )
        return _new_id(cur)


def create_event(
    title: str,
    description: str,
    team_size: int,
    date: str,
    *,
    db_path: Path = DB_PATH,
) -> int:
    if not title.strip():
        raise ValueError("title must not be empty")
    if team_size < 2:
        raise ValueError("team_size must be at least 2")
    datetime.fromisoformat(date)  # raises ValueError if not ISO format
    with get_conn(db_path) as conn:
        cur = conn.execute(
            "INSERT INTO events (title, description, team_size, date) "
            "VALUES (?, ?, ?, ?)",
            (title.strip(), description, team_size, date),
        )
        return _new_id(cur)


def add_entry(
    student_id: int,
    event_id: int,
    note: str,
    *,
    db_path: Path = DB_PATH,
) -> int:
    with get_conn(db_path) as conn:
        try:
            cur = conn.execute(
                "INSERT INTO event_entries (student_id, event_id, note) "
                "VALUES (?, ?, ?)",
                (student_id, event_id, note),
            )
        except sqlite3.IntegrityError as e:
            if "UNIQUE" in str(e):
                raise ValueError("Student already entered this event") from e
            raise
        return _new_id(cur)


def get_entries(
    event_id: int, *, db_path: Path = DB_PATH
) -> list[tuple[Student, str]]:
    with get_conn(db_path) as conn:
        rows = conn.execute(
            "SELECT s.*, ee.note AS note "
            "FROM event_entries ee "
            "JOIN students s ON s.id = ee.student_id "
            "WHERE ee.event_id = ? "
            "ORDER BY s.name",
            (event_id,),
        ).fetchall()
    return [(_row_to_student(r), r["note"]) for r in rows]
