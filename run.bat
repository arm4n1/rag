@echo off
REM ============================================================
REM RAG Auto-Grading System - Run Script
REM Quick run script untuk Windows
REM ============================================================

echo.
echo ============================================================
echo   RAG AUTO-GRADING SYSTEM v2.0
echo   Sistem Penilaian Otomatis Laporan Praktikum
echo ============================================================
echo.

REM Check if venv exists
if not exist venv (
    echo [ERROR] Virtual environment tidak ditemukan!
    echo.
    echo Jalankan setup.bat terlebih dahulu untuk setup environment
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

REM Check .env
if not exist .env (
    echo [WARNING] File .env tidak ditemukan!
    echo Pastikan .env sudah dikonfigurasi dengan benar
    echo.
)

REM Check data folder
echo [*] Checking data folder...
if not exist data\rubrik.json (
    echo [ERROR] File data\rubrik.json tidak ditemukan!
    echo.
    pause
    exit /b 1
)

REM Count PDF files
set count=0
for %%f in (data\*.pdf) do set /a count+=1

if %count%==0 (
    echo [WARNING] Tidak ada file PDF di folder data\
    echo.
    echo Silakan copy file PDF yang akan dinilai ke folder data\
    echo.
    pause
    exit /b 1
)

echo [OK] Ditemukan %count% file PDF untuk diproses
echo.

REM Create output folder
if not exist output mkdir output

REM Run the grading system
echo [*] Starting RAG Auto-Grading System...
echo.
echo ============================================================
echo.

python rag_grading_improved.py

echo.
echo ============================================================
echo.

if %errorlevel%==0 (
    echo [OK] Grading completed successfully!
    echo.
    echo Results saved in output\ folder
    echo.
    choice /C YN /M "Apakah Anda ingin membuka folder output"
    if errorlevel 2 goto :end
    if errorlevel 1 explorer output\
) else (
    echo [ERROR] Grading process failed!
    echo Check rag_system.log for details
    echo.
    pause
)

:end
echo.
echo Thank you for using RAG Auto-Grading System!
echo.
