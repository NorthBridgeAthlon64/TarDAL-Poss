@echo off
chcp 65001 >nul
cd /d "%~dp0..\frontend"
title TarDAL-Poss 前端 (Vite)
if not exist "node_modules\" (
  echo [错误] 未找到 frontend\node_modules
  echo 请在 frontend 目录执行: npm install
  pause
  exit /b 1
)
echo [TarDAL-Poss] 启动 Vite 开发服务器...
call npm run dev
echo.
echo [TarDAL-Poss] 前端已退出。
pause
