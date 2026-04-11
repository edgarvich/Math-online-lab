import streamlit as st
import google.generativeai as genai

# Page Setup
st.set_page_config(page_title="Math-Online-Lab", page_icon="🎓")

# Sidebar for API Key & Model Selection
st.sidebar.title("Configuration")
user_api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

# Fallback to Streamlit Secrets if available
api_key = user_api_key if user_api_key else st.secrets.get("GEMINI_API_KEY")

model_name = st.sidebar.selectbox("Model:", ["gemini-1.5-flash", "gemini-1.5-pro"])

if not api_key:
    st.warning("⚠️ Please enter your Google AI Studio API Key in the sidebar to start.")
    st.stop()

# Initialize Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    model_name=model_name,
    system_instruction="You are an expert Math Tutor. Focus on conceptual reasoning. Don't give answers immediately; provide step-by-step scaffolding."
)

st.title("Math-Online-Lab 🧠")
st.markdown("---")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if prompt := st.chat_input("Ask a math question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
