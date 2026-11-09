from pathlib import Path

import db
import seed


def test_seed_builds_expected_data(tmp_path: Path) -> None:
    path = tmp_path / "seed.db"
    counts = seed.seed(db_path=path)
    assert counts["students"] == 28
    assert counts["events"] == 3
    for event_id in (1, 2, 3):
        assert 8 <= len(db.get_entries(event_id, db_path=path)) <= 12


def test_seed_is_rerunnable_and_deterministic(tmp_path: Path) -> None:
    path = tmp_path / "seed.db"
    first = seed.seed(db_path=path)
    second = seed.seed(db_path=path)
    assert first == second
