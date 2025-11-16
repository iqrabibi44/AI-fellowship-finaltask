# Shifra AI — Smart Academic Assistant

Shifra AI is an intelligent academic assistant designed to help students and researchers interact with their lecture notes and documents through natural language conversations. The system allows users to upload PDF documents, extract and index their content using vector embeddings, and query the information via a chat interface powered by Google's Gemini AI.

## Features

- **PDF Document Ingestion**: Upload and process PDF files (lecture notes, research papers, textbooks) to extract text and create searchable vector embeddings.
- **Intelligent Chat Assistant**: Engage in conversational AI interactions using Google's Gemini 1.5 Flash model for contextual responses.
- **Vector Search**: Utilize FAISS (Facebook AI Similarity Search) for efficient similarity search across document chunks.
- **Voice Input**: Support for speech-to-text input using Google Speech Recognition.
- **Session Management**: Maintain conversation history and document context across sessions.
- **CORS-Enabled API**: RESTful FastAPI backend with proper CORS configuration for web integration.
- **Responsive Web UI**: Streamlit-based frontend with a clean, academic-focused interface.

## Architecture

### Backend (FastAPI)
- **Endpoints**:
  - `POST /upload_pdf`: Upload and process PDF files
  - `POST /query`: Search indexed documents
  - `GET /assistant/greet`: Get AI assistant greeting
  - `POST /assistant/chat`: Chat with AI assistant
- **Components**:
  - PDF text extraction using PyMuPDF
  - Text chunking with configurable overlap
  - Gemini embeddings for vectorization
  - FAISS index for similarity search
  - Conversation history management

### Frontend (Streamlit)
- Chat interface with message history
- PDF upload with progress feedback
- Voice input capability
- Session state management
- Responsive design with academic theme

## Tech Stack

- **Backend**: Python 3.9+, FastAPI, Uvicorn, FAISS, Google Generative AI (Gemini)
- **Frontend**: Streamlit, Python
- **AI/ML**: Google Gemini 1.5 Flash (chat), Gemini Text Embedding 004 (embeddings)
- **Document Processing**: PyMuPDF (Fitz)
- **Vector Database**: FAISS (in-memory)
- **Speech Recognition**: Google Speech Recognition
- **Deployment**: Railway (backend), Streamlit Cloud (frontend)

## Prerequisites

- Python 3.9 or higher
- Google Gemini API key (get from [Google AI Studio](https://makersuite.google.com/app/apikey))
- Git (for cloning the repository)

## Local Development Setup

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend/app
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create environment file:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your `GEMINI_API_KEY`.

5. Run the backend server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup
1. Open a new terminal and navigate to frontend:
   ```bash
   cd frontend
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

5. Open your browser to `http://localhost:8501`

## Usage

1. **Upload Documents**: Use the upload section to add PDF files containing your lecture notes or study materials.

2. **Chat with AI**: Start a conversation by typing questions or using voice input. The AI can reference uploaded documents in its responses.

3. **Query Documents**: Ask specific questions about your uploaded content, such as "Explain the concept from page 5" or "Summarize the key points from lecture 3".

4. **Voice Interaction**: Click the "Speak" button to use voice input for hands-free interaction.

## Deployment

### Backend (Railway)
1. Sign up at [Railway.app](https://railway.app)
2. Connect your GitHub repository
3. Railway will automatically detect the `railway.json` configuration
4. Set environment variable: `GEMINI_API_KEY=your_api_key_here`
5. Deploy - Railway will provide a production URL

### Frontend (Streamlit Cloud)
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repository
3. Set the `BACKEND_URL` secret to your Railway backend URL
4. Deploy the app

## Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `MODEL_CHAT`: Chat model (default: gemini-1.5-flash)
- `MODEL_EMBED`: Embedding model (default: text-embedding-004)
- `BACKEND_URL`: Backend API URL for frontend (default: localhost:8000)

### Text Chunking
- Chunk size: 400 tokens
- Overlap: 50 tokens
- Adjustable in `utils.py`

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation powered by Swagger UI.

## Troubleshooting

### Common Issues
- **FAISS Installation**: On Windows, FAISS can be tricky. Consider using alternatives like ChromaDB or Pinecone for production.
- **API Key Errors**: Ensure your Gemini API key is valid and has sufficient quota.
- **PDF Processing**: Only PDF files are supported. Ensure files are not corrupted.
- **Voice Input**: Requires microphone access and internet connection for Google Speech Recognition.

### Performance Notes
- Vector search is performed in-memory using FAISS
- Large document collections may require external vector databases
- API rate limits apply to Gemini services

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -am 'Add some feature'`
5. Push to the branch: `git push origin feature/your-feature`
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Generative AI for powering the conversational capabilities
- Facebook AI for FAISS vector search library
- Streamlit for the web framework
- FastAPI for the robust API framework

## Future Enhancements

- Multi-user authentication and session isolation
- Support for additional document formats (DOCX, TXT)
- Persistent vector storage with database integration
- Advanced RAG techniques for better context retrieval
- Integration with learning management systems
- Mobile app companion
