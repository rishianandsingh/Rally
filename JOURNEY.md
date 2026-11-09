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





## Entry 3: Mon Nov 9, matching logic

**Built:** `matcher.py` with a `Candidate` dataclass, a DB row adapter (`from_row`), `score_pair`, and a greedy `form_teams`. Added 6 pytest tests in `tests/test_matcher.py`. Matcher logic is pure Python with no SQLite or UI dependencies, so it can be tested with hand-built inputs.

**AI prompts used:** Asked Claude to elaborate the Monday plan step by step. Followed each step in order, pasting terminal output and errors back for debugging.

**Design decisions:**
- Pair score = 0.6 * skill complementarity + 0.4 * availability overlap, both Jaccard-based. Weights are module constants.
- Skills are stored in the DB as a JSON list string, so the adapter uses `json.loads`.
- Availability is stored as a style label, so I mapped each of the 3 styles to a set of time slots, with partial overlaps so the overlap score is graded and not just 0 or 1.
- Unknown availability styles raise a `ValueError` instead of silently producing an empty set.
- Team formation is deterministic: processed in student id order, ties go to the lowest id. Leftover students form a smaller final team and nobody is dropped.

**What broke and how I fixed it:**
- The first adapter assumed comma-separated skills, but the DB stores JSON lists. Checked real rows with a query and switched to `json.loads`.
- A column name guess (`availability`) was wrong. The real column is `availability_style`. Fixed by running `pragma table_info(students)`.
- zsh hung on a `quote>` prompt because an apostrophe in a pasted comment opened a quote. Fixed by removing the comment.
- `python3 -c` failed with an IndentationError because the pasted code block was indented. Fixed by pasting it flush left.
- pytest reported 20 passed instead of 6 because it also collected other test files. Confirmed by running `tests/test_matcher.py` alone.

**Known limitations:**
- Greedy grouping is order-dependent: the lowest id is seeded first and picks the best partners.
- Two students with empty skill sets would score as perfectly complementary. Seed data has none, so I left it.
- With only 3 availability styles, teams end up segmented by style. The style-to-slots mapping is my assumption, not user data.

**Result:** 28 seed students formed 7 teams of 4. Mean pair scores ranged from 0.85 to 0.97 with no sharp drop in later teams. Skills were mixed within every team and every team shared one availability style.