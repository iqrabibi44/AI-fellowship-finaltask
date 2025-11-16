import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env in the same directory
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_CHAT = os.getenv('MODEL_CHAT', 'gemini-1.5-flash')

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in environment or .env")

genai.configure(api_key=GEMINI_API_KEY)

class AIAssistant:
    def __init__(self):
        if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
            self.error_msg = "GEMINI_API_KEY not configured. Please add a valid API key to .env"
            self.model = None
        else:
            self.error_msg = None
            self.model = genai.GenerativeModel(MODEL_CHAT)
        self.history = []  # conversation history

    def greet(self):
        if self.error_msg:
            return self.error_msg
        return "Hi! I am your AI assistant. How can I help you today?"

    def chat(self, user_input: str):
        """Send user input to Gemini API and get response"""
        if self.error_msg:
            return self.error_msg
            
        self.history.append({"role": "user", "content": user_input})

        try:
            # Prepare history for Gemini (Gemini uses different format)
            messages = []
            for msg in self.history:
                if msg["role"] == "user":
                    messages.append(f"User: {msg['content']}")
                else:
                    messages.append(f"Assistant: {msg['content']}")
            prompt = "\n".join(messages)

            response = self.model.generate_content(prompt)
            assistant_msg = response.text

            # Update history
            self.history.append({"role": "assistant", "content": assistant_msg})
            return assistant_msg

        except Exception as e:
            error_msg = f"Error contacting Gemini API: {str(e)}"
            print(f"Chat error: {error_msg}")
            return error_msg

# Single global assistant instance
assistant = AIAssistant()
