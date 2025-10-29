import os
import json
import numpy as np
import faiss
import requests
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Konfigurasi sistem grading - loaded from .env file"""

    OPENROUTER_KEY = os.getenv("OPENROUTER_KEY", "")
    OPENROUTER_URL = os.getenv("OPENROUTER_URL", "https://openrouter.ai/api/v1/chat/completions")
    MODEL = os.getenv("MODEL", "z-ai/glm-4.5")

    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
    TOP_K_RETRIEVAL = int(os.getenv("TOP_K_RETRIEVAL", "5"))
    SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.65"))

    MIN_CONFIDENCE_THRESHOLD = 0.6
    TEMPERATURE = 0.0

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "rag_system.log")

    DATA_FOLDER = "data"
    OUTPUT_FOLDER = "output"
    RUBRIC_FILE = "data/rubrik.json"

    @classmethod
    def validate(cls):
        """Validate configuration"""
        errors = []

        if not cls.OPENROUTER_KEY:
            errors.append("OPENROUTER_KEY tidak ditemukan di .env file")

        if cls.CHUNK_SIZE <= 0:
            errors.append(f"CHUNK_SIZE harus > 0, got {cls.CHUNK_SIZE}")

        if cls.CHUNK_OVERLAP < 0 or cls.CHUNK_OVERLAP >= cls.CHUNK_SIZE:
            errors.append(f"CHUNK_OVERLAP harus antara 0 dan CHUNK_SIZE")

        if cls.TOP_K_RETRIEVAL <= 0:
            errors.append(f"TOP_K_RETRIEVAL harus > 0, got {cls.TOP_K_RETRIEVAL}")

        if not (0 <= cls.SIMILARITY_THRESHOLD <= 1):
            errors.append(f"SIMILARITY_THRESHOLD harus antara 0 dan 1")

        return errors

    @classmethod
    def print_config(cls):
        """Print current configuration"""
        print("\n" + "="*60)
        print("KONFIGURASI SISTEM (dari .env)")
        print("="*60)
        print(f"Model: {cls.MODEL}")
        print(f"Embedding Model: {cls.EMBEDDING_MODEL}")
        print(f"Chunk Size: {cls.CHUNK_SIZE}")
        print(f"Chunk Overlap: {cls.CHUNK_OVERLAP}")
        print(f"Top-K Retrieval: {cls.TOP_K_RETRIEVAL}")
        print(f"Similarity Threshold: {cls.SIMILARITY_THRESHOLD}")
        print(f"Log Level: {cls.LOG_LEVEL}")
        print(f"Log File: {cls.LOG_FILE}")
        print("="*60)


def setup_logging():
    """Setup logging configuration from Config"""
    log_level = getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = logging.FileHandler(Config.LOG_FILE, encoding='utf-8')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(log_level)

    logger.handlers.clear()

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logging.info("="*60)
    logging.info("RAG AUTO-GRADING SYSTEM v2.0 - Session Started")
    logging.info("="*60)

    return logger


class PDFExtractor:
    """Ekstraksi teks dari PDF dengan metadata"""

    @staticmethod
    def extract_text_with_metadata(pdf_path: str) -> Dict:
        """
        Ekstrak teks dan metadata dari PDF

        Returns:
            Dict dengan keys: text, filename, page_count, metadata
        """
        try:
            logging.info(f"Extracting PDF: {pdf_path}")
            reader = PdfReader(pdf_path)
            pages = []

            for i, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                if text.strip():
                    pages.append({
                        'page_num': i + 1,
                        'text': text.strip()
                    })

            full_text = "\n".join([p['text'] for p in pages])

            filename = Path(pdf_path).stem
            metadata = PDFExtractor._extract_metadata_from_text(full_text, filename)

            logging.info(f"Successfully extracted {len(pages)} pages from {filename}")
            logging.debug(f"Total text length: {len(full_text)} characters")

            return {
                'text': full_text,
                'filename': filename,
                'page_count': len(pages),
                'pages': pages,
                'metadata': metadata
            }
        except Exception as e:
            logging.error(f"Error extracting {pdf_path}: {e}", exc_info=True)
            print(f"⚠️ Error extracting {pdf_path}: {e}")
            return None

    @staticmethod
    def _extract_metadata_from_text(text: str, filename: str) -> Dict:
        """Ekstrak metadata seperti nama kelompok, NIM, dll dari teks"""
        metadata = {
            'kelompok': filename,
            'extracted_from': 'filename'
        }

        lines = text.split('\n')[:20]

        for line in lines:
            line_lower = line.lower()
            if 'kelompok' in line_lower:
                metadata['kelompok'] = line.strip()
            elif 'nim' in line_lower:
                metadata['nim'] = line.strip()
            elif 'nama' in line_lower and 'kelompok' not in line_lower:
                metadata['nama'] = line.strip()

        return metadata


class RAGEngine:
    """RAG Engine dengan FAISS untuk retrieval"""

    def __init__(self, model_name: str = Config.EMBEDDING_MODEL):
        self.embedder = SentenceTransformer(model_name)
        self.index = None
        self.chunks = []
        self.chunk_metadata = []

    def build_index(self, text: str, chunk_size: int = Config.CHUNK_SIZE,
                    chunk_overlap: int = Config.CHUNK_OVERLAP):
        """Build FAISS index dari teks"""
        logging.info(f"Building FAISS index with chunk_size={chunk_size}, overlap={chunk_overlap}")

        self.chunks = self._chunk_text(text, chunk_size, chunk_overlap)

        if not self.chunks:
            logging.warning("No chunks created from text")
            print("⚠️ Tidak ada chunks yang dibuat")
            return

        logging.info(f"Created {len(self.chunks)} chunks from text")

        print(f"📝 Membuat embeddings untuk {len(self.chunks)} chunks...")
        logging.info(f"Generating embeddings using model: {self.embedder}")

        embeddings = self.embedder.encode(
            self.chunks,
            convert_to_numpy=True,
            show_progress_bar=False
        )
        embeddings = np.asarray(embeddings, dtype=np.float32)

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

        logging.info(f"FAISS index built successfully with {self.index.ntotal} vectors, dimension={dim}")
        print(f"✅ Index berhasil dibuat dengan {self.index.ntotal} vectors")

    def search(self, query: str, k: int = Config.TOP_K_RETRIEVAL) -> List[str]:
        """Search relevant chunks"""
        if self.index is None or self.index.ntotal == 0:
            return []

        k = min(k, self.index.ntotal)
        q_emb = self.embedder.encode([query], convert_to_numpy=True)
        q_emb = np.asarray(q_emb, dtype=np.float32)

        D, I = self.index.search(q_emb, k)
        return [self.chunks[i] for i in I[0] if i < len(self.chunks)]

    def search_multi_query(self, queries: List[str], k: int = 3) -> List[str]:
        """
        Search dengan multiple queries dan gabungkan hasilnya
        Berguna untuk mendapatkan evidence lebih comprehensive
        """
        all_results = []
        seen = set()

        for query in queries:
            results = self.search(query, k)
            for result in results:
                if result not in seen:
                    all_results.append(result)
                    seen.add(result)

        return all_results

    def _chunk_text(self, text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
        """Chunk text dengan RecursiveCharacterTextSplitter"""
        if not text or not text.strip():
            return []

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        chunks = splitter.split_text(text)
        return [c.strip() for c in chunks if c and c.strip()]


class GradingEngine:
    """Engine untuk grading menggunakan LLM"""

    def __init__(self, config: Config = Config()):
        self.config = config

    def grade_document(self, rag_engine: RAGEngine, rubric_data: Dict) -> Dict:
        """
        Grade satu dokumen berdasarkan rubrik

        Returns:
            Dict berisi hasil grading
        """
        print("\n🎯 Mulai proses grading...")
        logging.info("Starting grading process")

        sub_rubrics = rubric_data.get('sub_rubrics', [])
        logging.info(f"Processing {len(sub_rubrics)} sub-rubrics")

        evidence_map = {}
        for sub_rubric in sub_rubrics:
            queries = self._build_queries_for_subrubric(sub_rubric)
            logging.debug(f"Searching evidence for sub-rubric: {sub_rubric['name']}")
            evidence = rag_engine.search_multi_query(queries, k=3)
            evidence_map[sub_rubric['name']] = evidence
            logging.debug(f"Found {len(evidence)} evidence chunks for {sub_rubric['name']}")

        all_evidence = []
        for name, chunks in evidence_map.items():
            all_evidence.extend(chunks)

        seen = set()
        unique_evidence = []
        for item in all_evidence:
            if item not in seen:
                unique_evidence.append(item)
                seen.add(item)

        evidence_text = "\n\n---\n\n".join(unique_evidence[:10])
        logging.info(f"Collected {len(unique_evidence)} unique evidence chunks")

        prompt = self._build_grading_prompt(rubric_data, evidence_text)
        logging.debug(f"Prompt length: {len(prompt)} characters")

        print("🤖 Mengirim ke LLM untuk penilaian...")
        response = self._call_llm(prompt)

        result = self._parse_grading_response(response, rubric_data)
        logging.info(f"Grading completed. Final score: {result.get('final_score', 0)}")

        return result

    def _build_queries_for_subrubric(self, sub_rubric: Dict) -> List[str]:
        """Build multiple queries untuk satu sub-rubrik"""
        name = sub_rubric['name']
        description = sub_rubric.get('description', '')

        queries = [
            f"Cari bagian tentang {name}",
            f"{description}",
            f"Evidence untuk menilai {name}",
        ]

        return queries

    def _build_grading_prompt(self, rubric_data: Dict, evidence: str) -> str:
        """Build prompt untuk LLM"""
        rubric_json = json.dumps(rubric_data, indent=2, ensure_ascii=False)

        return f"""
