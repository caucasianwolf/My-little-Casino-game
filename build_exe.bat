@echo off
echo Installing PyInstaller (if not already installed)...
py -3 -m pip install --user pyinstaller
echo Building single-file executable (windowed)...
py -3 -m PyInstaller --onefile --windowed main.py
echo Build complete. Check the \dist folder for the executable.
pause
