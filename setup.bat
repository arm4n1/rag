@echo off
REM ============================================================
REM RAG Auto-Grading System - Setup Script
REM Automatic setup untuk Windows
REM ============================================================

echo.
echo ============================================================
echo   RAG AUTO-GRADING SYSTEM v2.0 - SETUP
echo ============================================================
echo.

REM Check Python version
echo [1/5] Checking Python version...
py -3.12 --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python 3.12 tidak ditemukan!
    echo.
    echo Silakan install Python 3.12 terlebih dahulu:
    echo https://www.python.org/downloads/
    echo.
    echo Atau cek versi Python yang terinstall:
    py --list
    echo.
    pause
    exit /b 1
)

echo [OK] Python 3.12 ditemukan
py -3.12 --version

REM Create virtual environment
echo.
echo [2/5] Creating virtual environment...
if exist venv (
    echo [SKIP] Virtual environment sudah ada
) else (
    py -3.12 -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Gagal membuat virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)

REM Activate virtual environment
echo.
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Gagal aktivasi virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated

REM Upgrade pip
echo.
echo [4/5] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo [OK] Pip upgraded

REM Install dependencies
echo.
echo [5/5] Installing dependencies...
echo This may take 5-10 minutes depending on your internet connection...
echo.
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Gagal install dependencies
    pause
    exit /b 1
)

echo.
echo [OK] All dependencies installed successfully!

REM Verify installation
echo.
echo ============================================================
echo VERIFYING INSTALLATION
echo ============================================================
echo.

python -c "import torch; import sentence_transformers; import faiss; import dotenv; print('[OK] All critical libraries imported successfully!')"
if %errorlevel% neq 0 (
    echo [ERROR] Import verification failed
    echo Please check the error messages above
    pause
    exit /b 1
)

REM Check .env file
echo.
if exist .env (
    echo [OK] .env file found
) else (
    echo [WARNING] .env file not found
    echo Please create .env file before running the system
)

REM Check data folder
echo.
if exist data\rubrik.json (
    echo [OK] Rubrik file found
) else (
    echo [WARNING] data\rubrik.json not found
)

REM Create output folder
if not exist output mkdir output
echo [OK] Output folder ready

echo.
echo ============================================================
echo SETUP COMPLETED SUCCESSFULLY!
echo ============================================================
echo.
echo Next steps:
echo 1. Make sure .env file is configured correctly
echo 2. Put your PDF files in data\ folder
echo 3. Run: python rag_grading_improved.py
echo.
echo Quick commands:
echo   - Activate environment: venv\Scripts\activate
echo   - Run grading: python rag_grading_improved.py
echo   - View results: explorer output\
echo.
echo For detailed guide, read: PANDUAN_INSTALASI.md
echo For quick reference, read: QUICK_START.md
echo.

pause
