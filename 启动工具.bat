@echo off
chcp 65001 >nul
echo ================================
echo    USDT管理工具启动器
echo ================================
echo.
echo 正在启动USDT管理工具...
echo.

python usdt_manager.py

if %errorlevel% neq 0 (
    echo.
    echo 启动失败，请检查：
    echo 1. 是否已安装Python
    echo 2. 是否已安装tronpy库 ^(pip install tronpy^)
    echo.
    pause
)