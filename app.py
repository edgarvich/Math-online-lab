import streamlit as st
import google.generativeai as genai
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np

# Page Configuration
st.set_page_config(page_title="Math-Online-Lab", page_icon="🎓", layout="wide")

# --- API SETUP ---
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.sidebar.title("Configuration")
    api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")
    if not api_key:
        st.warning("⚠️ Please add GEMINI_API_KEY to your Streamlit Secrets.")
        st.stop()

genai.configure(api_key=api_key)

# --- THE "UNIVERSAL" MODEL FIX ---
# This list covers all possible naming conventions to stop the 404 error
model_options = ["gemini-1.5-flash", "models/gemini-1.5-flash", "gemini-1.5-pro", "models/gemini-1.5-pro"]
selected_base = st.sidebar.selectbox("Select Model:", ["gemini-1.5-flash", "gemini-1.5-pro"])

# We attempt to initialize the model. If it fails, we try the alternative prefix.
try:
    model = genai.GenerativeModel(model_name=selected_base)
    # Test a tiny call to verify the name is accepted by the server
    model.generate_content("test")
except Exception:
    try:
        model = genai.GenerativeModel(model_name=f"models/{selected_base}")
    except Exception as e:
        st.error(f"Critical Connection Error: {e}")
        st.stop()

st.title("Math-Online-Lab 🧠")
st.caption("Interactive Math Tutoring with Visual Recognition")

# --- LAYOUT ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Interactive Whiteboard")
    canvas_result = st_canvas(
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
        
        text_query = prompt if prompt else "Analyze the math problem I drew. Help me solve it step-by-step."
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
                st.error(f"AI Error: {e}")
