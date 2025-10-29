# 🎓 RAG Auto-Grading System - Streamlit Web Interface

## 📋 Overview

Aplikasi web berbasis Streamlit yang menyediakan interface user-friendly untuk:
- ✅ Upload dan grade PDF laporan praktikum
- ✅ Visualisasi hasil grading dengan charts interaktif
- ✅ Evaluasi akurasi AI vs Human grading
- ✅ Export hasil ke Excel, JSON, dan CSV
- ✅ Real-time monitoring dan statistics

---

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
# Activate conda environment
conda activate rag-grading

# Install Streamlit dan dependencies
pip install streamlit plotly

# Atau install dari requirements
pip install -r requirements_streamlit.txt
```

### Step 2: Run Streamlit App

**Option A: Using Batch Script (Windows)**
```bash
# Double-click atau run di command prompt
run_streamlit.bat
```

**Option B: Manual**
```bash
# Activate environment
conda activate rag-grading

# Run streamlit
streamlit run streamlit_app.py
```

### Step 3: Open Browser

Aplikasi akan otomatis terbuka di browser pada:
```
http://localhost:8501
```

---

## 📱 FITUR-FITUR APLIKASI

### 🏠 HOME PAGE

**Overview Dashboard:**
- System statistics (total gradings, files, etc.)
- Quick start guide
- Configuration summary

**Features:**
- View system info
- Check previous gradings
- Navigation to other pages

---

### 📄 GRADING PAGE

**Upload & Process Tab:**

1. **Upload Files:**
   - Click "Browse files" atau drag & drop PDF files
   - Support multiple files sekaligus
   - Lihat file size dan preview

2. **Start Grading:**
   - Click "Start Grading" button
   - Progress bar menunjukkan status
   - Real-time processing updates

3. **Results:**
   - Automatic save to `output/` folder
   - JSON format untuk data persistence
   - Ready untuk visualisasi

**Batch Processing Tab:**

1. **Auto-detect Files:**
   - Scan `data/` folder untuk PDF files
   - List semua files yang ditemukan
   - Show file count

2. **Process All:**
   - Click "Process All PDFs"
   - Batch processing dengan progress tracking
   - Save results automatically

---

### 📊 RESULTS PAGE

#### **Tab 1: Summary**

**Statistics Cards:**
- Total Documents
- Average Score
- Average Confidence
- Low Confidence Count

**Summary Table:**
```
| Filename | Kelompok | Final Score | Confidence | Page Count |
|----------|----------|-------------|------------|------------|
| LP_Kel_8 | Kel 8    | 74.5        | 0.81       | 15         |
```

**Features:**
- Color-coded scores (gradient green-yellow-red)
- Sortable columns
- Low confidence warnings

---

#### **Tab 2: Detailed Scores**

**Document Selector:**
- Dropdown untuk pilih dokumen
- Show document metadata

**Per Sub-Rubrik:**
```
📋 Dasar Teori - Level A (85/100)
   ├─ Score: 85/100
   ├─ Weight: 10%
   ├─ Level: A
   ├─ Confidence: 0.90
   ├─ Reason: "Dasar teori dikemukakan dengan jelas..."
   └─ Evidence: "Variabel merupakan..."
