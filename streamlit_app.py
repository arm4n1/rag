import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from pathlib import Path
from datetime import datetime
import os
import sys

from rag_grading_improved import Config, BatchProcessor, PDFExtractor, RAGEngine, GradingEngine
from evaluation_metrics import RAGEvaluationMetrics

st.set_page_config(
    page_title="RAG Auto-Grading System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables"""
    if 'grading_results' not in st.session_state:
        st.session_state.grading_results = None
    if 'evaluation_metrics' not in st.session_state:
        st.session_state.evaluation_metrics = None
    if 'human_results' not in st.session_state:
        st.session_state.human_results = None


def sidebar_config():
    """Sidebar for configuration"""
    with st.sidebar:
        st.title("⚙️ Configuration")

        st.subheader("📋 System Info")
        st.info(f"""
        **Model:** {Config.MODEL}
        **Embedding:** {Config.EMBEDDING_MODEL}
        **Chunk Size:** {Config.CHUNK_SIZE}
        **Top-K:** {Config.TOP_K_RETRIEVAL}
        """)

        st.subheader("🔧 Settings")

        chunk_size = st.slider(
            "Chunk Size",
            min_value=500,
            max_value=2000,
            value=Config.CHUNK_SIZE,
            step=100,
            help="Size of text chunks for embedding"
        )

        top_k = st.slider(
            "Top-K Retrieval",
            min_value=3,
            max_value=15,
            value=Config.TOP_K_RETRIEVAL,
            step=1,
            help="Number of evidence chunks to retrieve"
        )

        confidence_threshold = st.slider(
            "Confidence Threshold",
            min_value=0.0,
            max_value=1.0,
            value=Config.MIN_CONFIDENCE_THRESHOLD,
            step=0.05,
            help="Minimum confidence for flagging"
        )

        if chunk_size != Config.CHUNK_SIZE:
            Config.CHUNK_SIZE = chunk_size
        if top_k != Config.TOP_K_RETRIEVAL:
            Config.TOP_K_RETRIEVAL = top_k
        if confidence_threshold != Config.MIN_CONFIDENCE_THRESHOLD:
            Config.MIN_CONFIDENCE_THRESHOLD = confidence_threshold

        st.divider()

        if st.button("🔄 Reset Configuration", use_container_width=True):
            st.cache_data.clear()
            st.rerun()


def home_page():
    """Home page with system overview"""
    st.markdown('<div class="main-header">🎓 RAG Auto-Grading System v2.0</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
    <h3>Sistem Penilaian Otomatis Laporan Praktikum</h3>
    <p>Menggunakan Retrieval-Augmented Generation (RAG) dan Large Language Models</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-card">
        <h4>📄 Upload & Process</h4>
        <p>Upload PDF laporan dan proses dengan AI</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
        <h4>📊 View Results</h4>
        <p>Lihat hasil grading dengan visualisasi</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
        <h4>📈 Evaluation</h4>
        <p>Evaluasi akurasi dengan metrik</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("🚀 Quick Start")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Step 1: Upload PDF Files**
        - Navigate to "📄 Grading" page
        - Upload PDF laporan praktikum
        - Klik "Start Grading"

        **Step 2: View Results**
        - Lihat score summary
        - Detail grading per sub-rubrik
        - Export to Excel/JSON
        """)

    with col2:
        st.markdown("""
        **Step 3: Evaluation (Optional)**
        - Navigate to "📈 Evaluation" page
        - Upload human grading results
        - View accuracy metrics
        - Compare AI vs Human
        """)

    st.divider()

    st.subheader("📊 System Statistics")

    output_folder = Path(Config.OUTPUT_FOLDER)
    if output_folder.exists():
        json_files = list(output_folder.glob("*.json"))
        excel_files = list(output_folder.glob("*.xlsx"))

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Gradings", len(json_files))
        col2.metric("Excel Reports", len(excel_files))
        col3.metric("Data Folder", len(list(Path(Config.DATA_FOLDER).glob("*.pdf"))))
        col4.metric("Model", Config.MODEL.split("/")[-1])
    else:
        st.info("No grading results yet. Start by uploading PDFs!")


def grading_page():
    """Grading page for processing PDFs"""
    st.title("📄 Auto-Grading")

    tab1, tab2 = st.tabs(["Upload & Process", "Batch Processing"])

    with tab1:
        st.subheader("Upload PDF Files")

        uploaded_files = st.file_uploader(
            "Upload PDF laporan praktikum",
            type=['pdf'],
            accept_multiple_files=True,
            help="Upload satu atau lebih file PDF"
        )

        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) uploaded")

            for file in uploaded_files:
                st.write(f"📄 {file.name} ({file.size / 1024:.1f} KB)")

            if st.button("🚀 Start Grading", type="primary", use_container_width=True):
                process_uploaded_files(uploaded_files)

    with tab2:
        st.subheader("Batch Processing from Data Folder")

        data_folder = Path(Config.DATA_FOLDER)
        pdf_files = list(data_folder.glob("*.pdf"))

        if pdf_files:
            st.info(f"Found {len(pdf_files)} PDF files in {Config.DATA_FOLDER}")

            for pdf in pdf_files:
                st.write(f"📄 {pdf.name}")

            if st.button("🚀 Process All PDFs", type="primary", use_container_width=True):
                process_batch_files()
        else:
            st.warning(f"No PDF files found in {Config.DATA_FOLDER}")


def process_uploaded_files(uploaded_files):
    """Process uploaded PDF files"""

    temp_dir = Path("temp_uploads")
    temp_dir.mkdir(exist_ok=True)

    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        rubric_path = Path(Config.RUBRIC_FILE)
        with open(rubric_path, 'r', encoding='utf-8') as f:
            rubric_data = json.load(f)

        results = []

        for idx, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Processing {uploaded_file.name}...")

            temp_path = temp_dir / uploaded_file.name
            with open(temp_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())

            pdf_extractor = PDFExtractor()
            extracted = pdf_extractor.extract_text_with_metadata(str(temp_path))

            if extracted and extracted['text']:
                rag_engine = RAGEngine()
                rag_engine.build_index(extracted['text'])

                grading_engine = GradingEngine()
                grading_result = grading_engine.grade_document(rag_engine, rubric_data)

                grading_result['document_info'] = {
                    'filename': extracted['filename'],
                    'page_count': extracted['page_count'],
                    'metadata': extracted['metadata'],
                    'processed_at': datetime.now().isoformat()
                }

                results.append(grading_result)

            progress_bar.progress((idx + 1) / len(uploaded_files))

        st.session_state.grading_results = results

        status_text.empty()
        progress_bar.empty()

        st.success(f"✅ Successfully graded {len(results)} documents!")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_folder = Path(Config.OUTPUT_FOLDER)
        output_folder.mkdir(exist_ok=True)

        json_path = output_folder / f"grading_results_{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        st.info(f"📄 Results saved to: {json_path}")

        for temp_file in temp_dir.glob("*.pdf"):
            temp_file.unlink()
        temp_dir.rmdir()

    except Exception as e:
        st.error(f"❌ Error during processing: {str(e)}")


def process_batch_files():
    """Process files from data folder"""

    progress_bar = st.progress(0)
    status_text = st.empty()

    try:
        processor = BatchProcessor()

        status_text.text("Loading rubric and scanning files...")

        results = processor.process_folder(Config.DATA_FOLDER, Config.RUBRIC_FILE)

        st.session_state.grading_results = results

        status_text.empty()
        progress_bar.progress(1.0)

        st.success(f"✅ Successfully graded {len(results)} documents!")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_folder = Path(Config.OUTPUT_FOLDER)
        output_folder.mkdir(exist_ok=True)

        json_path = output_folder / f"grading_results_{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        st.info(f"📄 Results saved to: {json_path}")

    except Exception as e:
        st.error(f"❌ Error during processing: {str(e)}")


def results_page():
    """Results page for viewing grading results"""
    st.title("📊 Grading Results")

    if st.session_state.grading_results is None:
        output_folder = Path(Config.OUTPUT_FOLDER)
        if output_folder.exists():
            json_files = sorted(list(output_folder.glob("grading_results_*.json")), reverse=True)

            if json_files:
                st.info("No current results. Load from previous grading?")

                selected_file = st.selectbox(
                    "Select previous results",
                    options=json_files,
                    format_func=lambda x: f"{x.name} ({datetime.fromtimestamp(x.stat().st_mtime).strftime('%Y-%m-%d %H:%M')})"
                )

                if st.button("📂 Load Results"):
                    with open(selected_file, 'r', encoding='utf-8') as f:
                        st.session_state.grading_results = json.load(f)
                    st.rerun()
            else:
                st.warning("No grading results available. Please grade some documents first!")
                return
        else:
            st.warning("No grading results available. Please grade some documents first!")
            return

    results = st.session_state.grading_results

    tab1, tab2, tab3, tab4 = st.tabs(["Summary", "Detailed Scores", "Visualizations", "Export"])

    with tab1:
        show_summary(results)

    with tab2:
        show_detailed_scores(results)

    with tab3:
        show_visualizations(results)

    with tab4:
        show_export_options(results)


def show_summary(results):
    """Show summary statistics"""
    st.subheader("📈 Summary Statistics")

    scores = [r.get('final_score', 0) for r in results]
    confidences = [r.get('overall_confidence', 0) for r in results]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Documents", len(results))
    col2.metric("Average Score", f"{sum(scores)/len(scores):.1f}")
    col3.metric("Avg Confidence", f"{sum(confidences)/len(confidences):.2f}")
    col4.metric("Low Confidence", sum(1 for c in confidences if c < Config.MIN_CONFIDENCE_THRESHOLD))

    st.divider()

    summary_data = []
    for result in results:
        doc_info = result.get('document_info', {})
        summary_data.append({
            'Filename': doc_info.get('filename', 'Unknown'),
            'Kelompok': doc_info.get('metadata', {}).get('kelompok', 'Unknown'),
            'Final Score': result.get('final_score', 0),
            'Confidence': result.get('overall_confidence', 0),
            'Page Count': doc_info.get('page_count', 0),
        })

    df = pd.DataFrame(summary_data)

    st.dataframe(
        df.style.background_gradient(subset=['Final Score'], cmap='RdYlGn')
              .background_gradient(subset=['Confidence'], cmap='Blues'),
        use_container_width=True,
        height=400
    )

    low_conf = [r for r in results if r.get('overall_confidence', 1.0) < Config.MIN_CONFIDENCE_THRESHOLD]
    if low_conf:
        st.warning(f"⚠️ {len(low_conf)} documents have low confidence (< {Config.MIN_CONFIDENCE_THRESHOLD})")
        for r in low_conf:
            doc_info = r.get('document_info', {})
            st.write(f"- {doc_info.get('filename', 'Unknown')}: {r.get('overall_confidence', 0):.3f}")


def show_detailed_scores(results):
    """Show detailed scores per sub-rubric"""
    st.subheader("🔍 Detailed Scores")

    selected_doc = st.selectbox(
        "Select Document",
        options=range(len(results)),
        format_func=lambda i: results[i]['document_info']['filename']
    )

    result = results[selected_doc]
    doc_info = result['document_info']

    st.markdown(f"**Document:** {doc_info['filename']}")
    st.markdown(f"**Pages:** {doc_info['page_count']}")
    st.markdown(f"**Final Score:** {result['final_score']:.1f}/100")
    st.markdown(f"**Confidence:** {result['overall_confidence']:.2f}")

    st.divider()

    for grade in result['grading_result']:
        with st.expander(f"📋 {grade['sub_rubric']} - Level {grade['selected_level']} ({grade['score_awarded']}/100)"):

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Score", f"{grade['score_awarded']}/100")
                st.metric("Weight", f"{grade['weight']}%")

            with col2:
                st.metric("Level", grade['selected_level'])
                st.metric("Confidence", f"{grade.get('confidence', 0):.2f}")

            st.markdown("**Reason:**")
            st.info(grade.get('reason', 'No reason provided'))

            if 'evidence_quote' in grade and grade['evidence_quote']:
                st.markdown("**Evidence:**")
                st.text_area(
                    "Evidence Quote",
                    value=grade['evidence_quote'],
                    height=100,
                    disabled=True,
                    label_visibility="collapsed"
                )


def show_visualizations(results):
    """Show visualizations"""
    st.subheader("📊 Visualizations")

    scores = [r.get('final_score', 0) for r in results]
    confidences = [r.get('overall_confidence', 0) for r in results]
    filenames = [r['document_info']['filename'] for r in results]

    col1, col2 = st.columns(2)

    with col1:
        fig_dist = px.histogram(
            x=scores,
            nbins=10,
            title="Score Distribution",
            labels={'x': 'Score', 'y': 'Count'},
            color_discrete_sequence=['#1f77b4']
        )
        fig_dist.update_layout(showlegend=False)
        st.plotly_chart(fig_dist, use_container_width=True)

    with col2:
        fig_conf = px.histogram(
            x=confidences,
            nbins=10,
            title="Confidence Distribution",
            labels={'x': 'Confidence', 'y': 'Count'},
            color_discrete_sequence=['#ff7f0e']
        )
        fig_conf.update_layout(showlegend=False)
        st.plotly_chart(fig_conf, use_container_width=True)

    fig_bar = px.bar(
        x=filenames,
        y=scores,
        title="Scores by Document",
        labels={'x': 'Document', 'y': 'Score'},
        color=confidences,
        color_continuous_scale='RdYlGn'
    )
    fig_bar.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_bar, use_container_width=True)

    sub_rubric_scores = {}
    for result in results:
        for grade in result['grading_result']:
            sub_name = grade['sub_rubric']
            if sub_name not in sub_rubric_scores:
                sub_rubric_scores[sub_name] = []
            sub_rubric_scores[sub_name].append(grade['score_awarded'])

    fig_box = go.Figure()
    for sub_name, scores in sub_rubric_scores.items():
        fig_box.add_trace(go.Box(y=scores, name=sub_name))

    fig_box.update_layout(
        title="Score Distribution by Sub-Rubric",
        yaxis_title="Score",
        showlegend=True
    )
    st.plotly_chart(fig_box, use_container_width=True)

    fig_scatter = px.scatter(
        x=scores,
        y=confidences,
        title="Score vs Confidence",
        labels={'x': 'Final Score', 'y': 'Confidence'},
        trendline="ols"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)


def show_export_options(results):
    """Show export options"""
    st.subheader("💾 Export Results")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Export to Excel")
        st.write("Generate Excel file with Summary and Detailed sheets")

        if st.button("📊 Generate Excel", use_container_width=True):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_folder = Path(Config.OUTPUT_FOLDER)
            output_folder.mkdir(exist_ok=True)
            excel_path = output_folder / f"grading_results_{timestamp}.xlsx"

            from rag_grading_improved import ReportGenerator
            ReportGenerator.generate_excel_report(results, str(excel_path))

            st.success(f"✅ Excel file generated: {excel_path.name}")

            with open(excel_path, 'rb') as f:
                st.download_button(
                    label="⬇️ Download Excel",
                    data=f,
                    file_name=excel_path.name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

    with col2:
        st.markdown("### Export to JSON")
        st.write("Generate JSON file with raw grading data")

        json_str = json.dumps(results, indent=2, ensure_ascii=False)

        st.download_button(
            label="📄 Download JSON",
            data=json_str,
            file_name=f"grading_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )

    st.divider()

    st.markdown("### Preview Data")

    summary_data = []
    for result in results:
        doc_info = result.get('document_info', {})
        summary_data.append({
            'Filename': doc_info.get('filename', 'Unknown'),
            'Final Score': result.get('final_score', 0),
            'Confidence': result.get('overall_confidence', 0),
        })

    df = pd.DataFrame(summary_data)

    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📑 Download CSV Summary",
        data=csv,
        file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )


def evaluation_page():
    """Evaluation page for comparing AI vs Human grading"""
    st.title("📈 Evaluation & Metrics")

    if st.session_state.grading_results is None:
        st.warning("No AI grading results available. Please grade some documents first!")
        return

    tab1, tab2 = st.tabs(["Upload Human Results", "Evaluation Metrics"])

    with tab1:
        st.subheader("Upload Human Grading Results")

        st.info("""
        Upload a JSON file with human grading results in the same format as AI results.
        This will enable comparison and accuracy metrics.
        """)

        uploaded_file = st.file_uploader(
            "Upload Human Grading JSON",
            type=['json'],
            help="JSON file with human grading results"
        )

        if uploaded_file:
            try:
                human_results = json.load(uploaded_file)
                st.session_state.human_results = human_results
                st.success(f"✅ Loaded {len(human_results)} human grading results")
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")

    with tab2:
        if st.session_state.human_results is None:
            st.info("Upload human grading results to view evaluation metrics")
        else:
            show_evaluation_metrics()


def show_evaluation_metrics():
    """Show evaluation metrics comparing AI vs Human"""
    st.subheader("🎯 Evaluation Metrics")

    ai_results = st.session_state.grading_results
    human_results = st.session_state.human_results

    if len(ai_results) != len(human_results):
        st.warning(f"Mismatch: {len(ai_results)} AI results vs {len(human_results)} human results")
        min_len = min(len(ai_results), len(human_results))
        ai_results = ai_results[:min_len]
        human_results = human_results[:min_len]
        st.info(f"Using first {min_len} results for comparison")

    metrics = RAGEvaluationMetrics.comprehensive_evaluation(ai_results, human_results)

    st.session_state.evaluation_metrics = metrics

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("MAE", f"{metrics['accuracy_metrics']['mae']:.2f}",
                help="Mean Absolute Error (lower is better)")
    col2.metric("RMSE", f"{metrics['accuracy_metrics']['rmse']:.2f}",
                help="Root Mean Squared Error")
    col3.metric("Pearson r", f"{metrics['correlation_metrics']['pearson_r']:.3f}",
                help="Correlation coefficient")
    col4.metric("Cohen's κ", f"{metrics['agreement_metrics']['cohen_kappa']:.3f}",
                help="Inter-rater agreement")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Accuracy Metrics")

        acc = metrics['accuracy_metrics']

        st.metric("Within ±5 points", f"{acc['within_5_points']*100:.1f}%")
        st.metric("Within ±10 points", f"{acc['within_10_points']*100:.1f}%")
        st.metric("Exact Match Rate", f"{acc['exact_match_rate']*100:.1f}%")

        if acc['mae'] < 5:
            st.success("✅ Excellent: MAE < 5")
        elif acc['mae'] < 10:
            st.success("✅ Good: MAE < 10")
        elif acc['mae'] < 15:
            st.warning("⚠️ Acceptable: MAE < 15")
        else:
            st.error("❌ Needs Improvement: MAE > 15")

    with col2:
        st.markdown("### 🎯 Confidence Metrics")

        conf = metrics['confidence_metrics']

        st.metric("Mean Confidence", f"{conf['mean_confidence']:.3f}")
        st.metric("Confidence-Error Correlation", f"{conf['confidence_accuracy_correlation']:.3f}")
        st.metric("Expected Calibration Error", f"{conf['ece']:.3f}")

        if conf['confidence_accuracy_correlation'] < 0:
            st.success("✅ Good: High confidence → Low error")
        else:
            st.warning("⚠️ Confidence not well-calibrated")

    st.divider()

    ai_scores = [r['final_score'] for r in ai_results]
    human_scores = [r['final_score'] for r in human_results]
    errors = [abs(a - h) for a, h in zip(ai_scores, human_scores)]

    col1, col2 = st.columns(2)

    with col1:
        fig_scatter = px.scatter(
            x=human_scores,
            y=ai_scores,
            title="AI vs Human Scores",
            labels={'x': 'Human Score', 'y': 'AI Score'},
            trendline="ols"
        )
        fig_scatter.add_trace(go.Scatter(
            x=[0, 100],
            y=[0, 100],
            mode='lines',
            name='Perfect Agreement',
            line=dict(dash='dash', color='red')
        ))
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col2:
        fig_error = px.histogram(
            x=errors,
            nbins=15,
            title="Error Distribution",
            labels={'x': 'Absolute Error', 'y': 'Count'},
            color_discrete_sequence=['#ff7f0e']
        )
        st.plotly_chart(fig_error, use_container_width=True)

    fig_bland_altman = go.Figure()
    mean_scores = [(a + h) / 2 for a, h in zip(ai_scores, human_scores)]
    diff_scores = [a - h for a, h in zip(ai_scores, human_scores)]

    fig_bland_altman.add_trace(go.Scatter(
        x=mean_scores,
        y=diff_scores,
        mode='markers',
        name='Scores'
    ))

    mean_diff = sum(diff_scores) / len(diff_scores)
    std_diff = (sum((d - mean_diff)**2 for d in diff_scores) / len(diff_scores))**0.5

    fig_bland_altman.add_hline(y=mean_diff, line_dash="dash", line_color="green", annotation_text="Mean")
    fig_bland_altman.add_hline(y=mean_diff + 1.96*std_diff, line_dash="dot", line_color="red", annotation_text="+1.96 SD")
    fig_bland_altman.add_hline(y=mean_diff - 1.96*std_diff, line_dash="dot", line_color="red", annotation_text="-1.96 SD")

    fig_bland_altman.update_layout(
        title="Bland-Altman Plot",
        xaxis_title="Mean of AI and Human Scores",
        yaxis_title="Difference (AI - Human)"
    )
    st.plotly_chart(fig_bland_altman, use_container_width=True)

    st.divider()

    if st.button("📥 Download Evaluation Report"):
        report_json = json.dumps(metrics, indent=2)
        st.download_button(
            label="💾 Download JSON Report",
            data=report_json,
            file_name=f"evaluation_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )


def main():
    """Main application"""
    init_session_state()

    sidebar_config()

    page = st.sidebar.radio(
        "Navigation",
        ["🏠 Home", "📄 Grading", "📊 Results", "📈 Evaluation"],
        label_visibility="collapsed"
    )

    if page == "🏠 Home":
        home_page()
    elif page == "📄 Grading":
        grading_page()
    elif page == "📊 Results":
        results_page()
    elif page == "📈 Evaluation":
        evaluation_page()

    st.sidebar.divider()
    st.sidebar.caption("RAG Auto-Grading System v2.0")
    st.sidebar.caption("Powered by GLM-4.5 & FAISS")


if __name__ == "__main__":
    main()
