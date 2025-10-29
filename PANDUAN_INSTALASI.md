# 🚀 PANDUAN INSTALASI & TESTING
## RAG Auto-Grading System v2.0

---

## 📋 DAFTAR ISI

1. [Persiapan Environment](#1-persiapan-environment)
2. [Instalasi Dependencies](#2-instalasi-dependencies)
3. [Konfigurasi System](#3-konfigurasi-system)
4. [Testing Single PDF](#4-testing-single-pdf)
5. [Troubleshooting](#5-troubleshooting)

---

## ⚠️ ISSUE PENTING: Python Version

**Masalah yang terdeteksi:**
- Python 3.14.0 **BELUM KOMPATIBEL** dengan PyTorch dan transformers
- Error: `OSError: Error loading torch\lib\c10.dll`

**Solusi:** Gunakan Python 3.11 atau 3.12 (Recommended: **Python 3.12**)

---

## 1. PERSIAPAN ENVIRONMENT

### Opsi A: Install Python 3.12 (Recommended)

#### Windows:

**Step 1: Download Python 3.12**
```
1. Buka: https://www.python.org/downloads/
2. Download: Python 3.12.x (latest stable)
3. Saat install, CENTANG: "Add Python 3.12 to PATH"
4. Install di custom directory (contoh: C:\Python312)
```

**Step 2: Verifikasi Instalasi**
```bash
# Buka Command Prompt / PowerShell baru
py -3.12 --version
# Output: Python 3.12.x
```

**Step 3: Buat Virtual Environment**
```bash
# Masuk ke folder RAG
cd D:\RAG

# Buat virtual environment dengan Python 3.12
py -3.12 -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Verifikasi Python version di venv
python --version
# Output: Python 3.12.x
```

---

### Opsi B: Menggunakan Conda (Alternative)

```bash
# Install Miniconda/Anaconda jika belum ada
# Download dari: https://docs.conda.io/en/latest/miniconda.html

# Buat conda environment dengan Python 3.12



# Activate environment
conda activate rag-grading

# Verifikasi
python --version
# Output: Python 3.12.x
```

---

## 2. INSTALASI DEPENDENCIES

### Step 1: Upgrade pip

```bash
# Pastikan virtual environment sudah aktif
# Lihat prompt: (venv) atau (rag-grading)

python -m pip install --upgrade pip
```

### Step 2: Install Dependencies

```bash
# Install semua dependencies dari requirements.txt
pip install -r requirements.txt
```

**Proses ini akan install:**
- torch (PyTorch)
- sentence-transformers
- faiss-cpu
- langchain
- PyPDF2
- pandas, numpy, openpyxl
- requests
- python-dotenv
- dll.

**Estimasi waktu:** 5-10 menit (tergantung internet)

### Step 3: Verifikasi Instalasi

```bash
# Test import semua library utama
python -c "import torch; import sentence_transformers; import faiss; print('All imports successful!')"
```

**Output yang diharapkan:**
```
All imports successful!
```

**Jika ada error**, lihat section [Troubleshooting](#5-troubleshooting)

---

## 3. KONFIGURASI SYSTEM

### Step 1: Cek File .env

File `.env` sudah ada di `D:\RAG\.env` dengan konfigurasi:

```env
# OpenRouter API Configuration
OPENROUTER_KEY=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
OPENROUTER_URL=https://openrouter.ai/api/v1/chat/completions
MODEL=z-ai/glm-4.5

# RAG Configuration
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RETRIEVAL=5
SIMILARITY_THRESHOLD=0.65

# Logging
LOG_LEVEL=INFO
LOG_FILE=rag_system.log
```

**✅ File ini sudah benar, tidak perlu diubah!**

### Step 2: Verifikasi Struktur Folder

```
D:\RAG\
├── .env                          # ✅ Ada
├── rag_grading_improved.py       # ✅ Ada
├── requirements.txt              # ✅ Ada
├── data/
│   ├── rubrik.json              # ✅ Ada
│   └── LP 2 & 3_Kelompok 8.pdf  # ✅ Ada (sample)
├── output/                       # Akan dibuat otomatis
└── venv/                         # Virtual environment
```

**Jika folder `output` belum ada**, akan dibuat otomatis saat run.

---

## 4. TESTING SINGLE PDF

### Step 1: Activate Virtual Environment

```bash
# Pastikan di folder D:\RAG
cd D:\RAG

# Activate venv
venv\Scripts\activate

# Atau jika pakai conda:
# conda activate rag-grading
```

### Step 2: Test Run Pertama

```bash
python rag_grading_improved.py
```

### Step 3: Apa yang Akan Terjadi?

**1. Validasi Konfigurasi**
```
╔══════════════════════════════════════════════════════════╗
║     RAG AUTO-GRADING SYSTEM v2.0                        ║
║     Sistem Penilaian Otomatis Laporan Praktikum        ║
╚══════════════════════════════════════════════════════════╝

============================================================
KONFIGURASI SISTEM (dari .env)
============================================================
Model: z-ai/glm-4.5
Embedding Model: sentence-transformers/all-MiniLM-L6-v2
Chunk Size: 1000
Chunk Overlap: 200
Top-K Retrieval: 5
Similarity Threshold: 0.65
Log Level: INFO
Log File: rag_system.log
============================================================
```

**2. Processing PDF**
```
📂 Ditemukan 1 PDF untuk diproses

============================================================
📄 Processing: LP 2 & 3_Kelompok 8.pdf
============================================================
✅ Ekstraksi berhasil: 15 halaman
📝 Membuat embeddings untuk 23 chunks...
✅ Index berhasil dibuat dengan 23 vectors

🎯 Mulai proses grading...
🤖 Mengirim ke LLM untuk penilaian...
✅ Score: 74.5
   Confidence: 0.81
```

**3. Generate Reports**
```
📊 Generating Excel report...
✅ Excel report saved: output/grading_results_20251029_143000.xlsx

📄 Generating JSON report...
✅ JSON report saved: output/grading_results_20251029_143000.json

📊 SUMMARY STATISTICS
============================================================
Total Documents: 1
Scores:
  Mean:   74.50
  Median: 74.50
  ...
```

**4. Check Hasil**
```
✅ SELESAI!
============================================================
📁 Output folder: D:\RAG\output
📊 Excel report: grading_results_20251029_143000.xlsx
📄 JSON report: grading_results_20251029_143000.json

💡 Tip: Buka Excel report untuk melihat detail lengkap penilaian
```

### Step 4: Lihat Hasil

**A. Excel Report**
```bash
# Buka file Excel di folder output
explorer output\
```

Excel memiliki 2 sheets:
- **Sheet 1 (Summary)**: Overview nilai akhir
- **Sheet 2 (Detailed Scores)**: Detail per sub-rubrik dengan evidence

**B. JSON Report**
```bash
# Buka dengan text editor atau VS Code
code output\grading_results_*.json
```

**C. Log File**
```bash
# Lihat log lengkap proses
type rag_system.log
# atau
code rag_system.log
```

---

## 5. TROUBLESHOOTING

### ❌ Error: Python 3.14 DLL Loading

**Error Message:**
```
OSError: Error loading "torch\lib\c10.dll" or one of its dependencies
```

**Solusi:**
1. Install Python 3.12 (lihat [Opsi A](#opsi-a-install-python-312-recommended))
2. Buat virtual environment baru dengan Python 3.12
3. Install ulang dependencies

---

### ❌ Error: ModuleNotFoundError

**Error Message:**
```
ModuleNotFoundError: No module named 'dotenv'
```

**Solusi:**
```bash
# Pastikan venv aktif
pip install python-dotenv

# Atau install ulang semua
pip install -r requirements.txt
```

---

### ❌ Error: API Key Invalid

**Error Message:**
```
❌ OPENROUTER_KEY tidak ditemukan di .env file
```

**Solusi:**
1. Buka file `.env`
2. Pastikan ada baris: `OPENROUTER_KEY=sk-or-v1-...`
3. Pastikan tidak ada spasi sebelum/sesudah `=`
4. Save file

---

### ❌ Error: FAISS Import Failed

**Error Message:**
```
ImportError: DLL load failed while importing faiss
```

**Solusi:**
```bash
# Uninstall dan reinstall faiss
pip uninstall faiss-cpu
pip install faiss-cpu

# Atau gunakan conda (jika pakai conda):
conda install -c conda-forge faiss-cpu
```

---

### ❌ Error: PDF Extraction Failed

**Error Message:**
```
⚠️ Gagal ekstrak atau PDF kosong
```

**Possible Causes:**
1. PDF corrupt atau tidak bisa dibaca
2. PDF hasil scan (perlu OCR)

**Solusi untuk PDF Scan:**
```bash
# Install OCR library
pip install pytesseract pdf2image

# Install Tesseract-OCR
# Download dari: https://github.com/UB-Mannheim/tesseract/wiki
# Install dan tambahkan ke PATH
```

---

### ❌ Error: API Timeout

**Error Message:**
```
⚠️ Gagal memanggil LLM: timeout
```

**Solusi:**
1. Check koneksi internet
2. Dokumen terlalu besar, coba increase timeout di code
3. API OpenRouter sedang down, coba lagi nanti

---

### ❌ Error: Low Confidence Warnings

**Warning Message:**
```
⚠️ 1 dokumen dengan confidence rendah (<0.6):
   - LP_Kelompok_X: 0.550
```

**Ini bukan error!** Tapi warning untuk manual review.

**Penyebab:**
- Evidence kurang jelas
- Laporan tidak sesuai rubrik
- Perlu human verification

**Solusi:**
1. Review manual dokumen tersebut
2. Adjust `TOP_K_RETRIEVAL` di `.env` (increase ke 7-10)
3. Refine rubrik descriptions

---

## 6. TESTING DENGAN MULTIPLE PDFs

### Step 1: Tambah PDF ke Folder data/

```bash
# Copy lebih banyak PDF ke folder data
copy "C:\path\to\laporan*.pdf" data\
```

### Step 2: Run Batch Processing

```bash
python rag_grading_improved.py
```

**Output:**
```
📂 Ditemukan 5 PDF untuk diproses
Processing PDFs: 100%|██████████| 5/5 [02:30<00:00, 30.2s/it]
```

### Step 3: Review Hasil

Buka `output/grading_results_*.xlsx` untuk lihat semua hasil.

---

## 7. CUSTOMIZE KONFIGURASI

### Adjust Chunk Size

Edit `.env`:
```env
CHUNK_SIZE=1500       # Untuk laporan panjang
CHUNK_OVERLAP=300     # Overlap lebih besar
```

### Adjust Retrieval

Edit `.env`:
```env
TOP_K_RETRIEVAL=7     # Cari lebih banyak evidence
```

### Adjust Logging

Edit `.env`:
```env
LOG_LEVEL=DEBUG       # Untuk debugging detail
# atau
LOG_LEVEL=WARNING     # Untuk production (minimal log)
```

**Restart script setelah edit `.env`**

---

## 8. VERIFIKASI LENGKAP

### Checklist Sebelum Production

- [ ] Python 3.12 installed & verified
- [ ] Virtual environment created & activated
- [ ] All dependencies installed (`pip list`)
- [ ] `.env` file configured correctly
- [ ] Test dengan 1 PDF berhasil
- [ ] Excel report generated correctly
- [ ] Log file readable
- [ ] API key valid (check billing di OpenRouter)
- [ ] Test dengan multiple PDFs

---

## 9. ESTIMASI WAKTU & BIAYA

### Waktu Processing

| Jumlah PDF | Estimasi Waktu |
|------------|----------------|
| 1 dokumen  | ~30-45 detik   |
| 10 dokumen | ~5-7 menit     |
| 50 dokumen | ~25-35 menit   |
| 100 dokumen| ~50-75 menit   |

**Note:** Sequential processing. Bisa dipercepat dengan parallelization.

### Biaya API

| Item | Cost |
|------|------|
| Per dokumen | ~$0.008 |
| 100 dokumen | ~$0.80 |
| 1000 dokumen | ~$8.00 |

**Check billing di:** https://openrouter.ai/account

---

## 10. QUICK START COMMAND

```bash
# Setup (One-time)
cd D:\RAG
py -3.12 -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

# Every run
cd D:\RAG
venv\Scripts\activate
python rag_grading_improved.py

# Check hasil
explorer output\
```

---

## 📞 SUPPORT

**Jika masih error:**

1. Check log file: `rag_system.log`
2. Pastikan semua step di panduan sudah diikuti
3. Screenshot error message
4. Check Python version: `python --version`
5. Check installed packages: `pip list`

---

## 🎉 SELAMAT!

Jika sudah berhasil running, sistem RAG Auto-Grading Anda sudah siap digunakan!

**Next Steps:**
1. Test dengan lebih banyak PDF
2. Review accuracy dengan manual grading
3. Adjust konfigurasi sesuai kebutuhan
4. Deploy ke production environment

---

**Document Version**: 1.0
**Last Updated**: 2025-10-29
**Tested On**: Python 3.12, Windows 11
