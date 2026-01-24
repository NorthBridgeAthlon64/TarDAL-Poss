@echo off
chcp 65001 >nul
echo ====================================
echo    TarDAL 图像融合系统启动器
echo ====================================
echo.

echo 🔍 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装或未添加到PATH
    echo 请安装Python 3.8+并添加到系统PATH
    pause
    exit /b 1
)

echo ✅ Python环境检查通过
echo.

echo 🚀 启动TarDAL系统...
python run_system.py

echo.
echo 👋 系统已停止
pause