# TODO: Switch to Gemini API and Fix 422 Error

## Steps to Complete

- [x] Update requirements.txt: replace openai with google-generativeai
- [x] Update utils.py: change OPENAI_API_KEY to GEMINI_API_KEY, set MODEL_CHAT to 'gemini-1.5-flash', MODEL_EMBED to 'text-embedding-004'
- [x] Update ai_assistant.py: switch to use google.generativeai for chat
- [x] Update vector_store.py: switch to use google.generativeai for embeddings
- [x] Update main.py: fix /assistant/chat to accept JSON using Pydantic BaseModel
- [x] Update TODO.md: mark completed steps
- [x] Install new requirements
- [ ] Test the /assistant/chat endpoint
