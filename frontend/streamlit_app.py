import streamlit as st
import requests
import os
from uuid import uuid4
import tempfile
import speech_recognition as sr
from PIL import Image

BACKEND = os.environ.get('BACKEND_URL','https://shifra-ai-backend-production.up.railway.app')

st.set_page_config(page_title='Shifra AI', layout='wide')
st.markdown("<h1 style='color:#00FFC6'>🤖 Shifra AI — Smart Academic Assistant</h1>", unsafe_allow_html=True)

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state['session_id'] = None
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = str(uuid4())
if 'assistant_history' not in st.session_state:
    st.session_state['assistant_history'] = []

# Sidebar with robot image and greeting
with st.sidebar:
    st.header("🤖 AI Assistant")
    robot_img = Image.open("robot.png")  # Make sure robot.png exists in the folder
    st.image(robot_img, width=200)
    if st.button("Greet"):
        try:
            resp = requests.get(f"{BACKEND}/assistant/greet", timeout=10)
            message = resp.json()['message']
            st.session_state['assistant_history'].append(("assistant", message))
        except Exception as e:
            st.error(f"Error contacting assistant: {e}")

# Layout
col1, col2 = st.columns([3,1])

with col1:
    st.subheader('Chat with Shifra AI')

    # Display assistant and user messages
    for role, msg in st.session_state['assistant_history']:
        if role == "user":
            st.markdown(f"**You:** {msg}")
        else:
            st.markdown(f"**Shifra AI:** {msg}")

    # User text input
    user_input = st.text_input('Type your message here...')
    if st.button('Send') and user_input.strip():
        st.session_state['assistant_history'].append(("user", user_input))
        try:
            resp = requests.post(
                f"{BACKEND}/assistant/chat",
                json={"user_input": user_input},
                timeout=30
            )
            resp.raise_for_status()
            assistant_msg = resp.json().get('message', '')
            st.session_state['assistant_history'].append(("assistant", assistant_msg))
        except Exception as e:
            st.error(f"Error contacting assistant: {e}")

    # Voice input
    if st.button("Speak"):
        r = sr.Recognizer()
        with st.spinner("Listening..."):
            try:
                with sr.Microphone() as source:
                    audio = r.listen(source, timeout=5, phrase_time_limit=10)
                    user_input_voice = r.recognize_google(audio)
                    st.session_state['assistant_history'].append(("user", user_input_voice))
                    # Send voice text to assistant
                    resp = requests.post(
                        f"{BACKEND}/assistant/chat",
                        json={"user_input": user_input_voice},
                        timeout=30
                    )
                    resp.raise_for_status()
                    assistant_msg = resp.json().get('message', '')
                    st.session_state['assistant_history'].append(("assistant", assistant_msg))
            except Exception as e:
                st.error(f"Voice input error: {e}")

with col2:
    st.header('Uploads')
    uploaded = st.file_uploader('Upload PDFs (lecture notes)', type=['pdf'], accept_multiple_files=True)
    if uploaded:
        for f in uploaded:
            files = {'file': (f.name, f.getvalue(), 'application/pdf')}
            data = {'user_id': st.session_state['user_id']}
            try:
                r = requests.post(f"{BACKEND}/upload_pdf", files=files, data=data)
                if r.ok:
                    st.success(f"Uploaded {f.name} — indexed {r.json().get('added_chunks')} chunks")
                else:
                    st.error(f"Upload failed: {r.text}")
            except Exception as e:
                st.error(f"Upload error: {e}")

    st.header('Session')
    st.write(st.session_state['session_id'])

st.markdown('---')
st.markdown('Tip: upload lecture PDFs, then ask questions referencing them (e.g., "Explain theorem X from lecture 3").')
