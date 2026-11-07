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
