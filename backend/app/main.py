from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from uuid import uuid4
import os

# Import your vector store
from .vector_store import store

# Import the AI assistant
from .ai_assistant import assistant

# Import PDF ingestion
from .pdf_ingest import ingest_pdf_bytes

app = FastAPI()

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_input: str

# -----------------------
# PDF Upload and Query Endpoints
# -----------------------
@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...), user_id: str = Form(...)):
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            return {"status": "error", "detail": "Only PDF files are allowed."}

        content = await file.read()

        # Check if file is empty
        if len(content) == 0:
            return {"status": "error", "detail": "Uploaded file is empty."}

        chunks = ingest_pdf_bytes(content, file.filename)
        texts = [t for t, m in chunks]
        metadatas = [m for t, m in chunks]

        if not texts:
            return {"status": "error", "detail": "No text could be extracted from the PDF."}

        store.add(texts, metadatas)
        return {"status": "success", "added_chunks": len(texts)}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.post("/query")
async def query(session_id: str = Form(None), user_id: str = Form(...), query: str = Form(...)):
    try:
        results = store.search(query, k=4)
        answer_text = "\n".join([r['text'] for r in results])
        new_session_id = session_id or str(uuid4())
        return {"session_id": new_session_id, "answer": answer_text}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

# -----------------------
# AI Assistant Endpoints
# -----------------------
@app.get("/assistant/greet")
def greet():
    """Return greeting message from AI assistant"""
    try:
        message = assistant.greet()
        return {"message": message}
    except Exception as e:
        return {"message": f"Error: {e}"}

@app.post("/assistant/chat")
def chat(request: ChatRequest):
    """Send user input to AI assistant and return response"""
    try:
        response = assistant.chat(request.user_input)
        return {"message": response}
    except Exception as e:
        print(f"Chat endpoint error: {e}")
        import traceback
        traceback.print_exc()
        return {"message": f"Error: {e}"}
