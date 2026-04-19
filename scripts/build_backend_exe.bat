@echo off
setlocal
cd /d "%~dp0.."

rem NOTE: Do not use ASCII parentheses inside bare "echo" lines - cmd.exe parses them as block/subshell syntax.

echo ========================================
echo   TarDAL-Poss: build backend EXE
echo ========================================
echo Developer machine only: needs pip deps and PyInstaller.
echo Offline judge bundle: weights\v1\tardal-dt.pth and mask-u2.pth must exist before PyInstaller.
echo If frontend\dist already exists, npm is SKIPPED.
echo To rebuild frontend: set FORCE_NPM=1 before running this script.
echo.

if not exist "weights\v1\tardal-dt.pth" (
  echo ERROR: missing weights\v1\tardal-dt.pth — place release weight here for offline EXE.
  pause
  exit /b 1
)
if not exist "weights\v1\mask-u2.pth" (
  echo ERROR: missing weights\v1\mask-u2.pth — place release weight here for offline EXE.
  pause
  exit /b 1
)

rem --- Frontend: skip npm when dist exists unless FORCE_NPM=1 ---
if /I "%FORCE_NPM%"=="1" goto :npm_build
if exist "frontend\dist\index.html" (
  echo SKIP npm: frontend\dist already present. Set FORCE_NPM=1 to rebuild.
  goto :after_npm
)

:npm_build
where npm >nul 2>&1
if errorlevel 1 (
  echo ERROR: npm not found. Install Node.js LTS, or build frontend elsewhere and copy frontend\dist here.
  pause
  exit /b 1
)
if not exist "frontend\node_modules\" (
  echo [npm] node_modules missing - running npm install ...
  pushd frontend
  call npm install
  if errorlevel 1 (
    echo ERROR: npm install failed.
    popd
    pause
    exit /b 1
  )
  popd
)
echo [npm] npm run build ...
pushd frontend
call npm run build
if errorlevel 1 (
  echo ERROR: npm run build failed.
  popd
  pause
  exit /b 1
)
popd

:after_npm
if not exist "frontend\dist\index.html" (
  echo ERROR: frontend\dist\index.html not found. Run npm run build in frontend or set FORCE_NPM=1.
  pause
  exit /b 1
)

echo [pyinstaller] packaging ...
echo.

python -c "import flask" 2>nul
if errorlevel 1 (
  echo [pip] Flask or deps missing - installing requirements.txt ...
  pip install -r requirements.txt
  if errorlevel 1 (
    echo ERROR: pip install -r requirements.txt failed.
    pause
    exit /b 1
  )
)

pip show pyinstaller >nul 2>&1
if errorlevel 1 (
  echo [pip] Installing PyInstaller...
  pip install "pyinstaller>=6.0"
  if errorlevel 1 (
    echo ERROR: pip install pyinstaller failed.
    pause
    exit /b 1
  )
)

echo Running PyInstaller - this may take a long time.
pyinstaller --clean --noconfirm tardal_backend.spec
if errorlevel 1 (
  echo ERROR: PyInstaller failed. Check the log above.
  pause
  exit /b 1
)

echo Copying Picture-Example next to EXE for judges...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Copy-PictureExampleToDist.ps1" -DistBackendRoot "%CD%\dist\TarDAL-Poss-Backend"

echo.
echo Done. Output folder:
echo   %CD%\dist\TarDAL-Poss-Backend\
echo.
echo Run from folder: dist\TarDAL-Poss-Backend\  - TarDAL-Poss-Backend.exe or RUN.bat
echo.
pause
exit /b 0