Anda adalah sistem auto-grading untuk Learning Management System (LMS).
Tugas Anda adalah menilai laporan mahasiswa berdasarkan **rubrik penilaian (JSON)** dan **evidence dari hasil pencarian dokumen (RAG)**.

Gunakan *hanya informasi dari evidence di bawah ini* sebagai dasar penilaian.
JANGAN mengarang isi di luar evidence.

---

### 📘 RUBRIK PENILAIAN (JSON)
{rubric_json}

---

### 📄 EVIDENCE DARI LAPORAN (hasil pencarian RAG)
Gunakan bagian-bagian teks berikut untuk mendukung setiap penilaian:
{evidence}

---

### 📋 INSTRUKSI PENILAIAN
1. Evaluasi **SEMUA sub-rubrik** yang ada pada rubrik JSON, jangan ada yang dilewatkan.
2. Setiap level memiliki rentang nilai (`score_range`). Pilih **nilai numerik** dalam rentang itu, bukan hanya ujungnya.
   - Contoh: jika sesuai level B (61–80), boleh kasih 70 atau 75 tergantung kualitas.
   - Jika isi tidak mencukupi, tetap tampilkan sub-rubrik tersebut dengan level terendah dan beri alasan.
3. Gunakan bukti dari bagian *Evidence* di atas untuk setiap keputusan penilaian.
   - Jika ada kalimat pendukung, sebutkan ringkas potongan teks evidence yang relevan.
