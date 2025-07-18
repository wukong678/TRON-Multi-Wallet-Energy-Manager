@echo off
chcp 65001 >nul
echo ================================
echo    USDT管理工具 - 依赖安装
echo ================================
echo.
echo 正在安装必要的依赖库...
echo.

pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ✅ 依赖安装成功！
    echo 现在可以运行 "启动工具.bat" 来使用USDT管理工具
) else (
    echo.
    echo ❌ 依赖安装失败，请检查：
    echo 1. 是否已安装Python
    echo 2. 网络连接是否正常
    echo 3. 是否有管理员权限
)

echo.
pause