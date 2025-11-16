import os
from dotenv import load_dotenv
from typing import List

# Load .env from the same directory as this file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
MODEL_CHAT = os.getenv('MODEL_CHAT', 'gemini-1.5-flash')
MODEL_EMBED = os.getenv('MODEL_EMBED', 'text-embedding-004')

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> List[str]:
    tokens = text.split()
    chunks = []
    i = 0
    while i < len(tokens):
        chunk = tokens[i:i+chunk_size]
        chunks.append(' '.join(chunk))
        i += chunk_size - overlap
    return chunks
