"""
DEMO SIMULASI: RAG Auto-Grading System
======================================
Simulasi untuk menunjukkan workflow sistem tanpa perlu API key aktif
"""

import json
from pathlib import Path
from datetime import datetime


def simulate_demo():
    """
    Simulasi demo workflow sistem RAG Auto-Grading
    """

    print("""
==============================================================
     RAG AUTO-GRADING SYSTEM v2.0 - DEMO SIMULASI
     Sistem Penilaian Otomatis Laporan Praktikum
==============================================================
""")

    # STEP 1: Load Rubrik
    print("\n" + "="*60)
    print("STEP 1: LOAD RUBRIK PENILAIAN")
    print("="*60)

    rubric_path = Path("data/rubrik.json")

    if rubric_path.exists():
        with open(rubric_path, 'r', encoding='utf-8') as f:
            rubric_data = json.load(f)

        print(f"[OK] Rubrik berhasil dimuat dari: {rubric_path}")
        print(f"   Mata Kuliah: {rubric_data['rubric']['course']}")
        print(f"   Jumlah Sub-Rubrik: {len(rubric_data['sub_rubrics'])}")

        print("\n[*] Sub-Rubrik yang akan dinilai:")
        for idx, sr in enumerate(rubric_data['sub_rubrics'], 1):
            weight = next((asr['weight'] for asr in rubric_data['assignment_sub_rubrics']
                          if asr['sub_rubric_id'] == sr['id']), 0)
            print(f"   {idx}. {sr['name']} (Weight: {weight}%)")
            print(f"      Description: {sr['description']}")
    else:
        print("[!] Rubrik tidak ditemukan. Menggunakan dummy data...")
        rubric_data = create_dummy_rubric()

    # STEP 2: Scan PDF Files
    print("\n" + "="*60)
    print("STEP 2: SCAN PDF FILES")
    print("="*60)

    data_folder = Path("data")
    pdf_files = list(data_folder.glob("*.pdf"))

    print(f"[*] Scanning folder: {data_folder.absolute()}")
    print(f"[OK] Ditemukan {len(pdf_files)} file PDF:")

    for idx, pdf in enumerate(pdf_files, 1):
        size_mb = pdf.stat().st_size / (1024 * 1024)
        print(f"   {idx}. {pdf.name} ({size_mb:.2f} MB)")

    # STEP 3: Simulate Processing
    print("\n" + "="*60)
    print("STEP 3: SIMULATE DOCUMENT PROCESSING")
    print("="*60)

    # Simulate for first PDF
    if pdf_files:
        sample_pdf = pdf_files[0]
        print(f"\n[PDF] Processing (simulasi): {sample_pdf.name}")
        print("="*60)

        # Simulate extraction
        print("\n[1/5] Extracting text from PDF...")
        print("      [OK] Extracted 15 pages")
        print("      [OK] Total characters: 12,458")
        print("      [OK] Detected metadata:")
        print("          - Kelompok: Kelompok 8")
        print("          - Mata Kuliah: Algoritma dan Pemrograman")

        # Simulate chunking
        print("\n[2/5] Chunking text...")
        print("      [OK] Created 23 chunks")
        print("      [OK] Chunk size: 1000 chars")
        print("      [OK] Overlap: 200 chars")

        # Simulate embedding
        print("\n[3/5] Creating embeddings...")
        print("      [OK] Model: all-MiniLM-L6-v2")
        print("      [OK] Embedding dimension: 384")
        print("      [OK] FAISS index built successfully")

        # Simulate RAG retrieval
        print("\n[4/5] RAG retrieval for evidence...")
        print("      Query 1: 'Dasar teori dalam laporan'")
        print("      [OK] Found 5 relevant chunks")
        print("      Query 2: 'Kode program dan implementasi'")
        print("      [OK] Found 5 relevant chunks")
        print("      Query 3: 'Kesimpulan dan pembahasan'")
        print("      [OK] Found 5 relevant chunks")

        # Simulate LLM grading
        print("\n[5/5] LLM grading dengan GLM-4.5...")
        print("      [OK] Prompt sent (3,245 tokens)")
        print("      [OK] Response received (892 tokens)")
        print("      [OK] JSON parsed successfully")

        # Simulate results
        print("\n" + "="*60)
        print("GRADING RESULTS (SIMULASI)")
        print("="*60)

        simulate_grading_result = {
            "grading_result": [
                {
                    "sub_rubric": "Dasar Teori",
                    "selected_level": "A",
                    "score_awarded": 90,
                    "weight": 10,
                    "confidence": 0.9,
                    "reason": "Dasar teori dikemukakan dengan jelas dan informatif"
                },
                {
                    "sub_rubric": "Kode Program",
                    "selected_level": "B",
                    "score_awarded": 70,
                    "weight": 50,
                    "confidence": 0.7,
                    "reason": "Program berjalan tapi kurang efisien"
                },
                {
                    "sub_rubric": "Keterangan Baris Program",
                    "selected_level": "A",
                    "score_awarded": 85,
                    "weight": 20,
                    "confidence": 0.85,
                    "reason": "Sebagian besar baris diberi penjelasan"
                },
                {
                    "sub_rubric": "Kesimpulan",
                    "selected_level": "B",
                    "score_awarded": 75,
                    "weight": 20,
                    "confidence": 0.8,
                    "reason": "Kesimpulan cukup jelas namun bisa lebih detail"
                }
            ],
            "final_score": 74.5,
            "overall_confidence": 0.81
        }

        print(f"\n[STATS] File: {sample_pdf.name}")
        print(f"{'-'*60}")

        for grade in simulate_grading_result["grading_result"]:
            print(f"\n[+] {grade['sub_rubric']}")
            print(f"  Level:      {grade['selected_level']}")
            print(f"  Score:      {grade['score_awarded']}/100")
            print(f"  Weight:     {grade['weight']}%")
            print(f"  Confidence: {grade['confidence']:.2f}")
            print(f"  Reason:     {grade['reason']}")

        print(f"\n{'-'*60}")
        print(f"[SCORE] FINAL SCORE: {simulate_grading_result['final_score']:.1f}/100")
        print(f"[CONF] CONFIDENCE:  {simulate_grading_result['overall_confidence']:.2f}")

        # STEP 4: Batch Processing Summary
        print("\n" + "="*60)
        print("STEP 4: BATCH PROCESSING SUMMARY (SIMULASI)")
        print("="*60)

        if len(pdf_files) > 1:
            print(f"\n[OK] Total {len(pdf_files)} dokumen akan diproses")
            print("\nEstimasi waktu:")
            print(f"   - Per dokumen: ~30-45 detik")
            print(f"   - Total: ~{len(pdf_files) * 35 / 60:.1f} menit")

            print("\nSimulasi hasil untuk semua dokumen:")
            print(f"{'-'*60}")
            print(f"{'Filename':<30} {'Score':<10} {'Confidence':<12}")
            print(f"{'-'*60}")

            # Simulate scores for all PDFs
            import random
            random.seed(42)

            all_scores = []
            for pdf in pdf_files:
                score = random.randint(65, 95)
                conf = random.uniform(0.7, 0.95)
                all_scores.append(score)
                print(f"{pdf.stem[:28]:<30} {score:<10} {conf:<12.2f}")

            print(f"{'-'*60}")
            print(f"\n[STATS] STATISTIK:")
            print(f"   Mean Score:   {sum(all_scores)/len(all_scores):.1f}")
            print(f"   Min Score:    {min(all_scores)}")
            print(f"   Max Score:    {max(all_scores)}")
            print(f"   Std Dev:      {(sum((x-sum(all_scores)/len(all_scores))**2 for x in all_scores)/len(all_scores))**0.5:.1f}")

    # STEP 5: Output Generation
    print("\n" + "="*60)
    print("STEP 5: OUTPUT GENERATION (SIMULASI)")
    print("="*60)

    output_folder = Path("output")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print(f"\n[DIR] Output folder: {output_folder.absolute()}")
    print("\nFiles yang akan di-generate:")

    print(f"\n1. [STATS] Excel Report: grading_results_{timestamp}.xlsx")
    print("   - Sheet 1: Summary (overview semua mahasiswa)")
    print("   - Sheet 2: Detailed Scores (breakdown per sub-rubrik)")

    print(f"\n2. [PDF] JSON Report: grading_results_{timestamp}.json")
    print("   - Raw data dalam format JSON")
    print("   - Bisa digunakan untuk integrasi dengan sistem lain")

    print(f"\n3. [CONF] Statistics Report:")
    print("   - Mean, Median, Std Dev")
    print("   - Score distribution")
    print("   - Low confidence warnings")

    # STEP 6: Next Steps
    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)

    print("""
Untuk menjalankan sistem sesungguhnya:

1. Install dependencies:
   $ pip install -r requirements.txt

2. Setup API key di rag_grading_improved.py:
   OPENROUTER_KEY = "your-api-key-here"

3. Siapkan data:
   - Letakkan PDF di folder data/
   - Pastikan rubrik.json sudah sesuai

4. Run batch processing:
   $ python rag_grading_improved.py

5. Check output:
   - Buka file Excel di folder output/
   - Review hasil penilaian
   - Flag dokumen dengan confidence rendah untuk manual review

[DOCS] Dokumentasi lengkap: README.md
""")

    print("="*60)
    print("[OK] DEMO SIMULASI SELESAI")
    print("="*60)


