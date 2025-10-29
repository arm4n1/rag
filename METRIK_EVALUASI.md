# 📊 METRIK EVALUASI RAG AUTO-GRADING SYSTEM

---

## 🎯 OVERVIEW

Berbeda dengan klasifikasi tradisional (yang menggunakan accuracy, precision, recall, F1), **sistem RAG memerlukan metrik khusus** karena melibatkan 2 komponen:

1. **Retrieval Component** → Seberapa baik sistem menemukan evidence yang relevan
2. **Generation Component** → Seberapa akurat LLM dalam menggunakan evidence untuk grading

---

## 📈 KATEGORI METRIK

### 1️⃣ RETRIEVAL METRICS (RAG/Vector Search)

#### **Hit Rate@K**
```
Hit Rate@K = (Queries dengan dokumen relevan di Top-K) / Total queries
```

**Interpretasi:**
- Range: 0 to 1
- Target: **> 0.85** (85% queries menemukan evidence relevan di Top-5)
- **Contoh**: Dari 100 sub-rubrik yang dinilai, 87 menemukan evidence di Top-5 chunks → Hit Rate@5 = 0.87

**Kapan gunakan:**
- Untuk mengukur apakah retrieval "menemukan" informasi yang dibutuhkan
- Evaluasi kualitas embedding model dan chunking strategy

---

#### **Mean Reciprocal Rank (MRR)**
```
MRR = (1/n) × Σ(1 / rank_first_relevant)
```

**Interpretasi:**
- Range: 0 to 1
- Target: **> 0.7** (dokumen relevan rata-rata di posisi 1-2)
- **Contoh**: Dokumen relevan di posisi [1, 3, 2, 1, 4] → MRR = (1/1 + 1/3 + 1/2 + 1/1 + 1/4) / 5 = 0.61

**Kapan gunakan:**
- Untuk mengukur "ranking quality"
- Lebih ketat dari Hit Rate (peduli posisi dokumen)

---

#### **Context Precision**
```
Precision = Chunks yang digunakan / Chunks yang di-retrieve
```

**Interpretasi:**
- Range: 0 to 1
- Target: **> 0.6** (minimal 60% chunks yang di-retrieve benar-benar dipakai)
- **Contoh**: Retrieve 10 chunks, LLM pakai 7 chunks → Precision = 0.7

**Kapan gunakan:**
- Untuk mendeteksi apakah sistem retrieve **terlalu banyak irrelevant chunks**
- Optimization: Kalau precision rendah, turunkan TOP_K atau improve query generation

---

#### **Context Recall**
```
Recall = Relevant chunks yang di-retrieve / Total relevant chunks
```

**Interpretasi:**
- Range: 0 to 1
- Target: **> 0.7** (sistem tidak miss informasi penting)
- **Contoh**: Ada 10 relevant chunks, sistem retrieve 8 → Recall = 0.8

**Kapan gunakan:**
- Untuk mendeteksi apakah sistem **miss informasi penting**
- Optimization: Kalau recall rendah, naikkan TOP_K atau improve chunking

---

### 2️⃣ GENERATION METRICS (LLM Quality)

#### **Faithfulness Score**
```
Faithfulness = Claims yang didukung evidence / Total claims
```

**Interpretasi:**
- Range: 0 to 1
- Target: **> 0.8** (80% claims didukung evidence)
- **Penting untuk RAG**: Mengukur apakah LLM **tidak hallucinate**

**Contoh:**
```
Evidence: "Program menggunakan variabel x dan y"
Response: "Program menggunakan variabel x, y, dan z" ❌
Faithfulness: 0.67 (2/3 benar, 1 claim tidak didukung evidence)
```

**Kapan gunakan:**
- Untuk memastikan LLM tidak "mengarang" di luar evidence
- Critical untuk auto-grading (harus objektif berdasarkan dokumen)

---

#### **Answer Relevance**
```
Relevance = Semantic similarity(answer, question)
```

**Interpretasi:**
- Range: 0 to 1
- Target: **> 0.75**
- Mengukur apakah jawaban LLM **on-topic** dengan pertanyaan

---

### 3️⃣ GRADING ACCURACY METRICS (End-to-End)

#### **Mean Absolute Error (MAE)**
```
MAE = (1/n) × Σ|predicted_score - actual_score|
```

**Interpretasi:**
- Range: 0 to 100 (untuk scale 0-100)
- **Target:**
  - Excellent: **MAE < 5**
  - Good: **MAE < 10**
  - Acceptable: **MAE < 15**
  - Needs improvement: **MAE > 15**

**Contoh:**
```
AI:    [75, 82, 68]
Human: [78, 85, 65]
Errors: [3, 3, 3]
MAE = 3.0 ✅ Excellent!
```

**Kapan gunakan:**
- **Primary metric** untuk evaluasi grading accuracy
- Mudah interpretasi (rata-rata error dalam points)

---

#### **Root Mean Squared Error (RMSE)**
```
RMSE = sqrt((1/n) × Σ(predicted - actual)²)
```