4. Sertakan alasan singkat (1–3 kalimat) yang berdasarkan evidence.
5. Cantumkan bobot (`assignment_sub_rubrics.weight`).
6. Hitung nilai total berdasarkan skor × bobot.
7. Tambahkan confidence score untuk setiap sub-rubrik dan keseluruhan (`overall_confidence`).

---

### 📤 FORMAT OUTPUT WAJIB (JSON)
Jawaban akhir **HARUS** mengikuti struktur JSON berikut:

{{
  "grading_result": [
    {{
      "sub_rubric": "Nama Sub Rubrik",
      "selected_level": "A/B/C/...",
      "score_awarded": 0-100,
      "weight": 0-100,
      "reason": "alasan singkat berdasarkan evidence",
      "evidence_quote": "potongan teks relevan dari evidence",
      "confidence": 0.0-1.0
    }}
  ],
  "final_score": 0-100,
  "overall_confidence": 0.0-1.0
}}

Output tidak boleh berisi penjelasan tambahan di luar struktur JSON.
"""

    def _call_llm(self, prompt: str) -> str:
        """Call LLM via OpenRouter"""
        logging.info(f"Calling LLM API: {self.config.MODEL}")
        logging.debug(f"API URL: {self.config.OPENROUTER_URL}")

        headers = {
            "Authorization": f"Bearer {self.config.OPENROUTER_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.config.MODEL,
            "messages": [
                {"role": "system", "content": "Kamu adalah sistem penilai otomatis. Jawab hanya dalam format JSON."},
                {"role": "user", "content": prompt},
            ],
            "temperature": self.config.TEMPERATURE,
        }

        try:
            logging.debug("Sending request to OpenRouter API...")
            r = requests.post(
                self.config.OPENROUTER_URL,
                headers=headers,
                json=payload,
                timeout=120
            )
            r.raise_for_status()
            data = r.json()

            response = data["choices"][0]["message"]["content"]
            logging.info(f"Received LLM response, length: {len(response)} characters")
            logging.debug(f"Response preview: {response[:200]}...")

            return response
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {e}", exc_info=True)
            print(f"⚠️ Gagal memanggil LLM: {e}")
            return "{}"
        except Exception as e:
            logging.error(f"Unexpected error calling LLM: {e}", exc_info=True)
            print(f"⚠️ Gagal memanggil LLM: {e}")
            return "{}"

    def _parse_grading_response(self, response: str, rubric_data: Dict) -> Dict:
        """Parse response dari LLM"""
        try:
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]

            result = json.loads(response.strip())

            assignment_sub_rubrics = {
                sr['sub_rubric_id']: sr['weight']
                for sr in rubric_data.get('assignment_sub_rubrics', [])
            }

            sub_rubrics = {
                sr['id']: sr
                for sr in rubric_data.get('sub_rubrics', [])
            }

            for grade in result.get('grading_result', []):
                sub_name = grade['sub_rubric']
                for sr_id, sr in sub_rubrics.items():
                    if sr['name'] == sub_name:
                        weight = assignment_sub_rubrics.get(sr_id, 0)
                        grade['weight'] = weight
                        break

            return result
        except Exception as e:
            print(f"⚠️ Error parsing LLM response: {e}")
            print(f"Response: {response[:500]}...")
            return {
                "grading_result": [],
                "final_score": 0,
                "overall_confidence": 0.0,
                "error": str(e)
            }


class BatchProcessor:
    """Batch processing untuk multiple PDFs"""

    def __init__(self, config: Config = Config()):
        self.config = config
        self.pdf_extractor = PDFExtractor()
        self.grading_engine = GradingEngine(config)

    def process_folder(self, folder_path: str, rubric_path: str) -> List[Dict]:
        """
        Process semua PDF di folder

        Returns:
            List of grading results
        """
        with open(rubric_path, 'r', encoding='utf-8') as f:
            rubric_data = json.load(f)

        pdf_files = list(Path(folder_path).glob("*.pdf"))

        if not pdf_files:
            print(f"⚠️ Tidak ada PDF ditemukan di {folder_path}")
            return []

        print(f"\n📂 Ditemukan {len(pdf_files)} PDF untuk diproses")

        results = []

        for pdf_file in tqdm(pdf_files, desc="Processing PDFs"):
            print(f"\n{'='*60}")
            print(f"📄 Processing: {pdf_file.name}")
            print(f"{'='*60}")

            extracted = self.pdf_extractor.extract_text_with_metadata(str(pdf_file))

            if not extracted or not extracted['text']:
                print(f"⚠️ Gagal ekstrak atau PDF kosong: {pdf_file.name}")
                continue

            print(f"✅ Ekstraksi berhasil: {extracted['page_count']} halaman")

            rag_engine = RAGEngine()
            rag_engine.build_index(extracted['text'])

            grading_result = self.grading_engine.grade_document(rag_engine, rubric_data)

            grading_result['document_info'] = {
                'filename': extracted['filename'],
                'page_count': extracted['page_count'],
                'metadata': extracted['metadata'],
                'processed_at': datetime.now().isoformat()
            }

            results.append(grading_result)

            print(f"✅ Score: {grading_result.get('final_score', 0):.1f}")
            print(f"   Confidence: {grading_result.get('overall_confidence', 0):.2f}")

        return results


class ReportGenerator:
    """Generate various report formats"""

    @staticmethod
    def generate_excel_report(results: List[Dict], output_path: str):
        """Generate Excel report dengan multiple sheets"""
        print(f"\n📊 Generating Excel report...")
        logging.info(f"Generating Excel report to: {output_path}")

        summary_data = []
        for result in results:
            doc_info = result.get('document_info', {})
            summary_data.append({
                'Filename': doc_info.get('filename', 'Unknown'),
                'Kelompok': doc_info.get('metadata', {}).get('kelompok', 'Unknown'),
                'Final Score': result.get('final_score', 0),
                'Confidence': result.get('overall_confidence', 0),
                'Page Count': doc_info.get('page_count', 0),
                'Processed At': doc_info.get('processed_at', '')
            })

        df_summary = pd.DataFrame(summary_data)

        detailed_data = []
        for result in results:
            doc_info = result.get('document_info', {})
            filename = doc_info.get('filename', 'Unknown')

            for grade in result.get('grading_result', []):
                detailed_data.append({
                    'Filename': filename,
                    'Sub Rubric': grade.get('sub_rubric', ''),
                    'Level': grade.get('selected_level', ''),
                    'Score': grade.get('score_awarded', 0),
                    'Weight': grade.get('weight', 0),
                    'Confidence': grade.get('confidence', 0),
                    'Reason': grade.get('reason', ''),
                    'Evidence Quote': grade.get('evidence_quote', '')[:100] + '...'
                })

        df_detailed = pd.DataFrame(detailed_data)

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df_summary.to_excel(writer, sheet_name='Summary', index=False)
            df_detailed.to_excel(writer, sheet_name='Detailed Scores', index=False)

        print(f"✅ Excel report saved: {output_path}")

    @staticmethod
    def generate_json_report(results: List[Dict], output_path: str):
        """Generate JSON report"""
        print(f"\n📄 Generating JSON report...")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"✅ JSON report saved: {output_path}")

    @staticmethod
    def print_summary_statistics(results: List[Dict]):
        """Print summary statistics"""
        if not results:
            print("No results to summarize")
            return

        scores = [r.get('final_score', 0) for r in results]
        confidences = [r.get('overall_confidence', 0) for r in results]

        print(f"\n{'='*60}")
        print(f"📊 SUMMARY STATISTICS")
        print(f"{'='*60}")
        print(f"Total Documents: {len(results)}")
        print(f"\nScores:")
        print(f"  Mean:   {np.mean(scores):.2f}")
        print(f"  Median: {np.median(scores):.2f}")
        print(f"  Std:    {np.std(scores):.2f}")
        print(f"  Min:    {np.min(scores):.2f}")
        print(f"  Max:    {np.max(scores):.2f}")
        print(f"\nConfidence:")
        print(f"  Mean:   {np.mean(confidences):.3f}")
        print(f"  Median: {np.median(confidences):.3f}")

        low_conf = [r for r in results if r.get('overall_confidence', 1.0) < Config.MIN_CONFIDENCE_THRESHOLD]
        if low_conf:
            print(f"\n⚠️ {len(low_conf)} dokumen dengan confidence rendah (<{Config.MIN_CONFIDENCE_THRESHOLD}):")
            for r in low_conf:
                doc_info = r.get('document_info', {})
                print(f"   - {doc_info.get('filename', 'Unknown')}: {r.get('overall_confidence', 0):.3f}")


def main():
    """Main execution function"""
    print(f"""
