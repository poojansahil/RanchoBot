import streamlit as st
import google.generativeai as genai
import base64
import requests  # 🔹 Added to send webhook requests

# Load API Key from Streamlit Secrets
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

st.set_page_config(page_title="Rancho - Life Advice", layout="centered")

# Set background image using base64
def set_background(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .title-box {{
            background-color: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 2rem;
        }}
        .title-box h1 {{
            color: #000;
            font-size: 2.5rem;
        }}
        .title-box h3 {{
            color: #333;
            font-weight: normal;
        }}
        .chat-bubble {{
            background-color: rgba(255, 255, 255, 0.9);
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            color: #000;
        }}
        .user-question {{
            font-weight: bold;
            color: #000;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

# Apply background
set_background("background.png")

# Title Box
st.markdown("""
<div class="title-box">
    <h1>🤖 Rancho - Life Advice</h1>
    <h3>Ask anything about life. Rancho-style wisdom in &lt;100 words.</h3>
</div>
""", unsafe_allow_html=True)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("💬 Your question:", key="input_text")
    submit = st.form_submit_button("Ask Rancho")

# Handle response
if submit and user_input.strip():
    prompt = f"""
    You are Rancho from the movie 3 Idiots.
    Give a life advice in less than 100 words.
    Keep it wise, witty, and practical like Rancho.
    Question: {user_input}
    Answer:
    """
    with st.spinner("Rancho is thinking..."):
        try:
            response = model.generate_content(prompt)
            answer = response.text.strip()
            st.session_state.chat_history.append((user_input, answer))
        except Exception as e:
            st.error(f"Error: {e}")

# Show chat history
for q, a in st.session_state.chat_history:
    st.markdown(f"""
    <div class="chat-bubble">
        <div class="user-question">You asked:</div>
        <div>{q}</div><br>
        <div class="user-question">Rancho says:</div>
        <div>{a}</div>
    </div>
    """, unsafe_allow_html=True)

# 🔹 ADDITION: Telegram Start Chat Button
if st.button("🚀 Start Chat on Telegram"):
    try:
        webhook_url = "https://n8n-production-cacf.up.railway.app/webhook-test/1f60e267-a7f8-4765-825a-6ba1a1537736"
        response = requests.post(webhook_url)
        if response.status_code == 200:
            st.success("Telegram chat started successfully!")
        else:
            st.error(f"Failed to start Telegram chat. Status: {response.status_code}")
    except Exception as e:
        st.error(f"Error triggering webhook: {e}")
