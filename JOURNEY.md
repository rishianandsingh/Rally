# Journey

**Scope:** Rally is a Streamlit app where teachers post Zenith events and students find teammates using structured profile fields.



## Entry 1: Environment setup

- **Prompt:** Asked for Mac-specific (M5 Air, VS Code terminal) steps for Saturday's Rally foundation: venv, dependencies, .gitignore, JOURNEY.md, Streamlit check, GitHub repo.

- **AI output:** A 10-step setup covering Python venv, `pip install streamlit pytest`, `.gitignore` (including `.DS_Store` and `._*`), a placeholder `app.py`, git init/commit, and `gh repo create`.

- **What I changed:**
  - Used Python 3.13 via Homebrew instead of the system 3.15, because 3.15 is too new for prebuilt wheels of Streamlit's dependencies.
  - Project lives on an external drive (`/Volumes/WORK`), so I checked the filesystem format before creating the venv.
  - Installed `gh` via Homebrew.
  - Renamed the project from "Team Matcher" to "Rally".

- **What broke:**
  - Ran `python venv .venv` without `-m`, so Python tried to run `venv` as a script. Fix: `python3.13 -m venv .venv`.
  - `python --version` failed because the venv wasn't active (macOS has no bare `python` outside a venv).
  - VS Code warned about global packages because its selected interpreter wasn't `.venv`. Fix: Python: Select Interpreter.
  - `gh` was not installed (command not found). Fix: `brew install gh`.
  
- **Lesson:** Activating a venv in a terminal and selecting an interpreter in VS Code are separate things, and both need to be set.

## Entry 2: Data layer

- **Prompt:** Asked for an elaborated step-by-step guide for Sunday's data layer (`db.py`, `seed.py`, no UI) from my saved week plan.

- **AI output:** Five design calls (JSON text for list columns, `UNIQUE(student_id, event_id)`, foreign keys ON per connection, ISO-8601 UTC timestamps, parameterized queries), then paste-ready blocks for each step.

- **What I built:**
  - `db.py`: frozen dataclasses, `get_conn()` context manager, schema, `init_db()`, `add_student`, `create_event`, `add_entry`, `get_entries`.
  - `seed.py`: deterministic (seed 42), 28 students, 3 events, 33 entries, safe to rerun.
  - `tests/test_db.py` and `tests/test_seed.py`: 14 tests passing, using pytest's `tmp_path` so the real DB is never touched.

- **What I changed:**
  - Added `CHECK (team_size >= 2)` in the schema as a second layer behind the Python validation.
  - `add_entry` converts the UNIQUE violation into a clean `ValueError`, while a missing student stays an `IntegrityError`.

- **What broke:**
  - Pylance struck through `contextmanager` because `-> Iterator[...]` is deprecated on `@contextmanager` functions. Fix: `Generator[sqlite3.Connection]`.
  - The AI told me to use `:memory:` for tests, which was wrong: each connection gets its own empty database. Used `tmp_path` instead.

- **Lesson:** SQLite ignores foreign keys unless `PRAGMA foreign_keys = ON` is set on every connection. Verified by testing that a nonexistent student id is rejected.
