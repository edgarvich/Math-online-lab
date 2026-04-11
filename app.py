import streamlit as st
import google.generativeai as genai
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np

# Page Configuration
st.set_page_config(page_title="Math-Online-Lab", page_icon="🎓", layout="wide")

# --- API & MODEL SETUP ---
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Missing API Key. Please add GEMINI_API_KEY to your Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# SMART MODEL PICKER: This prevents the 404 error by finding the correct name
@st.cache_resource
def get_model():
    try:
        # We try to find a model that supports 'generateContent'
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'gemini-1.5-flash' in m.name:
                    return genai.GenerativeModel(m.name)
        # Fallback if the list fails
        return genai.GenerativeModel("gemini-1.5-flash")
    except:
        return genai.GenerativeModel("gemini-1.5-flash")

model = get_model()

st.title("Math-Online-Lab 🧠")
st.markdown("---")

# --- LAYOUT ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Interactive Whiteboard")
    st.info("Draw your problem below 👇")
    canvas_result = st_canvas(
        stroke_width=5,
        stroke_color="#000000",
        background_color="#ffffff",
        height=400,
        drawing_mode="freedraw",
        key="canvas",
    )
    
    if st.button("🗑️ Clear Everything"):
        st.rerun()

with col2:
    st.subheader("Tutoring Session")
    
    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Analyze Button
    if st.button("🚀 Analyze & Solve"):
        if canvas_result.image_data is not None:
            # Prepare Image
            img_raw = canvas_result.image_data.astype(np.uint8)
            img = Image.fromarray(img_raw).convert("RGB")
            
            with st.chat_message("assistant"):
                with st.spinner("Analyzing your handwriting..."):
                    try:
                        # Professional System Instruction
                        prompt = (
                            "You are an expert Math Tutor. Analyze the handwritten problem in the image. "
                            "Use scaffolding to guide the student. Do not give the answer immediately. "
                            "Ask the student what the first step should be."
                        )
                        response = model.generate_content([prompt, img])
                        
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                    except Exception as e:
                        st.error(f"Logic Error: {e}")
        else:
            st.warning("Please draw something on the board first!")