**Interpretasi:**
- Range: 0 to 100
- Lebih sensitif terhadap **outlier** dibanding MAE
- Target: RMSE < 12

**Contoh:**
```
Errors: [3, 3, 30]  <- Ada 1 outlier besar
MAE = 12 (keliatan OK)
RMSE = 17.5 (lebih tinggi karena outlier)
```

**Kapan gunakan:**
- Ketika ingin **penalize outlier** lebih berat
- Untuk detect systematic bias

---

#### **Pearson Correlation**
```
r = cov(AI, Human) / (σ_AI × σ_Human)
```

**Interpretasi:**
- Range: -1 to 1
- **Target: r > 0.8** (strong positive correlation)
- Mengukur **linear relationship** antara AI vs Human grading

**Interpretasi nilai:**
- 0.9 - 1.0: Very strong correlation ✅
- 0.7 - 0.9: Strong correlation ✅
- 0.5 - 0.7: Moderate correlation ⚠️
- < 0.5: Weak correlation ❌

**Contoh:**
```
AI:    [60, 70, 80, 90]
Human: [62, 72, 82, 92]
r = 0.99 ✅ Sangat konsisten!
```

---

#### **Cohen's Kappa (κ)**
```
κ = (p_o - p_e) / (1 - p_e)
```

**Interpretasi:**
- Range: -1 to 1
- Mengukur **agreement** antara raters (beyond chance)

**Nilai benchmark:**
```
κ < 0.00:     Worse than random ❌
κ 0.01-0.20:  Slight agreement ❌
κ 0.21-0.40:  Fair agreement ⚠️
κ 0.41-0.60:  Moderate agreement ⚠️
κ 0.61-0.80:  Substantial agreement ✅
κ 0.81-1.00:  Almost perfect agreement ✅
```

**Contoh:**
```
AI Labels:    [A, B, A, C, B]
Human Labels: [A, B, A, C, A]
Agreement: 4/5 = 80%
κ = 0.75 ✅ Substantial agreement
```

---

#### **Within-Range Accuracy**
```
WRA = (Predictions within ±threshold) / Total
```

**Interpretasi:**
- Range: 0 to 1
- Praktis untuk auto-grading (toleransi error)

**Benchmarks:**
- Within ±5 points: Target **> 70%**
- Within ±10 points: Target **> 90%**

**Contoh:**
```
Errors: [3, 7, 12, 4, 2]
Within ±5: 60% (3 dari 5)
Within ±10: 80% (4 dari 5)
```

---

### 4️⃣ CONFIDENCE CALIBRATION METRICS

#### **Expected Calibration Error (ECE)**
```
ECE = Σ |accuracy_bin - confidence_bin| × weight_bin
```

**Interpretasi:**
- Range: 0 to 1
- Target: **ECE < 0.1** (well-calibrated)
- Mengukur apakah confidence score **akurat**

**Ideal calibration:**
```
Jika model 80% confident → Seharusnya benar 80% of the time
Jika model 90% confident → Seharusnya benar 90% of the time
```

**Contoh:**
```
Model says: 90% confident
Actual accuracy: 85%
Calibration error: 5%

Model says: 70% confident
Actual accuracy: 75%
Calibration error: 5%

ECE = 0.05 ✅ Well-calibrated!
```

---

#### **Confidence-Error Correlation**
```
Correlation(confidence_scores, error_magnitudes)
```

**Interpretasi:**
- Range: -1 to 1
- Target: **Negative correlation** (r < -0.3)
- High confidence → Low error
- Low confidence → High error

**Contoh:**
```
Confidences: [0.9, 0.8, 0.6, 0.9, 0.7]
Errors:      [2,   5,   12,  3,   8  ]
r = -0.85 ✅ High conf → Low error (good!)
```

---

## 🎯 METRIK PRIORITAS UNTUK SISTEM ANDA

### **Priority 1 (MUST TRACK)**

1. **MAE** - Primary accuracy metric
   - Target: < 10 points
   - Kalau MAE tinggi → Model perlu improvement

2. **Pearson Correlation** - Consistency metric
   - Target: > 0.8
   - Kalau r rendah → Model tidak konsisten dengan human judgment

3. **Within ±5 Points Accuracy**
   - Target: > 70%
   - Praktis untuk evaluasi "acceptable error"

4. **Mean Confidence**
   - Target: > 0.75
   - Kalau confidence rendah → Evidence tidak cukup atau rubrik ambiguous

---

### **Priority 2 (SHOULD TRACK)**

5. **Hit Rate@5** - Retrieval quality
   - Target: > 0.85
   - Kalau rendah → Problem di embedding atau chunking

6. **Faithfulness Score** - No hallucination
   - Target: > 0.8
   - Critical untuk credibility

7. **Cohen's Kappa** - Inter-rater agreement
   - Target: > 0.6 (substantial)

---

### **Priority 3 (NICE TO HAVE)**

8. **MRR** - Ranking quality
9. **ECE** - Confidence calibration
10. **Context Precision/Recall** - RAG optimization

---

## 📊 EXAMPLE EVALUATION WORKFLOW

### Step 1: Generate AI Grading
```bash
python rag_grading_improved.py
```

