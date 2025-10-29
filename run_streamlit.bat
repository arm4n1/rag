@echo off
REM ============================================================
REM RAG Auto-Grading System - Streamlit App Launcher
REM ============================================================

echo.
echo ============================================================
echo   RAG AUTO-GRADING SYSTEM - WEB INTERFACE
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo [ERROR] Virtual environment tidak ditemukan!
    echo Jalankan setup.bat terlebih dahulu
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if streamlit is installed
python -c "import streamlit" 2>nul
if %errorlevel% neq 0 (
    echo [*] Installing Streamlit dependencies...
    pip install -r requirements_streamlit.txt
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if plotly is installed
python -c "import plotly" 2>nul
if %errorlevel% neq 0 (
    echo [*] Installing Plotly...
    pip install plotly
)

echo.
echo [*] Starting Streamlit app...
echo [*] URL will open automatically in your browser
echo [*] Press Ctrl+C to stop the server
echo.

REM Run streamlit app
streamlit run streamlit_app.py

pause
