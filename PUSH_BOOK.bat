@echo off
REM Push book to GitHub

echo.
echo ============================================================
echo PUSH BOOK TO GITHUB
echo ============================================================
echo.
echo Enter your GitHub token when prompted:
echo.

set /p GITHUB_TOKEN="GitHub Token: "

echo.
echo Pushing book to: github.com/dirvenmjh/dirven-books
echo.

python c:/hashtag1/push_via_api.py

echo.
echo ============================================================
echo Done!
echo View at: https://github.com/dirvenmjh/dirven-books
echo ============================================================
echo.
pause
