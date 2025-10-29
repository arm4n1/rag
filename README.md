# 🎓 RAG Auto-Grading System v2.0

Sistem penilaian otomatis untuk laporan praktikum menggunakan **Retrieval-Augmented Generation (RAG)** dan **Large Language Models (LLM)**.

## 📋 Fitur Utama

### ✅ Version 1.0 (GLM_RAG.ipynb)
- Single PDF processing
- RAG dengan FAISS vector database
- Grading berbasis rubrik JSON
- Evidence-based scoring
- Confidence scoring

### 🚀 Version 2.0 (rag_grading_improved.py) - **NEW!**
- ✨ **Batch Processing**: Proses multiple PDF sekaligus
- 📊 **Excel Export**: Laporan detail dengan multiple sheets
- 📈 **Statistical Analysis**: Mean, median, std, distribution
- 🎯 **Enhanced RAG**: Multi-query retrieval per sub-rubrik
- 📦 **Metadata Extraction**: Auto-extract kelompok, NIM, nama
- 🔍 **Quality Assurance**: Low confidence flagging
- 💾 **Multiple Output Formats**: Excel, JSON
- 🏗️ **Modular Architecture**: Clean, maintainable code
- 🔧 **Configuration via .env**: Konfigurasi terpisah dari code
- 📝 **Comprehensive Logging**: Track semua proses dengan detail

### 🌐 Web Interface (streamlit_app.py) - **NEW!**
- 🖥️ **User-Friendly UI**: Interface web interaktif
- 📤 **Drag & Drop Upload**: Upload multiple PDFs sekaligus
- 📊 **Interactive Visualizations**: Charts dengan Plotly
- 📈 **Evaluation Dashboard**: Compare AI vs Human grading
- 💾 **Easy Export**: Excel, JSON, CSV dengan 1-click
- 🎯 **Real-time Monitoring**: Progress tracking dan statistics
- ⚙️ **Dynamic Configuration**: Adjust settings via sidebar

---

## ⚡ QUICK START

### PENTING: Python Version Requirement

❌ **Python 3.14** - Tidak kompatibel dengan PyTorch
✅ **Python 3.12** - **RECOMMENDED**

### Setup Otomatis (Windows)

```bash
# 1. Download dan install Python 3.12 dari python.org
# 2. Double-click setup.bat
# 3. Tunggu hingga instalasi selesai
# 4a. Double-click run.bat untuk command-line
# 4b. Double-click run_streamlit.bat untuk web interface
```

### Setup Manual

**Command-Line Interface:**
```bash
# 1. Buat virtual environment dengan Python 3.12
conda create -n rag-grading python=3.12
conda activate rag-grading

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run program
python rag_grading_improved.py
```

**Web Interface (RECOMMENDED):**
```bash
# 1. Activate environment
conda activate rag-grading

# 2. Install web dependencies (if not already)
pip install streamlit plotly

# 3. Run Streamlit app
streamlit run streamlit_app.py

# 4. Open browser to http://localhost:8501
```

### 📚 Dokumentasi Lengkap

**Setup & Installation:**
- **Panduan Detail**: [PANDUAN_INSTALASI.md](PANDUAN_INSTALASI.md)
- **Quick Reference**: [QUICK_START.md](QUICK_START.md)
- **Rencana Implementasi**: [RENCANA_IMPLEMENTASI.md](RENCANA_IMPLEMENTASI.md)

**Web Interface:**
- **Streamlit Guide**: [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md) - Comprehensive guide
- **Quick Reference**: [STREAMLIT_QUICK_REFERENCE.md](STREAMLIT_QUICK_REFERENCE.md) - Cheat sheet

**Evaluation:**
- **Metrik Evaluasi**: [METRIK_EVALUASI.md](METRIK_EVALUASI.md) - RAG-specific metrics

---

## 🏗️ Arsitektur Sistem

