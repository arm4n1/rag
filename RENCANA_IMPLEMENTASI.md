# RENCANA IMPLEMENTASI: Sistem RAG Auto-Grading

## 📋 RINGKASAN EKSEKUTIF

Dokumen ini berisi rencana lengkap implementasi sistem RAG (Retrieval-Augmented Generation) untuk auto-grading laporan praktikum. Sistem ini menggunakan AI untuk memberikan penilaian objektif dan konsisten berdasarkan rubrik yang telah ditentukan.

---

## 🎯 TUJUAN SISTEM

1. **Automatisasi Penilaian**: Mengurangi waktu dosen dalam menilai laporan
2. **Konsistensi**: Penilaian yang objektif dan konsisten antar mahasiswa
3. **Transparansi**: Setiap nilai disertai alasan dan evidence dari dokumen
4. **Skalabilitas**: Mampu memproses puluhan hingga ratusan laporan sekaligus
5. **Feedback Berkualitas**: Memberikan feedback spesifik untuk setiap aspek penilaian

---

## 📊 ARSITEKTUR SISTEM

### Diagram Arsitektur

```
┌─────────────────────────────────────────────────────────┐
│                    INPUT LAYER                          │
│  • PDF Reports (folder batch)                          │
│  • Rubrik JSON dengan weighted criteria                │
│  • Configuration (model, API keys, thresholds)         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              PREPROCESSING LAYER                        │
│  • PDF Text Extraction                                 │
│  • Text Cleaning & Normalization                       │
│  • Metadata Extraction (kelompok, NIM, nama)          │
│  • Smart Chunking (1000 chars, 200 overlap)           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  RAG LAYER                              │
│  • Sentence Transformers (all-MiniLM-L6-v2)           │
│  • FAISS Vector Database                               │
│  • Multi-query Retrieval (per sub-rubrik)             │
│  • Evidence Ranking & Filtering                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│               GRADING ENGINE                            │
│  • LLM: GLM-4.5 via OpenRouter                         │
│  • Evidence-based Prompt Engineering                   │
│  • JSON Structured Output                              │
│  • Confidence Scoring                                  │
│  • Retry Mechanism & Error Handling                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│          POST-PROCESSING & REPORTING                    │
│  • Weighted Score Calculation                          │
│  • Statistical Analysis                                │
│  • Excel Export (2 sheets: Summary + Detail)          │
│  • JSON Export (raw data)                              │
│  • Quality Assurance Checks                            │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 KOMPONEN SISTEM

### 1. PDF Extractor Module
**File**: `rag_grading_improved.py` (class `PDFExtractor`)

**Fungsi:**
- Ekstraksi teks dari PDF menggunakan PyPDF2
- Auto-deteksi metadata (kelompok, NIM, nama)
- Handling untuk PDF scan (OCR capability - optional)

**Input**: Path ke file PDF
**Output**: Dict dengan `text`, `metadata`, `page_count`

---

### 2. RAG Engine Module
**File**: `rag_grading_improved.py` (class `RAGEngine`)

**Fungsi:**
- Chunking teks dengan RecursiveCharacterTextSplitter
- Embedding generation dengan Sentence Transformers
- Build FAISS index untuk similarity search
- Multi-query retrieval untuk comprehensive evidence

**Konfigurasi:**
```python
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K_RETRIEVAL = 5
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
```

---

### 3. Grading Engine Module
**File**: `rag_grading_improved.py` (class `GradingEngine`)

**Fungsi:**
- Build prompt dengan rubrik dan evidence
- Call LLM (GLM-4.5) via OpenRouter API
- Parse dan validate JSON response
- Calculate weighted scores

**Prompt Strategy:**
- Evidence-based grading (no hallucination)
- Structured JSON output
- Per-criterion evaluation
- Confidence scoring
- Reasoning explanation

---

### 4. Batch Processor Module
**File**: `rag_grading_improved.py` (class `BatchProcessor`)

**Fungsi:**
- Process multiple PDFs in sequence
- Progress tracking dengan tqdm
- Error handling per document
- Aggregate results

**Performance:**
- ~30-45 detik per dokumen (tergantung panjang)
- Sequential processing (bisa di-parallelkan untuk improvement)

---

### 5. Report Generator Module
**File**: `rag_grading_improved.py` (class `ReportGenerator`)

**Fungsi:**
- Generate Excel report (2 sheets)
- Generate JSON report
- Print statistical summary
- Flag low-confidence documents

**Output Formats:**
1. **Excel**: `grading_results_YYYYMMDD_HHMMSS.xlsx`
   - Sheet 1: Summary (semua mahasiswa)
   - Sheet 2: Detailed scores (per sub-rubrik)

2. **JSON**: `grading_results_YYYYMMDD_HHMMSS.json`
   - Raw data untuk integrasi sistem lain

---

## 📝 RUBRIK PENILAIAN

### Struktur Rubrik JSON

```json
{
  "rubric": {
    "name": "Rubrik Penilaian Algoritma Pemrograman",
    "course": "Algoritma dan Pemrograman",
    "description": "Rubrik untuk menilai tugas laporan ALPRO"
  },
  "sub_rubrics": [
    {
      "id": "UUID-SUB1",
      "name": "Dasar Teori",
      "description": "Mengukur pemahaman teori dasar",
      "levels": [
        {
          "label": "A",
          "description": "Dasar teori dikemukakan dengan jelas dan dapat dimengerti",
          "score_range": [81, 100]
        },
        {
          "label": "B",
          "description": "Dasar teori dikemukakan dengan kurang jelas",
          "score_range": [61, 80]
        },
        {
          "label": "C",
          "description": "Dasar teori dikemukakan dengan tidak jelas",
          "score_range": [0, 60]
        }
      ]
    }
  ],
  "assignment_sub_rubrics": [
    {
      "sub_rubric_id": "UUID-SUB1",
      "weight": 10
    }
  ]
}
```

### Sub-Rubrik yang Dinilai

| No | Sub-Rubrik | Weight | Kriteria A (81-100) | Kriteria B (61-80) | Kriteria C (0-60) |
|----|------------|--------|---------------------|-------------------|-------------------|
| 1 | Dasar Teori | 10% | Jelas dan informatif | Kurang jelas | Tidak jelas |
| 2 | Kode Program | 50% | Efisien, variabel informatif | Kurang efisien | Tidak efisien |
| 3 | Keterangan Baris | 20% | Semua baris dijelaskan | Kurang informatif | Tidak ada penjelasan |
| 4 | Kesimpulan | 20% | Jelas dan sesuai | Kurang jelas | Tidak dapat dipahami |

### Formula Perhitungan

```
Final Score = Σ (score_i × weight_i / 100)

