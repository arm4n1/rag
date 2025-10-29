"""
Example: Evaluasi RAG Auto-Grading System

Script ini menunjukkan cara menggunakan metrik evaluasi untuk mengukur
performa sistem RAG auto-grading dibanding human grading.
"""

from evaluation_metrics import RAGEvaluationMetrics
import json

def example_evaluation():
    """
    Contoh evaluasi dengan dummy data
    Dalam praktik, ganti dengan data sesungguhnya
    """

    ai_results = [
        {
            "final_score": 75,
            "overall_confidence": 0.85,
            "grading_result": [
                {"sub_rubric": "Dasar Teori", "selected_level": "A", "score_awarded": 85},
                {"sub_rubric": "Kode Program", "selected_level": "B", "score_awarded": 70},
                {"sub_rubric": "Keterangan", "selected_level": "A", "score_awarded": 80},
                {"sub_rubric": "Kesimpulan", "selected_level": "B", "score_awarded": 75}
            ]
        },
        {
            "final_score": 82,
            "overall_confidence": 0.90,
            "grading_result": [
                {"sub_rubric": "Dasar Teori", "selected_level": "A", "score_awarded": 90},
                {"sub_rubric": "Kode Program", "selected_level": "A", "score_awarded": 85},
                {"sub_rubric": "Keterangan", "selected_level": "A", "score_awarded": 85},
                {"sub_rubric": "Kesimpulan", "selected_level": "B", "score_awarded": 70}
            ]
        },
        {
            "final_score": 68,
            "overall_confidence": 0.75,
            "grading_result": [
                {"sub_rubric": "Dasar Teori", "selected_level": "B", "score_awarded": 75},
                {"sub_rubric": "Kode Program", "selected_level": "C", "score_awarded": 60},
                {"sub_rubric": "Keterangan", "selected_level": "B", "score_awarded": 70},
                {"sub_rubric": "Kesimpulan", "selected_level": "B", "score_awarded": 72}
            ]
        },
    ]

    human_results = [
        {
            "final_score": 78,
            "overall_confidence": 1.0,
            "grading_result": [
                {"sub_rubric": "Dasar Teori", "selected_level": "A", "score_awarded": 88},
                {"sub_rubric": "Kode Program", "selected_level": "B", "score_awarded": 72},
                {"sub_rubric": "Keterangan", "selected_level": "A", "score_awarded": 82},
                {"sub_rubric": "Kesimpulan", "selected_level": "B", "score_awarded": 75}
            ]
        },
        {
            "final_score": 85,
            "overall_confidence": 1.0,
            "grading_result": [
                {"sub_rubric": "Dasar Teori", "selected_level": "A", "score_awarded": 92},
                {"sub_rubric": "Kode Program", "selected_level": "A", "score_awarded": 88},
                {"sub_rubric": "Keterangan", "selected_level": "A", "score_awarded": 85},
                {"sub_rubric": "Kesimpulan", "selected_level": "B", "score_awarded": 72}
            ]
        },
        {
            "final_score": 65,
            "overall_confidence": 1.0,
            "grading_result": [
                {"sub_rubric": "Dasar Teori", "selected_level": "B", "score_awarded": 72},
                {"sub_rubric": "Kode Program", "selected_level": "C", "score_awarded": 58},
                {"sub_rubric": "Keterangan", "selected_level": "B", "score_awarded": 68},
                {"sub_rubric": "Kesimpulan", "selected_level": "B", "score_awarded": 70}
            ]
        },
    ]

    print("EVALUASI SISTEM RAG AUTO-GRADING")
    print("="*60)
    print(f"Jumlah dokumen: {len(ai_results)}")
    print(f"AI Results: {[r['final_score'] for r in ai_results]}")
    print(f"Human Results: {[r['final_score'] for r in human_results]}")
    print()

    metrics = RAGEvaluationMetrics.comprehensive_evaluation(ai_results, human_results)

    RAGEvaluationMetrics.print_evaluation_report(metrics)

    with open("evaluation_report.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print("\n✅ Report saved to: evaluation_report.json")


def evaluate_from_files(ai_results_path: str, human_results_path: str):
    """
    Evaluasi dari file JSON hasil grading

    Args:
        ai_results_path: Path ke JSON hasil AI grading
        human_results_path: Path ke JSON hasil human grading
    """

    with open(ai_results_path, 'r', encoding='utf-8') as f:
        ai_results = json.load(f)

    with open(human_results_path, 'r', encoding='utf-8') as f:
        human_results = json.load(f)

    print(f"Loaded {len(ai_results)} AI results")
    print(f"Loaded {len(human_results)} human results")

    if len(ai_results) != len(human_results):
        print("WARNING: Number of AI results != Human results")
        min_len = min(len(ai_results), len(human_results))
        ai_results = ai_results[:min_len]
        human_results = human_results[:min_len]
        print(f"Using first {min_len} results for comparison")

    metrics = RAGEvaluationMetrics.comprehensive_evaluation(ai_results, human_results)

    RAGEvaluationMetrics.print_evaluation_report(metrics)

    return metrics


def individual_metric_examples():
    """Contoh penggunaan metrik individual"""

    print("\n" + "="*60)
    print("CONTOH PENGGUNAAN METRIK INDIVIDUAL")
    print("="*60)

    ai_scores = [75, 82, 68, 90, 55]
    human_scores = [78, 85, 65, 92, 58]

    print("\nData:")
    print(f"AI Scores:    {ai_scores}")
    print(f"Human Scores: {human_scores}")

    mae = RAGEvaluationMetrics.mean_absolute_error(ai_scores, human_scores)
    print(f"\nMAE: {mae:.2f} points")

    rmse = RAGEvaluationMetrics.root_mean_squared_error(ai_scores, human_scores)
    print(f"RMSE: {rmse:.2f} points")

    pearson_r, p_value = RAGEvaluationMetrics.pearson_correlation(ai_scores, human_scores)
    print(f"Pearson Correlation: {pearson_r:.3f} (p={p_value:.4f})")

    within_5 = RAGEvaluationMetrics.within_range_accuracy(ai_scores, human_scores, 5)
    print(f"Within ±5 points: {within_5*100:.1f}%")

    ai_labels = ['A', 'A', 'B', 'A', 'C']
    human_labels = ['A', 'A', 'B', 'A', 'C']
    kappa = RAGEvaluationMetrics.cohen_kappa(ai_labels, human_labels)
    print(f"Cohen's Kappa: {kappa:.3f}")

    confidences = [0.85, 0.90, 0.75, 0.95, 0.70]
    errors = [abs(a - h) for a, h in zip(ai_scores, human_scores)]
    conf_corr = RAGEvaluationMetrics.confidence_accuracy_correlation(confidences, errors)
    print(f"Confidence-Error Correlation: {conf_corr:.3f}")
    if conf_corr < 0:
        print("  ✅ Good: High confidence → Low error")
    else:
        print("  ⚠️ Bad: Confidence not calibrated well")


if __name__ == "__main__":
    print("RAG AUTO-GRADING EVALUATION EXAMPLES\n")

    print("="*60)
    print("EXAMPLE 1: Evaluasi dengan dummy data")
    print("="*60)
    example_evaluation()

    print("\n\n")
    print("="*60)
    print("EXAMPLE 2: Penggunaan metrik individual")
    print("="*60)
    individual_metric_examples()

    print("\n\n")
    print("="*60)
    print("USAGE: Evaluasi dari file JSON")
    print("="*60)
    print("""
Untuk evaluasi dengan data sesungguhnya:

1. Jalankan sistem untuk generate AI results:
   python rag_grading_improved.py

2. Siapkan file human grading results dengan format yang sama

3. Run evaluation:
   from example_evaluation import evaluate_from_files

   metrics = evaluate_from_files(
       'output/grading_results_20251029_120000.json',
       'data/human_grading_results.json'
   )
    """)
