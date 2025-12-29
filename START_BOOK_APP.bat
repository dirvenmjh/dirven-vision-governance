@echo off
REM Dirven's Book Authoring System - Startup Script

echo.
echo ============================================================
echo DIRVEN'S BOOK AUTHORING SYSTEM
echo ============================================================
echo.
echo Starting Flask web server...
echo.
echo Opening: http://localhost:5000
echo.
echo To connect GitHub:
echo 1. Read: GITHUB_SETUP_DIRVENMJH.md
echo 2. Create token at: https://github.com/settings/tokens
echo 3. Enter token in web UI
echo.
echo Repository: https://github.com/dirvenmjh/dirven-books
echo.
echo ============================================================
echo.

python book_app_web.py
pause
