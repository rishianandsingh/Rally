from __future__ import annotations
from options import AVAILABILITY_STYLES, BATCHES, LANGUAGES, SKILLS

import itertools
import random
from pathlib import Path

import db

SEED = 42

FIRST_NAMES = [
    "Aarav", "Diya", "Kabir", "Meera", "Rohan", "Isha", "Vihaan",
    "Ananya", "Arjun", "Saanvi", "Kiran", "Neha", "Dev", "Tara",
]
LAST_NAMES = ["Sharma", "Iyer", "Gupta", "Reddy", "Khan", "Das", "Nair", "Singh"]
NOTES = [
    "Need a frontend person",
    "Strong on the ML side, weak on deployment",
    "Happy to be the Git and docs person",
    "Looking for teammates who can meet on weekends",
    "Can lead, prefer a backend teammate",
    "First hackathon, eager to learn",
    "",
]
EVENTS: list[tuple[str, str, int, str]] = [
    ("EQUINOX AI Hackathon", "Build an AI tool for campus problems", 4, "2026-11-22"),
    ("DSA Sprint", "Team-based competitive programming round", 3, "2026-12-05"),
    ("Open Source Demo Day", "Present a contribution to a real project", 5, "2026-12-18"),
]


def seed(db_path: Path = db.DB_PATH, n_students: int = 28) -> dict[str, int]:
    """Wipe and rebuild the database with deterministic fake data."""
    db_path.unlink(missing_ok=True)
    db.init_db(db_path)
    rng = random.Random(SEED)

    full_names = [f"{f} {l}" for f, l in itertools.product(FIRST_NAMES, LAST_NAMES)]
    student_ids: list[int] = []
    for name in rng.sample(full_names, n_students):
        student_ids.append(
            db.add_student(
                name=name,
                batch=rng.choice(BATCHES),
                skills=rng.sample(SKILLS, rng.randint(2, 4)),
                languages=rng.sample(LANGUAGES, rng.randint(1, 2)),
                availability_style=rng.choice(AVAILABILITY_STYLES),
                db_path=db_path,
            )
        )

    n_entries = 0
    for title, description, team_size, date in EVENTS:
        event_id = db.create_event(title, description, team_size, date, db_path=db_path)
        for sid in rng.sample(student_ids, rng.randint(8, 12)):
            db.add_entry(sid, event_id, rng.choice(NOTES), db_path=db_path)
            n_entries += 1

    return {"students": len(student_ids), "events": len(EVENTS), "entries": n_entries}


if __name__ == "__main__":
    print(seed())