### Step 2: Collect Human Grading
Minta dosen untuk grade dokumen yang sama (ground truth)

### Step 3: Run Evaluation
```python
from example_evaluation import evaluate_from_files

metrics = evaluate_from_files(
    'output/grading_results_20251029.json',
    'data/human_grading_results.json'
)
```

### Step 4: Analyze Results
```
MAE = 8.5 ✅ Good
Pearson r = 0.82 ✅ Strong correlation
Within ±5: 72% ✅ Acceptable
Cohen's Kappa = 0.68 ✅ Substantial agreement

→ System ready for production!
```

---

## 🔧 TROUBLESHOOTING BERDASARKAN METRIK

### **Problem: MAE tinggi (> 15)**
**Possible causes:**
- Evidence tidak cukup relevan
- Prompt kurang jelas
- Rubrik ambiguous

**Solutions:**
- Increase TOP_K_RETRIEVAL (5 → 7-10)
- Improve multi-query generation
- Refine rubrik descriptions
- Adjust CHUNK_SIZE

---

### **Problem: Correlation rendah (< 0.7)**
**Possible causes:**
- Model tidak konsisten
- Rubrik interpretasi berbeda
- Systemic bias

**Solutions:**
- Add more examples in prompt
- Clarify rubrik criteria
- Check for specific sub-rubrik with low correlation

---

### **Problem: Hit Rate rendah (< 0.8)**
**Possible causes:**
- Embedding model tidak cocok
- Chunking strategy buruk
- Query generation tidak optimal

**Solutions:**
- Try different embedding model
- Adjust CHUNK_SIZE dan CHUNK_OVERLAP
- Improve _build_queries_for_subrubric()

---

### **Problem: Faithfulness rendah (< 0.7)**
**Possible causes:**
- LLM hallucinating
- Evidence tidak cukup
- Temperature terlalu tinggi

**Solutions:**
- Set TEMPERATURE = 0.0 (deterministic)
- Add stronger prompt constraints
- Increase evidence chunks
- Use better LLM model

---

### **Problem: ECE tinggi (> 0.15)**
**Possible causes:**
- Confidence scores not calibrated
- Model overconfident atau underconfident

**Solutions:**
- Implement confidence calibration
- Adjust confidence calculation method
- Use temperature scaling

---

## 📈 BENCHMARKS FOR PRODUCTION

Sistem siap production jika memenuhi:

✅ **MAE < 10**
✅ **Pearson r > 0.75**
✅ **Within ±5 points > 70%**
✅ **Cohen's Kappa > 0.6**
✅ **Mean Confidence > 0.7**
✅ **Hit Rate@5 > 0.8**

**Bonus (optional tapi recommended):**
- Faithfulness > 0.8
- ECE < 0.1
- MRR > 0.7

---

## 🎓 INTERPRETASI UNTUK STAKEHOLDERS

### Untuk Dosen:
**"MAE 8.5 points"** artinya:
- Rata-rata selisih nilai AI vs Dosen adalah 8.5 poin
- Misal dosen kasih 75, AI kemungkinan kasih 67-83
- Ini setara dengan "selisih setengah grade" (masih reasonable)

**"Pearson r = 0.82"** artinya:
- AI dan Dosen **82% konsisten** dalam ranking mahasiswa
- Mahasiswa yang dapat nilai tinggi dari dosen, juga dapat nilai tinggi dari AI

**"Cohen's Kappa = 0.68"** artinya:
- Agreement "substantial" antara AI vs Dosen
- Lebih reliable dari random guessing

### Untuk Management:
- **MAE < 10** → System production-ready
- **Hit Rate > 85%** → Retrieval system reliable
- **Confidence > 75%** → System knows when it's uncertain

---

## 📝 QUICK REFERENCE

| Metric | Formula | Good Value | Excellent Value |
|--------|---------|------------|-----------------|
| MAE | Avg abs error | < 10 | < 5 |
| RMSE | Sqrt mean sq error | < 12 | < 7 |
| Pearson r | Correlation | > 0.75 | > 0.85 |
| Cohen's κ | Agreement | > 0.6 | > 0.8 |
| Hit Rate@5 | Top-5 retrieval | > 0.80 | > 0.90 |
| MRR | Reciprocal rank | > 0.65 | > 0.80 |
| Faithfulness | No hallucination | > 0.75 | > 0.85 |
| ECE | Calibration error | < 0.15 | < 0.10 |
| Within ±5 | Tolerance acc | > 0.65 | > 0.80 |

---

## 🚀 NEXT STEPS

1. ✅ **Baca dokumentasi ini** untuk memahami metrik
2. ✅ **Run example_evaluation.py** untuk lihat contoh
3. ✅ **Collect human grading** untuk ground truth
4. ✅ **Evaluate sistem** Anda menggunakan metrik ini
5. ✅ **Iterate** berdasarkan hasil evaluasi

---

**Remember:** Tidak ada single "best" metric. Gunakan **combination of metrics** untuk comprehensive evaluation!

**Document Version**: 1.0
**Last Updated**: 2025-10-29
