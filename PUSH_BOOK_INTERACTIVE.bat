@echo off
REM Push book to GitHub interactively

echo.
echo ============================================================
echo PUSH BOOK TO GITHUB
echo ============================================================
echo.
echo Username: dirvenmjh
echo.
echo You need a GitHub Personal Access Token with 'repo' scope.
echo Create at: https://github.com/settings/tokens
echo.

set /p GITHUB_TOKEN="Enter your GitHub token: "

if "%GITHUB_TOKEN%"=="" (
    echo [ERROR] No token provided
    pause
    exit /b 1
)

echo.
echo Pushing book to GitHub...
echo.

python c:/hashtag1/push_book_interactive.py

echo.
echo ============================================================
echo Done!
echo View at: https://github.com/dirvenmjh/dirven-books
echo ============================================================
echo.
pause
