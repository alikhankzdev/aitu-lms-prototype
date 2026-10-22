@echo off
title AITU LMS - Web Prototype
:: Освобождаем порт 8000 если он завис
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do taskkill /f /pid %%a >nul 2>&1
timeout /t 1 /nobreak >nul
start "" http://127.0.0.1:8000
python "%~dp0web_prototype.py"
pause
