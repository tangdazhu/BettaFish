@echo off
echo ========================================
echo BettaFish Startup Script
echo ========================================
echo.

REM 1. Activate conda environment
echo [1/3] Activating conda environment...
call conda activate bettafish
if %errorlevel% neq 0 (
    echo Error: Cannot activate conda environment 'bettafish'
    echo Please create it first: conda create -n bettafish python=3.9
    pause
    exit /b 1
)
echo OK - Conda environment activated
echo.

REM 2. Kill processes on ports
echo [2/3] Cleaning up ports...
echo Checking and closing occupied ports...

REM Function to kill process on port
setlocal enabledelayedexpansion
set "ports=5000 8501 8502 8503 8504 8505"

for %%p in (%ports%) do (
    netstat -aon | findstr :%%p | findstr LISTENING >nul 2>&1
    if !errorlevel! equ 0 (
        for /f "tokens=5" %%a in ('netstat -aon ^| findstr :%%p ^| findstr LISTENING') do (
            echo   - Closing port %%p process %%a
            taskkill /F /PID %%a >nul 2>&1
        )
    )
)
endlocal

echo OK - Ports cleaned
echo.

REM Wait 1 second to ensure ports are released
timeout /t 1 /nobreak >nul

REM 3. Start main application
echo [3/3] Starting main application...
echo.
echo ========================================
echo Starting BettaFish...
echo Main app will run at http://localhost:5000
echo ========================================
echo.
echo Press Ctrl+C to stop
echo.

python app.py

REM If application exits abnormally
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo Application exited with error code: %errorlevel%
    echo ========================================
    pause
)