```

**Features:**
- Expandable cards per sub-rubrik
- Show reasoning dan evidence
- Confidence indicators

---

#### **Tab 3: Visualizations**

**1. Score Distribution (Histogram)**
- X-axis: Score range (0-100)
- Y-axis: Count
- Shows overall score distribution

**2. Confidence Distribution (Histogram)**
- X-axis: Confidence (0-1)
- Y-axis: Count
- Shows confidence reliability

**3. Scores by Document (Bar Chart)**
- X-axis: Document names
- Y-axis: Scores
- Color: Confidence level
- Interactive hover tooltips

**4. Score Distribution by Sub-Rubric (Box Plot)**
- Compare scores across sub-rubrics
- Show median, quartiles, outliers
- Identify problematic rubrics

**5. Score vs Confidence (Scatter Plot)**
- X-axis: Final Score
- Y-axis: Confidence
- Trendline untuk correlation
- Identify low-confidence outliers

**Interactive Features:**
- Zoom in/out
- Pan
- Hover tooltips
- Download plots as PNG

---

#### **Tab 4: Export**

**Export Options:**

1. **Excel Export:**
   - Click "Generate Excel"
   - Creates 2 sheets:
     - Summary: Overview all documents
     - Detailed Scores: Per sub-rubrik breakdown
   - Download button muncul setelah generate

2. **JSON Export:**
   - Click "Download JSON"
   - Raw data dalam JSON format
   - Untuk integrasi dengan sistem lain

3. **CSV Export:**
   - Click "Download CSV Summary"
   - Summary table dalam CSV
   - Easy untuk import ke Excel/Google Sheets

**File Naming:**
```
grading_results_YYYYMMDD_HHMMSS.xlsx
grading_results_YYYYMMDD_HHMMSS.json
summary_YYYYMMDD_HHMMSS.csv
```

---

### 📈 EVALUATION PAGE

#### **Tab 1: Upload Human Results**

**Purpose:**
- Compare AI grading dengan human grading
- Calculate accuracy metrics
- Identify systematic biases

**Steps:**

1. **Prepare Human Grading JSON:**
   ```json
   [
     {
       "final_score": 78,
       "overall_confidence": 1.0,
       "grading_result": [
         {
           "sub_rubric": "Dasar Teori",
           "selected_level": "A",
           "score_awarded": 88
         },
         ...
       ],
       "document_info": {
         "filename": "LP_Kel_8"
       }
     }
   ]
   ```

2. **Upload File:**
   - Click "Browse files"
   - Select human grading JSON
   - File automatically loaded

3. **Validation:**
   - System checks format
   - Validates data structure
   - Shows success/error message

---

#### **Tab 2: Evaluation Metrics**

**Metric Cards (Top Row):**
```
┌─────────┬─────────┬────────────┬─────────────┐
│   MAE   │  RMSE   │ Pearson r  │  Cohen's κ  │
│   8.5   │  10.2   │   0.82     │    0.68     │
└─────────┴─────────┴────────────┴─────────────┘
```

**Left Column: Accuracy Metrics**
- Within ±5 points: 72%
- Within ±10 points: 90%
- Exact Match Rate: 5%
- Status indicator:
  - ✅ Excellent (MAE < 5)
  - ✅ Good (MAE < 10)
  - ⚠️ Acceptable (MAE < 15)
  - ❌ Needs Improvement (MAE > 15)

**Right Column: Confidence Metrics**
- Mean Confidence: 0.81
- Confidence-Error Correlation: -0.65
- Expected Calibration Error: 0.08
- Calibration status indicator

---

**Visualizations:**

**1. AI vs Human Scores (Scatter Plot)**
```
      AI Score
       100│         ╱
          │       ╱ ●
          │     ╱   ●
        50│   ╱ ●●●
          │ ╱   ●
         0└────────────→
           0    50   100
              Human Score
```
- Perfect agreement line (red dashed)
- Trendline (blue)
- Points closer to line = better agreement

**2. Error Distribution (Histogram)**
- Shows frequency of errors
- Most errors should be < 10 points
- Identify if errors are normally distributed

**3. Bland-Altman Plot**
```
   Difference (AI - Human)
       +20│     ●           +1.96 SD
          │  ●  ●  ●
         0│●●●●●●●●●      Mean
          │  ●  ●
       -20│     ●           -1.96 SD
          └─────────────→
            Mean Score
```
- Check for systematic bias
- Points should be within ±1.96 SD
- Identify outliers

**Download Report:**
- Click "Download Evaluation Report"
- JSON file dengan semua metrics
- Untuk dokumentasi dan analysis

---

## ⚙️ SIDEBAR CONFIGURATION

**System Info:**
- Model: GLM-4.5
- Embedding: all-MiniLM-L6-v2
- Current settings

**Adjustable Settings:**

1. **Chunk Size** (500-2000)
   - Slide untuk adjust
   - Affects: RAG retrieval granularity
   - Recommendation: 1000 untuk most cases

2. **Top-K Retrieval** (3-15)
   - Slide untuk adjust
   - Affects: Number of evidence chunks
   - Recommendation: 5-7 untuk balance

3. **Confidence Threshold** (0.0-1.0)
   - Slide untuk adjust
   - Affects: Low confidence flagging
   - Recommendation: 0.6

**Reset Configuration:**
- Click "Reset Configuration"
- Restore default values
- Clear cache

---

## 🎯 WORKFLOW EXAMPLES

### Example 1: Grade New Submissions

```
1. Go to "Grading" page
2. Upload PDF files
3. Click "Start Grading"
4. Wait for processing (progress bar)
5. Go to "Results" page
6. View summary and detailed scores
7. Export to Excel
8. Share with stakeholders
```

**Time:** ~30-45 seconds per document

---

### Example 2: Batch Processing

```
1. Copy all PDF files to data/ folder
2. Go to "Grading" page → "Batch Processing" tab
3. Verify files listed
4. Click "Process All PDFs"
5. Wait for completion
6. Go to "Results" page
7. Analyze visualizations
8. Export summary CSV
```

**Time:** ~5-7 minutes for 10 documents

---

### Example 3: Evaluate AI Accuracy

```
1. Grade documents with AI (see Example 1)
2. Collect human grading for same documents
3. Go to "Evaluation" page
4. Upload human grading JSON
5. Go to "Evaluation Metrics" tab
6. Analyze metrics and visualizations
7. Download evaluation report
8. Make improvements if needed
```

**Time:** ~10 minutes (after data collection)

---

## 🔧 CUSTOMIZATION

### Themes

Streamlit supports themes. Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor="#1f77b4"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#f0f2f6"
textColor="#262730"
font="sans serif"
```

