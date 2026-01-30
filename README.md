# Higher or Lower — Casino Guess

Simple desktop guessing game built with Python and tkinter. Designed to run on Windows.

Features:
- Guess if the next card (1-13) is higher or lower than the current.
- Points per correct guess follow tiers: 10 (rounds 1-10), 25 (11-20), 50 (21-30), 100 (31+).
- Persistent local leaderboard stored in `leaderboard.json`.
- Casino-themed UI colors.

Run:

1. Make sure you have Python 3 installed.
2. From the project folder run:

```bash
python main.py
```

Packaging (optional):
- You can create a Windows executable with `pyinstaller --onefile main.py`.

Files:
- `main.py` — game application
- `leaderboard.json` — persistent leaderboard (created automatically)

Create download-ready exe:
- After building with `build_exe.bat`, run `export_exe.bat` to copy `dist/main.exe` to the project root as `Casino777.exe` which you can share or move.


