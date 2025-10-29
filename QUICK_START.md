# ⚡ QUICK START GUIDE
## RAG Auto-Grading System v2.0

---

## 🚨 IMPORTANT: Python Version

❌ **Python 3.14** - TIDAK KOMPATIBEL
✅ **Python 3.12** - RECOMMENDED

---

## 📦 SETUP (One-Time)

```bash
# 1. Install Python 3.12 dari python.org

# 2. Buat Virtual Environment
cd D:\RAG
py -3.12 -m venv venv
venv\Scripts\activate

# 3. Install Dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Verify
python -c "import torch, sentence_transformers, faiss; print('OK!')"
```

---

## ▶️ RUN PROGRAM

```bash
# Activate environment
cd D:\RAG
venv\Scripts\activate

# Run grading
python rag_grading_improved.py

# Lihat hasil
explorer output\
```

---

## 📊 OUTPUT

**3 File yang dihasilkan:**

1. `output/grading_results_YYYYMMDD_HHMMSS.xlsx`
   - Sheet 1: Summary (nilai akhir)
   - Sheet 2: Detailed (per sub-rubrik)

2. `output/grading_results_YYYYMMDD_HHMMSS.json`
   - Raw data JSON

3. `rag_system.log`
   - Log lengkap proses

---

## ⚙️ KONFIGURASI (.env)

```env
# Model
MODEL=z-ai/glm-4.5
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# RAG Settings
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_RETRIEVAL=5

# Logging
LOG_LEVEL=INFO
LOG_FILE=rag_system.log
```

**Edit `.env` untuk customize, lalu restart program**

---

## 🔧 COMMON ISSUES

### DLL Error (Python 3.14)
```bash
# Install Python 3.12, buat venv baru
py -3.12 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Module Not Found
```bash
pip install -r requirements.txt
```

### API Key Error
```bash
# Check .env file
# Pastikan: OPENROUTER_KEY=sk-or-v1-...
```

### Low Confidence
```bash
# Edit .env:
TOP_K_RETRIEVAL=7  # increase dari 5 ke 7-10
```

---

## 📈 PERFORMANCE

| PDF Count | Time | Cost |
|-----------|------|------|
| 1 doc | ~35s | $0.008 |
| 10 docs | ~6min | $0.08 |
| 100 docs | ~60min | $0.80 |

---

## 🎯 TESTING WORKFLOW

```bash
# 1. Activate
venv\Scripts\activate

# 2. Put PDFs in data/
copy "C:\path\*.pdf" data\

# 3. Run
python rag_grading_improved.py

# 4. Check output/
explorer output\

# 5. Review log
type rag_system.log
```

---

## 📁 FOLDER STRUCTURE

```
D:\RAG\
├── .env                    # Configuration
├── rag_grading_improved.py # Main script
├── data/
│   ├── rubrik.json        # Grading rubric
│   └── *.pdf              # Reports to grade
├── output/                 # Results (auto-created)
│   ├── *.xlsx
│   └── *.json
└── venv/                   # Virtual environment
```

---

## 🆘 HELP

**Full documentation:** `PANDUAN_INSTALASI.md`

**Check:**
- Python version: `python --version`
- Installed packages: `pip list`
- Log file: `type rag_system.log`

---

## ✅ CHECKLIST

- [ ] Python 3.12 installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] `.env` configured
- [ ] Test 1 PDF successful
- [ ] Excel report generated
- [ ] Ready for production!

---

**Quick Help:** See `PANDUAN_INSTALASI.md` for detailed guide
