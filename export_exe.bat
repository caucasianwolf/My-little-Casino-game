@echo off
if not exist dist\main.exe (
  echo dist\main.exe not found. Run build_exe.bat first.
  pause
  exit /b 1
)
echo Copying dist\main.exe to project root as Casino777.exe...
copy /Y dist\main.exe Casino777.exe >nul
if %errorlevel% equ 0 (
  echo Created Casino777.exe in project root.
) else (
  echo Failed to copy executable.
)
pause
