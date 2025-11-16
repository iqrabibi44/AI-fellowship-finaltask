import fitz  # PyMuPDF
from .utils import chunk_text
from typing import List, Tuple, Dict

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    texts = []
    for i, page in enumerate(doc):
        texts.append(page.get_text())
    return "\n\n".join(texts)

def ingest_pdf_bytes(pdf_bytes: bytes, filename: str) -> List[Tuple[str, Dict]]:
    text = extract_text_from_pdf_bytes(pdf_bytes)
    chunks = chunk_text(text, chunk_size=400, overlap=50)
    results = []
    for i, c in enumerate(chunks):
        meta = {"source": filename, "chunk": i}
        results.append((c, meta))
    return results
