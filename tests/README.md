# Isolated Python model tests

Run from the repository root with Python 3.11+:

    python -m pip install pytest flake8
    python -m pytest -q tests
    python -m flake8 . --select=E9,F63,F7,F82 --show-source

The tests use a temporary SQLite database. They do not need actual Raspberry Pi
hardware, a Docker daemon, FastAPI, network access, or production credentials.

The CI intentionally runs a critical-error lint subset across the existing
Python files: syntax errors and high-impact Pyflakes checks. This is not
equivalent to full-project flake8 compliance. The previous lint step ignored
failures, and the previous dependency-install step targeted requirements.txt,
which does not exist in this repository.
