from __future__ import annotations

import json
import sqlite3
from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass
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
