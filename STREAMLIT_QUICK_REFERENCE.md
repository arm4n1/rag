# ⚡ STREAMLIT APP - QUICK REFERENCE

---

## 🚀 LAUNCH APP

```bash
# Option 1: Double-click
run_streamlit.bat

# Option 2: Command line
conda activate rag-grading
streamlit run streamlit_app.py
```

**URL:** http://localhost:8501

---

## 📱 PAGES

| Page | Purpose | Key Features |
|------|---------|--------------|
| 🏠 Home | Overview | Stats, Quick Start |
| 📄 Grading | Process PDFs | Upload, Batch Process |
| 📊 Results | View Results | Tables, Charts, Export |
| 📈 Evaluation | Compare AI vs Human | Metrics, Visualizations |

---

## 🎯 COMMON TASKS

### Grade New Documents
```
1. 📄 Grading → Upload files
2. Click "Start Grading"
3. 📊 Results → View scores
4. Export → Download Excel
```

### Batch Process
```
1. Copy PDFs to data/
2. 📄 Grading → Batch tab
3. Click "Process All PDFs"
4. 📊 Results → Analyze
```

### Evaluate Accuracy
```
1. 📄 Grade with AI
2. 📈 Evaluation → Upload human results
3. View metrics
4. Download report
```

---

## 📊 KEY METRICS

| Metric | Good Value | Excellent | Meaning |
|--------|------------|-----------|---------|
| MAE | < 10 | < 5 | Avg error in points |
| Pearson r | > 0.75 | > 0.85 | Correlation AI-Human |
| Cohen's κ | > 0.6 | > 0.8 | Inter-rater agreement |
| Within ±5 | > 65% | > 80% | Acceptable tolerance |

---

## 🎨 VISUALIZATIONS

### Available Charts
- 📊 Score Distribution (histogram)
- 📈 Confidence Distribution (histogram)
- 📉 Scores by Document (bar chart)
- 📦 Score by Sub-Rubric (box plot)
- 🎯 Score vs Confidence (scatter)
- 📐 AI vs Human (scatter + trendline)
- 📊 Error Distribution (histogram)
- 🔬 Bland-Altman Plot

### Interactions
- **Hover**: View details
- **Zoom**: Drag to select area
- **Pan**: Click and drag
- **Download**: Click camera icon

---

## 💾 EXPORT OPTIONS

| Format | Content | Use Case |
|--------|---------|----------|
| Excel | Summary + Detailed | Reporting to management |
| JSON | Raw data | System integration |
| CSV | Summary table | Quick analysis in Excel |

---

## ⚙️ SETTINGS (Sidebar)

| Setting | Range | Default | Impact |
|---------|-------|---------|--------|
| Chunk Size | 500-2000 | 1000 | Retrieval granularity |
| Top-K | 3-15 | 5 | Evidence chunks |
| Confidence Threshold | 0.0-1.0 | 0.6 | Warning flag |

---

## 🆘 QUICK FIXES

### App Not Starting
```bash
pip install streamlit plotly
```

### Port Busy
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Upload Error
```
Max file size: 200MB
Format: PDF only
```

### Slow Performance
- Process fewer files
- Reduce Top-K
- Clear cache (sidebar)

---

## ⌨️ SHORTCUTS

| Key | Action |
|-----|--------|
| R | Reload app |
| C | Clear cache |
| Ctrl+S | Auto-save |

---

## 📂 FILE LOCATIONS

```
D:\RAG\
├── output/           # Results saved here
│   ├── *.xlsx       # Excel reports
│   └── *.json       # Raw data
├── data/            # Source PDFs
└── temp_uploads/    # Temporary files
```

---

## 🎓 BEST PRACTICES

1. ✅ **Upload < 10 PDFs** via web interface
2. ✅ **Batch process > 10 PDFs** from data folder
3. ✅ **Export results** before closing app
4. ✅ **Evaluate regularly** with human grading
5. ✅ **Clear cache** if app slows down

---

## 📊 WORKFLOW

```
Upload PDFs
    ↓
Process/Grade
    ↓
View Results
    ↓
Analyze Charts
    ↓
Export Reports
    ↓
(Optional) Evaluate vs Human
```

---

## 🎯 STATUS INDICATORS

| Indicator | Meaning |
|-----------|---------|
| ✅ Green | Success / Good |
| ⚠️ Yellow | Warning / Acceptable |
| ❌ Red | Error / Needs Improvement |
| ℹ️ Blue | Information |

---

## 🔗 RESOURCES

- Full Guide: `STREAMLIT_GUIDE.md`
- Metrics Info: `METRIK_EVALUASI.md`
- Installation: `PANDUAN_INSTALASI.md`

---

**Tip:** Keep this reference open while using the app!