Contoh:
- Dasar Teori:    90 × 10% = 9.0
- Kode Program:   70 × 50% = 35.0
- Keterangan:     85 × 20% = 17.0
- Kesimpulan:     75 × 20% = 15.0
---------------------------------
Total:                    76.0
```

---

## 🚀 LANGKAH IMPLEMENTASI

### Phase 1: Setup & Persiapan (1-2 hari)

**1.1 Install Dependencies**
```bash
pip install -r requirements.txt
```

**Dependencies:**
- torch, sentence-transformers, transformers
- faiss-cpu
- langchain, langchain-text-splitters
- PyPDF2
- pandas, numpy, openpyxl
- requests, tqdm

**1.2 Setup API Key**
- Daftar di OpenRouter: https://openrouter.ai/
- Dapatkan API key
- Update di `rag_grading_improved.py`:
  ```python
  OPENROUTER_KEY = "sk-or-v1-your-key-here"
  ```

**1.3 Persiapan Data**
- Siapkan folder `data/` dengan PDF laporan
- Pastikan `rubrik.json` sudah sesuai dengan kriteria penilaian
- Create folder `output/` untuk hasil

---

### Phase 2: Testing & Validation (2-3 hari)

**2.1 Single Document Test**
```bash
# Jalankan version 1.0 untuk test single PDF
jupyter notebook GLM_RAG.ipynb
```

**2.2 Rubrik Validation**
- Verifikasi struktur JSON rubrik
- Test dengan 1-2 dokumen sample
- Compare dengan manual grading

**2.3 Confidence Tuning**
- Adjust `MIN_CONFIDENCE_THRESHOLD`
- Evaluate evidence quality
- Fine-tune `TOP_K_RETRIEVAL`

---

### Phase 3: Batch Processing (1 hari)

**3.1 Run Batch Grading**
```bash
python rag_grading_improved.py
```

**3.2 Monitor Progress**
- Check console output
- Verify FAISS index building
- Monitor API calls

**3.3 Review Results**
- Open Excel report
- Check score distribution
- Flag low-confidence documents

---

### Phase 4: Quality Assurance (2-3 hari)

**4.1 Manual Review**
- Review flagged documents (confidence < 0.6)
- Compare AI grading vs human grading
- Calculate agreement metrics (correlation, MAE)

**4.2 Iteration**
- Adjust prompts if needed
- Refine rubrik descriptions
- Update chunk size / TOP_K

**4.3 Documentation**
- Document any adjustments
- Create user guide for dosen
- Prepare feedback template

---

### Phase 5: Deployment & Scaling (ongoing)

**5.1 Production Setup**
- Setup scheduled batch processing
- Create backup mechanism
- Implement logging

**5.2 Integration**
- API untuk integrasi dengan LMS
- Database untuk historical tracking
- Dashboard untuk monitoring

---

## 📈 EVALUASI & METRICS

### Performance Metrics

1. **Speed**
   - Target: < 45 detik per dokumen
   - Actual: (to be measured)

2. **Accuracy**
   - Agreement dengan human grader: target > 80%
   - Mean Absolute Error: target < 10 points

3. **Reliability**
   - Consistency: Std Dev < 5 untuk multiple runs
   - Confidence: Mean confidence > 0.75

### Quality Assurance Checklist

- [ ] All sub-rubrik evaluated
- [ ] Scores within valid ranges
- [ ] Evidence quotes present
- [ ] Confidence scores calculated
- [ ] Weighted calculation correct
- [ ] JSON structure valid
- [ ] Excel report readable
- [ ] Low confidence flagged

---

## 🔮 FUTURE ENHANCEMENTS

### Priority 1 (Next Sprint)
1. **OCR Support**: Handle scanned PDFs
2. **Parallel Processing**: Speed up batch processing
3. **PDF Report Generation**: Auto-generate feedback report per student
4. **Confidence Threshold Tuning**: Adaptive thresholding

### Priority 2 (Future)
1. **Web Dashboard**: Interactive Streamlit/Gradio UI
2. **Database Integration**: PostgreSQL/MongoDB for history
3. **API Endpoint**: FastAPI untuk integrasi LMS
4. **Multi-language Support**: Support English reports

### Priority 3 (Research)
1. **Fine-tuning**: Custom model training on grading data
2. **Active Learning**: Incorporate human feedback
3. **Explainability**: Better visualization of evidence
4. **Comparative Grading**: Relative ranking within class

---

## 💰 ESTIMASI BIAYA

### OpenRouter API Costs
- Model: GLM-4.5
- Cost: ~$0.002 per 1K tokens
- Average tokens per grading: ~4,000 tokens (prompt + response)
- **Cost per document: ~$0.008**

### Untuk 100 dokumen
- API cost: $0.80
- Time: ~60-75 menit (dengan sequential processing)

### Untuk 1000 dokumen
- API cost: $8.00
- Time: ~10-12 jam

**Note**: Bisa lebih murah dengan batch API calls atau alternative models

---

## 🛠️ TROUBLESHOOTING

### Issue 1: PDF Extraction Gagal
**Symptom**: Empty text atau garbled characters
**Cause**: PDF hasil scan atau encrypted
**Solution**:
```python
# Install OCR
pip install pytesseract pdf2image
# Implement OCR fallback
```

### Issue 2: Low Confidence Scores
**Symptom**: Overall confidence < 0.6
**Cause**: Evidence tidak cukup atau rubrik ambiguous
**Solution**:
- Increase `TOP_K_RETRIEVAL` dari 5 ke 7-10
- Refine multi-query untuk better coverage
- Clarify rubrik descriptions

### Issue 3: API Timeout
**Symptom**: Request timeout errors
**Cause**: Large documents atau network issues
**Solution**:
```python
# Increase timeout
timeout=180  # 3 minutes
# Add retry logic
@retry(stop=stop_after_attempt(3))
```

### Issue 4: Inconsistent Scores
**Symptom**: Same document graded differently
**Cause**: Temperature > 0 or non-deterministic retrieval
**Solution**:
```python
TEMPERATURE = 0.0  # Ensure deterministic
# Fix random seed for FAISS
```

---

## 📚 REFERENSI

### Teknologi
- **RAG**: Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
- **FAISS**: Facebook AI Similarity Search
- **Sentence Transformers**: Reimers & Gurevych, "Sentence-BERT"

### Best Practices
- Prompt engineering untuk grading tasks
- Evidence-based AI assessment
- Confidence calibration
- Human-in-the-loop validation

---

## ✅ CHECKLIST IMPLEMENTASI

### Setup
- [x] Requirements.txt created
- [x] Config file prepared
- [ ] API key configured
- [x] Folder structure created
- [x] Demo simulation tested

### Development
- [x] PDF extractor implemented
- [x] RAG engine implemented
- [x] Grading engine implemented
- [x] Batch processor implemented
- [x] Report generator implemented

### Testing
- [ ] Single document test passed
- [ ] Rubrik validation done
- [ ] Batch processing tested
- [ ] Quality assurance done
- [ ] Manual review comparison

### Documentation
- [x] README created
- [x] Implementation plan created
- [x] User guide prepared
- [ ] API documentation (if applicable)

### Deployment
- [ ] Production environment setup
- [ ] Monitoring configured
- [ ] Backup mechanism in place
- [ ] User training completed

---

## 📞 KONTAK & SUPPORT

Untuk pertanyaan teknis atau issue:
1. Check README.md
2. Review TROUBLESHOOTING section
3. Contact: [your-contact-info]

---

**Document Version**: 1.0
**Last Updated**: 2025-10-29
**Status**: Ready for Implementation

---

## 🎉 KESIMPULAN

Sistem RAG Auto-Grading ini menyediakan solusi end-to-end untuk automatic grading laporan praktikum dengan:

✅ **Objective & Consistent** grading berdasarkan rubrik
✅ **Scalable** untuk batch processing
✅ **Transparent** dengan evidence dan reasoning
✅ **Cost-effective** (~$0.008 per document)
✅ **Comprehensive** reporting (Excel + JSON)

**Next Steps**: Setup API key → Test dengan sample documents → Run batch processing → Review & iterate

---

**Ready to implement!** 🚀
