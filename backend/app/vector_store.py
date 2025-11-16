import faiss
import numpy as np
from typing import List, Dict
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env in the same directory
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Import constants from utils
import os
from dotenv import load_dotenv

# Load environment variables from .env in the same directory
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_EMBED = os.getenv("MODEL_EMBED", "text-embedding-004")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in environment or .env")

genai.configure(api_key=GEMINI_API_KEY)

class FaissStore:
    def __init__(self, dim=1536):
        self.dim = dim
        self.index = None
        self.metadatas = []
        self.texts = []

    def create_index(self):
        self.index = faiss.IndexFlatL2(self.dim)

    def _embed(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts using Gemini."""
        if not texts:
            return np.array([]).astype('float32')
        result = genai.embed_content(
            model=MODEL_EMBED,
            content=texts,
            task_type="retrieval_document"
        )
        embs = result['embedding']
        return np.array(embs).astype('float32')

    def add(self, texts: List[str], metadatas: List[Dict]):
        if self.index is None:
            self.create_index()
        embs = self._embed(texts)
        if embs.size > 0:
            self.index.add(embs)
        self.metadatas.extend(metadatas)
        self.texts.extend(texts)

    def search(self, query: str, k: int = 4):
        """Search the index for the top-k most similar items."""
        if self.index is None or len(self.texts) == 0:
            return []
        q_emb = self._embed([query])
        D, I = self.index.search(q_emb, k)
        results = []
        for idx in I[0]:
            if idx < len(self.metadatas):
                results.append({"metadata": self.metadatas[idx], "text": self.texts[idx]})
        return results

# Single global store instance
store = FaissStore(dim=1536)
