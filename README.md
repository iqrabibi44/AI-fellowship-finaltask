# Shifra AI — Smart Academic Assistant

Shifra AI is an intelligent academic assistant designed to help students and educators interact with lecture notes and documents through natural language conversations. Built as a local MVP, it combines PDF ingestion, vector-based search, and AI-powered chat to provide contextual answers from uploaded academic materials.

## Features

- **PDF Ingestion**: Upload and process PDF documents (e.g., lecture notes) into searchable chunks.
- **Vector Search**: Uses FAISS vector database with Gemini embeddings for efficient semantic search.
- **AI Chat**: Conversational interface powered by Google's Gemini AI model for intelligent responses.
- **Voice Input**: Supports speech-to-text for hands-free interaction.
- **Session Management**: Maintains conversation history and user sessions.
- **Cross-Platform**: Runs locally on Linux, macOS, and Windows (with some dependencies noted).
- **FastAPI Backend**: RESTful API for scalable integrations.
- **Streamlit Frontend**: User-friendly web interface for chat and uploads.

## Architecture

The application consists of two main components:

### Backend (FastAPI)
- **main.py**: Core API endpoints for PDF upload, querying, and AI chat.
- **ai_assistant.py**: Handles AI interactions using Google Generative AI (Gemini).
- **vector_store.py**: Manages FAISS index and embeddings for document search.
- **pdf_ingest.py**: Extracts and chunks text from PDF files using PyMuPDF.
- **utils.py**: Utility functions for text chunking and environment configuration.

### Frontend (Streamlit)
- **streamlit_app.py**: Web interface for chat, voice input, and PDF uploads.
- Integrates with backend via HTTP requests.

### Data Flow
1. PDFs are uploaded via Streamlit and processed into text chunks.
2. Chunks are embedded using Gemini and stored in FAISS index.
3. User queries are embedded and searched against the index.
4. Relevant context is passed to Gemini for generating responses.

## Prerequisites

- Python 3.8+
- Gemini API Key (from Google AI Studio)
- Virtual environment support (venv)

## Installation

1. **Clone or Download the Project**:
   - Unzip the archive and navigate to the project directory: `cd shifraai`

2. **Backend Setup**:
   - Navigate to backend directory: `cd backend/app`
   - Create virtual environment: `python3 -m venv venv`
   - Activate environment:
     - Linux/macOS: `source venv/bin/activate`
     - Windows: `venv\Scripts\activate`
   - Install dependencies: `pip install -r requirements.txt`
   - Configure API key: Copy `.env.example` to `.env` and add your `GEMINI_API_KEY`

3. **Frontend Setup**:
   - Open a new terminal and navigate to frontend: `cd frontend`
   - Create virtual environment: `python3 -m venv venv`
   - Activate environment (same as above)
   - Install dependencies: `pip install -r requirements.txt`

## Usage

1. **Start Backend**:
   - From `backend/app`: `uvicorn main:app --reload --host 0.0.0.0 --port 8000`

2. **Start Frontend**:
   - From `frontend`: `streamlit run streamlit_app.py`

3. **Access Application**:
   - Open Streamlit interface at `http://localhost:8501`
   - Upload PDF documents in the sidebar
   - Chat with the AI assistant, referencing uploaded content

### Example Workflow
- Upload lecture notes PDFs
- Ask questions like: "Explain the concept of X from lecture 3"
- Use voice input for hands-free interaction
- AI responds with context from uploaded documents

## API Endpoints

### PDF Operations
- `POST /upload_pdf`: Upload and index PDF files
  - Parameters: `file` (PDF), `user_id` (string)
  - Returns: Status and number of indexed chunks

- `POST /query`: Search indexed documents
  - Parameters: `session_id` (optional), `user_id`, `query`
  - Returns: Search results and session ID

### AI Assistant
- `GET /assistant/greet`: Get greeting message
  - Returns: Welcome message from AI

- `POST /assistant/chat`: Send message to AI
  - Body: `{"user_input": "Your message"}`
  - Returns: AI response

## Configuration

Environment variables (set in `backend/app/.env`):
- `GEMINI_API_KEY`: Your Google Gemini API key
- `MODEL_CHAT`: Chat model (default: 'gemini-1.5-flash')
- `MODEL_EMBED`: Embedding model (default: 'text-embedding-004')

## Notes

- **Windows Compatibility**: FAISS installation may require additional setup; consider alternatives like ChromaDB for Windows.
- **Security**: This is an MVP for local use. Add authentication and error handling for production.
- **Performance**: Large PDFs may take time to process; optimize chunk sizes as needed.
- **Dependencies**: Ensure all requirements are installed in isolated virtual environments.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes and test locally
4. Submit a pull request

## License

This project is provided as-is for educational and demonstration purposes. See individual component licenses for details.
