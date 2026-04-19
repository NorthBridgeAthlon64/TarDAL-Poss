@echo off
setlocal
cd /d "%~dp0.."

rem Wrapper: real logic in clean_cache.ps1 (avoids cmd parsing issues with pipes and UTF-8).

set "ARGS="
if /I "%~1"=="full" set "ARGS=-Full"

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0clean_cache.ps1" %ARGS%
if errorlevel 1 (
  echo ERROR: clean_cache.ps1 failed.
  pause
  exit /b 1
)

echo.
pause
exit /b 0
