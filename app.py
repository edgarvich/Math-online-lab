import streamlit as st
import google.generativeai as genai
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np

# Page Configuration
st.set_page_config(page_title="Math-Online-Lab", page_icon="🎓", layout="wide")

# --- SECRET & API SETUP ---
# This looks for the key in Streamlit Secrets first so you don't have to type it!
api_key = st.secrets.get("GEMINI_API_KEY")

# Sidebar Configuration
st.sidebar.title("Configuration")

# If the secret isn't found, show the manual input box
if not api_key:
    api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")
    if not api_key:
        st.warning("⚠️ Please add GEMINI_API_KEY to your Streamlit Secrets or enter it here.")
        st.stop()
else:
    st.sidebar.success("✅ API Key loaded automatically!")

model_option = st.sidebar.selectbox("Select Model:", ["gemini-1.5-flash", "gemini-1.5-pro"])

# Initialize Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name=model_option)

st.title("Math-Online-Lab 🧠")
st.caption("Interactive Math Tutoring with Visual Recognition")

# --- LAYOUT ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Interactive Whiteboard")
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=4,
        stroke_color="#000000",
        background_color="#ffffff",
        height=400,
        drawing_mode="freedraw",
        key="canvas",
    )
    
    send_whiteboard = st.button("📤 Send Whiteboard to AI")
    if st.button("🗑️ Clear Board"):
        st.rerun()

with col2:
    st.subheader("Math Tutor Chat")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask a question about your drawing...")

    if send_whiteboard or prompt:
        user_content = []
        if canvas_result.image_data is not None:
            img_data = canvas_result.image_data.astype(np.uint8)
            img = Image.fromarray(img_data).convert("RGB")
            user_content.append(img)
        
        text_query = prompt if prompt else "Analyze the math problem I drew and guide me step-by-step."
        user_content.append(text_query)

        st.session_state.messages.append({"role": "user", "content": text_query})
        with st.chat_message("user"):
            st.markdown(text_query)

        with st.chat_message("assistant"):
            try:
                response = model.generate_content(user_content)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {e}")