```
┌─────────────────────────────────────────────────────────┐
│                    INPUT LAYER                          │
│  • Multiple PDF Reports (batch)                         │
│  • Rubrik JSON dengan weights                           │
│  • Configuration                                        │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              PREPROCESSING LAYER                        │
│  • PDF Text Extraction (PyPDF2)                        │
│  • Metadata extraction (kelompok, NIM)                 │
│  • Smart chunking dengan overlap                       │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  RAG LAYER                              │
│  • FAISS Vector Database                               │
│  • Sentence Transformers (all-MiniLM-L6-v2)           │
│  • Multi-query retrieval per sub-rubrik               │
│  • Top-K evidence extraction                           │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│               GRADING ENGINE                            │
│  • GLM-4.5 via OpenRouter API                          │
│  • Evidence-based scoring                              │
│  • JSON structured output                              │
│  • Confidence scoring                                  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│          POST-PROCESSING & REPORTING                    │
│  • Weighted score calculation                          │
│  • Statistical analysis                                │
│  • Excel report generation                             │
│  • JSON export                                         │
│  • Quality assurance checks                            │
└─────────────────────────────────────────────────────────┘
```

## 📂 Struktur Project

```
D:\RAG\
├── data/
│   ├── LP 2 & 3_Kelompok 8.pdf        # Sample PDF
│   ├── [PDF laporan lainnya...]
│   └── rubrik.json                    # Rubrik penilaian
│
├── output/                            # Generated reports
│   ├── grading_results_YYYYMMDD_HHMMSS.xlsx
│   ├── grading_results_YYYYMMDD_HHMMSS.json
│   └── [older reports...]
│
├── GLM_RAG.ipynb                      # Version 1.0 (original)
├── rag_grading_improved.py            # Version 2.0 (improved)
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Your Data

**Struktur Folder:**
```
data/
├── rubrik.json               # Rubrik penilaian Anda
├── Laporan_Kelompok_1.pdf
├── Laporan_Kelompok_2.pdf
└── [PDF laporan lainnya...]
```

**Format Rubrik (JSON):**
```json
{
  "rubric": {
    "name": "Rubrik Penilaian",
    "course": "Mata Kuliah",
    "description": "Deskripsi rubrik"
  },
  "sub_rubrics": [
    {
      "id": "UUID-SUB1",
      "name": "Dasar Teori",
      "description": "Mengukur pemahaman teori",
      "levels": [
        {
          "label": "A",
          "description": "Sangat baik",
          "score_range": [81, 100]
        },
        ...
      ]
    },
    ...
  ],
  "assignment_sub_rubrics": [
    {
      "sub_rubric_id": "UUID-SUB1",
      "weight": 25
    },
    ...
  ]
}
```

### 3. Run Version 1.0 (Single PDF)

```bash
jupyter notebook GLM_RAG.ipynb
```

Atau jalankan cell by cell untuk memproses 1 PDF.

### 4. Run Version 2.0 (Batch Processing)

```bash
python rag_grading_improved.py
```

Ini akan:
- ✅ Memproses semua PDF di folder `data/`
- ✅ Generate Excel report dengan 2 sheets (Summary + Detail)
- ✅ Generate JSON report
- ✅ Print statistik summary

## 📊 Output Reports

### Excel Report (Sheet 1: Summary)

| Filename | Kelompok | Final Score | Confidence | Page Count | Processed At |
|----------|----------|-------------|------------|------------|--------------|
| LP_Kel_8 | Kelompok 8 | 74.0 | 0.81 | 15 | 2025-10-29T10:30:00 |

### Excel Report (Sheet 2: Detailed Scores)

| Filename | Sub Rubric | Level | Score | Weight | Confidence | Reason | Evidence Quote |
|----------|------------|-------|-------|--------|------------|--------|----------------|
| LP_Kel_8 | Dasar Teori | A | 90 | 10 | 0.9 | Teori jelas... | "Variabel merupakan..." |
| LP_Kel_8 | Kode Program | B | 70 | 50 | 0.7 | Program kurang... | "Fungsi input()..." |

### JSON Report

```json
[
  {
    "grading_result": [
      {
        "sub_rubric": "Dasar Teori",
        "selected_level": "A",
        "score_awarded": 90,
        "weight": 10,
        "reason": "Dasar teori dikemukakan dengan jelas...",
        "evidence_quote": "Variabel merupakan...",
        "confidence": 0.9
      },
      ...
    ],
    "final_score": 74.0,
    "overall_confidence": 0.81,
    "document_info": {
      "filename": "LP 2 & 3_Kelompok 8",
      "page_count": 15,
      "metadata": {
        "kelompok": "Kelompok 8"
      },
      "processed_at": "2025-10-29T10:30:00"
    }
  }
]
```

## 🔧 Konfigurasi

Edit bagian `Config` di `rag_grading_improved.py`:

```python
class Config:
    # OpenRouter API
    OPENROUTER_KEY = "your-api-key-here"
    MODEL = "z-ai/glm-4.5"

    # RAG Settings
    CHUNK_SIZE = 1000          # Ukuran chunk
    CHUNK_OVERLAP = 200        # Overlap antar chunk
    TOP_K_RETRIEVAL = 5        # Jumlah evidence chunks

    # Grading Settings
    MIN_CONFIDENCE_THRESHOLD = 0.6  # Threshold warning
    TEMPERATURE = 0.0          # LLM temperature

    # Paths
    DATA_FOLDER = "data"
    OUTPUT_FOLDER = "output"
    RUBRIC_FILE = "data/rubrik.json"
