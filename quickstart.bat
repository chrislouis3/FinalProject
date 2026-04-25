@echo off
REM
REM Quick Start Script for Student Grading System
REM Windows Version
REM

echo.
echo ========================================
echo Student Grading System - Quick Start
echo ========================================
echo.

REM Check if venv exists
if not exist "venv\" (
    echo [1/3] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 goto error
)

REM Activate venv
echo [2/3] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 goto error

REM Install dependencies
echo [3/3] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 goto error

echo.
echo ========================================
echo Setup Complete! 
echo ========================================
echo.
echo Starting Student Grading System...
echo Accessing at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server.
echo.

REM Start application
python run.py

goto end

:error
echo.
echo ERROR: Setup failed!
echo Please check the console output above.
exit /b 1

:end