def create_dummy_rubric():
    """Create dummy rubric data untuk demo"""
    return {
        "rubric": {
            "name": "Rubrik Penilaian Algoritma Pemrograman",
            "course": "Algoritma dan Pemrograman",
            "description": "Rubrik untuk menilai tugas laporan ALPRO"
        },
        "sub_rubrics": [
            {
                "id": "UUID-SUB1",
                "name": "Dasar Teori",
                "description": "Mengukur pemahaman teori dasar"
            },
            {
                "id": "UUID-SUB2",
                "name": "Kode Program",
                "description": "Mengukur efisiensi program dan penamaan variabel"
            },
            {
                "id": "UUID-SUB3",
                "name": "Keterangan Baris Program",
                "description": "Mengukur kejelasan penjelasan baris code"
            },
            {
                "id": "UUID-SUB4",
                "name": "Kesimpulan",
                "description": "Mengukur kejelasan kesimpulan"
            }
        ],
        "assignment_sub_rubrics": [
            {"sub_rubric_id": "UUID-SUB1", "weight": 10},
            {"sub_rubric_id": "UUID-SUB2", "weight": 50},
            {"sub_rubric_id": "UUID-SUB3", "weight": 20},
            {"sub_rubric_id": "UUID-SUB4", "weight": 20}
        ]
    }


if __name__ == "__main__":
    simulate_demo()