```

## 🎯 Rubrik Penilaian

Sistem ini menggunakan rubrik dengan struktur:

### Sub-Rubrik yang Dinilai:
1. **Dasar Teori** (Weight: 10%)
   - A (81-100): Teori jelas dan informatif
   - B (61-80): Teori kurang jelas
   - C (0-60): Teori tidak jelas

2. **Kode Program** (Weight: 50%)
   - A (81-100): Program efisien, variabel informatif
   - B (61-80): Program kurang efisien
   - C (0-60): Program tidak efisien

3. **Keterangan Baris Program** (Weight: 20%)
   - A (81-100): Semua baris dijelaskan
   - B (61-80): Penjelasan kurang informatif
   - C (0-60): Tidak ada penjelasan

4. **Kesimpulan** (Weight: 20%)
   - A (81-100): Kesimpulan jelas dan sesuai
   - B (61-80): Kesimpulan kurang jelas
   - C (0-60): Kesimpulan tidak dapat dipahami

### Perhitungan Nilai Akhir:

```
Final Score = Σ (score_i × weight_i / 100)
```

Contoh:
- Dasar Teori: 90 × 10% = 9
- Kode Program: 70 × 50% = 35
- Keterangan: 75 × 20% = 15
- Kesimpulan: 75 × 20% = 15
- **Total: 74**

## 🧪 Example Usage

### Simulasi 1: Single PDF (Version 1.0)

```python
# Di Jupyter Notebook (GLM_RAG.ipynb)
rubric_file = "data/rubrik.json"
pdf_file = "data/LP 2 & 3_Kelompok 8.pdf"

# Load & extract
rubric_json = load_rubric_json(rubric_file)
pdf_text = extract_text_from_pdf(pdf_file)

# Build RAG
vectordb = SimpleVectorDB()
vectordb.build(chunk_text(pdf_text))

# Grade
evidence = vectordb.search("Evaluasi laporan sesuai rubrik", k=5)
prompt = build_prompt_with_rag(rubric_json, "\n\n".join(evidence))
result = call_glm(prompt)

print(result)  # JSON output
```

### Simulasi 2: Batch Processing (Version 2.0)

```python
# Run script
python rag_grading_improved.py