---

### Custom Logo

Add logo to app:

```python
from PIL import Image
logo = Image.open('logo.png')
st.image(logo, width=200)
```

---

### Additional Pages

Add new page to `streamlit_app.py`:

```python
def custom_page():
    st.title("Custom Page")
    # Your content here

# In main():
elif page == "Custom":
    custom_page()
```

---

## 📊 KEYBOARD SHORTCUTS

When app is running:

- **R**: Rerun the app
- **C**: Clear cache
- **Ctrl+S**: Save (auto-save enabled)
- **Ctrl+Shift+R**: Hard reload

---

## 🆘 TROUBLESHOOTING

### Issue 1: App Won't Start

**Error:** `streamlit: command not found`

**Solution:**
```bash
# Make sure environment is activated
conda activate rag-grading

# Install streamlit
pip install streamlit
```

---

### Issue 2: Import Error

**Error:** `ModuleNotFoundError: No module named 'plotly'`

**Solution:**
```bash
pip install plotly
```

---

### Issue 3: Port Already in Use

**Error:** `Port 8501 is already in use`

**Solution:**
```bash
# Use different port
streamlit run streamlit_app.py --server.port 8502

# Or find and kill process using port 8501
```

---

### Issue 4: Upload Size Limit

**Error:** `File size exceeds limit`

**Solution:**

Edit `.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 500
```

---

### Issue 5: Slow Performance

**Problem:** App feels slow with many PDFs

**Solutions:**
1. Use batch processing instead of upload
2. Reduce TOP_K_RETRIEVAL
3. Process fewer files at once
4. Increase streamlit memory:
   ```bash
   streamlit run streamlit_app.py --server.maxMessageSize 1000
   ```

---

## 📈 BEST PRACTICES

### 1. File Management
- Keep `data/` folder organized
- Archive old results regularly
- Use descriptive filenames

### 2. Performance
- Process < 10 PDFs at once via upload
- Use batch processing for > 10 PDFs
- Clear cache periodically (sidebar button)

### 3. Evaluation
- Collect human grading systematically
- Evaluate on representative sample (minimum 20 documents)
- Re-evaluate after making changes

### 4. Sharing
- Export results before sharing
- Include confidence scores in reports
- Flag low-confidence documents

---

## 🎓 TIPS & TRICKS

### Tip 1: Quick Reload
Press **R** to quickly reload after making changes

### Tip 2: Multi-Page Navigation
Use sidebar for quick navigation between pages

### Tip 3: Download Plots
Hover over any plot → Click camera icon → Save as PNG

### Tip 4: Filter Data
Use Pandas dataframe built-in filtering (click column headers)

### Tip 5: Session State
Data persists within session. Refresh to clear.

---

## 📞 SUPPORT

**Common Questions:**

Q: Can I grade only specific rubrics?
A: No, system grades all rubrics in rubrik.json

Q: Can I edit scores after grading?
A: No, re-grade if needed. Future: Manual override feature

Q: How to backup results?
A: Results auto-saved to `output/` folder. Backup this folder.

Q: Can multiple users use simultaneously?
A: Yes, run on server. Each user gets separate session.

---

## 🚀 DEPLOYMENT

### Local Network Deployment

```bash
# Run with network access
streamlit run streamlit_app.py --server.address 0.0.0.0

# Access from other devices
http://<your-ip>:8501
```

### Cloud Deployment

**Streamlit Cloud (Free):**
1. Push code to GitHub
2. Go to share.streamlit.io
3. Connect repository
4. Deploy!

**Heroku:**
```bash
# Create Procfile
echo "web: streamlit run streamlit_app.py --server.port $PORT" > Procfile

# Deploy
heroku create
git push heroku main
```

---

## 📋 CHECKLIST

**Before First Use:**
- [ ] Install dependencies
- [ ] Setup `.env` file
- [ ] Test with sample PDF
- [ ] Verify rubrik.json

**Regular Maintenance:**
- [ ] Clear old results (weekly)
- [ ] Update dependencies (monthly)
- [ ] Backup results (weekly)
- [ ] Review metrics (after each batch)

---

## 🎉 CONCLUSION

Streamlit interface membuat RAG auto-grading system:
- ✅ User-friendly untuk non-technical users
- ✅ Visual insights dengan charts interaktif
- ✅ Easy export untuk reporting
- ✅ Built-in evaluation tools

**Next Steps:**
1. Launch app dengan `run_streamlit.bat`
2. Upload beberapa PDF untuk testing
3. Explore visualizations
4. Compare dengan human grading
5. Deploy untuk production use

---

**Document Version**: 1.0
**Last Updated**: 2025-10-29
**Streamlit Version**: 1.28+