╔══════════════════════════════════════════════════════════╗
║     RAG AUTO-GRADING SYSTEM v2.0                        ║
║     Sistem Penilaian Otomatis Laporan Praktikum        ║
╚══════════════════════════════════════════════════════════╝
""")

    setup_logging()

    logging.info("Validating configuration from .env file...")
    errors = Config.validate()

    if errors:
        logging.error("Configuration validation failed:")
        for error in errors:
            logging.error(f"  - {error}")
            print(f"❌ {error}")
        print("\n⚠️ Pastikan file .env sudah benar dan lengkap!")
        return

    logging.info("Configuration validation passed")

    Config.print_config()

    output_folder = Path(Config.OUTPUT_FOLDER)
    output_folder.mkdir(exist_ok=True)
    logging.info(f"Output folder created/verified: {output_folder.absolute()}")

    processor = BatchProcessor()

    print(f"\n🚀 Memulai batch processing...")
    logging.info("Starting batch processing...")
    results = processor.process_folder(Config.DATA_FOLDER, Config.RUBRIC_FILE)

    if not results:
        print("❌ Tidak ada hasil yang dihasilkan")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    excel_path = output_folder / f"grading_results_{timestamp}.xlsx"
    ReportGenerator.generate_excel_report(results, str(excel_path))

    json_path = output_folder / f"grading_results_{timestamp}.json"
    ReportGenerator.generate_json_report(results, str(json_path))

    ReportGenerator.print_summary_statistics(results)

    print(f"\n{'='*60}")
    print(f"✅ SELESAI!")
    print(f"{'='*60}")
    print(f"📁 Output folder: {output_folder.absolute()}")
    print(f"📊 Excel report: {excel_path.name}")
    print(f"📄 JSON report: {json_path.name}")
    print(f"\n💡 Tip: Buka Excel report untuk melihat detail lengkap penilaian")


if __name__ == "__main__":
    main()
