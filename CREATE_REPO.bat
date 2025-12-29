@echo off
REM Create GitHub repository for Dirven's books

echo.
echo ============================================================
echo CREATE GITHUB REPOSITORY
echo ============================================================
echo.
echo This script will create: github.com/dirvenmjh/dirven-books
echo.
echo You will need your GitHub token.
echo Get it at: https://github.com/settings/tokens
echo.
echo ============================================================
echo.

python create_github_repo.py

echo.
echo ============================================================
echo Done! Repository created.
echo.
echo Next: python push_via_api.py
echo ============================================================
echo.
pause
