@echo off
chcp 65001 >nul
cd /d "%~dp0.."
title TarDAL-Poss 后端 (Flask :5000)
if exist ".venv\Scripts\python.exe" (
  echo [TarDAL-Poss] 使用虚拟环境 .venv
  ".venv\Scripts\python.exe" backend\app.py
) else (
  echo [TarDAL-Poss] 使用系统 PATH 中的 python
  python backend\app.py
)
echo.
echo [TarDAL-Poss] 后端已退出。若报错，请确认已在项目根目录执行 pip install -r requirements.txt
pause