# Output:
# ╔══════════════════════════════════════════════════════════╗
# ║     RAG AUTO-GRADING SYSTEM v2.0                        ║
# ╚══════════════════════════════════════════════════════════╝
#
# 📂 Ditemukan 5 PDF untuk diproses
# Processing PDFs: 100%|██████████| 5/5 [02:30<00:00, 30.2s/it]
#
# 📊 SUMMARY STATISTICS
# Total Documents: 5
# Scores:
#   Mean:   76.80
#   Median: 78.00
#   Std:    8.45
#
# ✅ SELESAI!
# 📊 Excel report: grading_results_20251029_103045.xlsx
```

## 🔍 Advanced Features

### 1. Multi-Query Retrieval

System uses multiple queries per sub-rubrik untuk coverage lebih baik:

```python
queries = [
    "Cari bagian tentang Dasar Teori",
    "Mengukur pemahaman teori dasar",
    "Evidence untuk menilai Dasar Teori"
]
evidence = rag_engine.search_multi_query(queries, k=3)
```

### 2. Confidence Scoring

Setiap penilaian dilengkapi confidence score (0-1):
- **>0.8**: High confidence - penilaian reliable
- **0.6-0.8**: Medium confidence - reasonable
- **<0.6**: Low confidence - perlu manual review

### 3. Quality Assurance

System otomatis flag dokumen dengan confidence rendah:
```
⚠️ 2 dokumen dengan confidence rendah (<0.6):
   - Laporan_Kelompok_5: 0.550
   - Laporan_Kelompok_9: 0.480
```

### 4. Evidence Transparency

Setiap penilaian disertai evidence quote dari dokumen:
```json
{
  "evidence_quote": "Variabel merupakan suatu tempat yang tersedia di memori komputer..."
}
```

## 📈 Performance Tips

1. **Chunk Size**: Sesuaikan `CHUNK_SIZE` berdasarkan panjang laporan
   - Laporan pendek (<10 halaman): 500-800
   - Laporan medium (10-20 halaman): 1000-1500
   - Laporan panjang (>20 halaman): 1500-2000

2. **Top-K Retrieval**: Sesuaikan `TOP_K_RETRIEVAL`
   - Minimal: 3 (cepat tapi evidence kurang)
   - Optimal: 5-7 (balance)
   - Maksimal: 10+ (comprehensive tapi lambat)

3. **Batch Size**: Proses PDF dalam batches untuk memory efficiency

4. **API Rate Limiting**: Tambahkan delay antar request jika rate limited

## 🐛 Troubleshooting

### Issue: PDF kosong / tidak bisa ekstrak

**Solution**: Kemungkinan PDF hasil scan. Gunakan OCR:
```python
# Install: pip install pytesseract
import pytesseract
from PIL import Image
import pdf2image

# Convert PDF to images then OCR
images = pdf2image.convert_from_path(pdf_path)
text = "\n".join([pytesseract.image_to_string(img) for img in images])
```

### Issue: Low confidence scores

**Causes**:
- Evidence tidak cukup relevan
- Rubrik terlalu subjektif
- Laporan tidak memenuhi kriteria

**Solutions**:
- Increase `TOP_K_RETRIEVAL` untuk more evidence
- Refine multi-query untuk better coverage
- Review rubrik untuk clarity

### Issue: API timeout

**Solution**:
```python
# Increase timeout
r = requests.post(..., timeout=180)  # 3 minutes

# Add retry logic
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def call_llm_with_retry(prompt):
    return call_llm(prompt)
```

## 📚 Tech Stack

- **LLM**: GLM-4.5 via OpenRouter
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector DB**: FAISS
- **PDF Processing**: PyPDF2
- **Text Splitting**: LangChain
- **Data Processing**: Pandas, NumPy
- **Excel Export**: OpenPyXL

## 🤝 Contributing

Contributions welcome! Areas untuk improvement:
- [ ] Support untuk OCR (scan PDFs)
- [ ] PDF report generation per student
- [ ] Interactive dashboard (Streamlit/Gradio)
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] API endpoint (FastAPI)
- [ ] Evaluation metrics (BLEU, ROUGE for grading quality)
- [ ] Multi-language support

## 📄 License

MIT License - feel free to use untuk educational purposes

## 📞 Support

Untuk pertanyaan atau issues:
- GitHub Issues
- Email: [your-email]

---

**Built with ❤️ for automated grading**
