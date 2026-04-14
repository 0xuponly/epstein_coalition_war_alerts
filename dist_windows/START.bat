@echo off
title Telegram channel forwarder
echo.
echo ========================================
echo   Telegram channel forwarder (Windows)
echo ========================================
echo.
cd /d "%~dp0"
python windows_launcher.py
echo.
echo Closed.
pause
