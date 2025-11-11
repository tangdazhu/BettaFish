@echo off
echo ========================================
echo Regenerate Final Report
echo ========================================
echo.

REM Activate conda environment
echo Activating conda environment...
call conda activate bettafish
if %errorlevel% neq 0 (
    echo Error: Cannot activate conda environment 'bettafish'
    pause
    exit /b 1
)
echo OK - Environment activated
echo.

REM Run regenerate script
echo Starting report regeneration...
echo.
python regenerate_report.py

echo.
echo ========================================
echo Done
echo ========================================
pause