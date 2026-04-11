import streamlit as st
import google.generativeai as genai
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np

# 1. Page Config
st.set_page_config(page_title="Math Lab", layout="wide")

# 2. API Key from Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Please add GEMINI_API_KEY to Streamlit Secrets.")
    st.stop()

# 3. Configure AI
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("Math-Online-Lab 🎓")

# 4. Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Whiteboard")
    canvas_result = st_canvas(
        stroke_width=4,
        stroke_color="#000000",
        background_color="#ffffff",
        height=400,
        drawing_mode="freedraw",
        key="canvas",
    )
    send_btn = st.button("Analyze Drawing")

with col2:
    st.subheader("Tutor")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    if send_btn and canvas_result.image_data is not None:
        # Convert drawing to image
        img = Image.fromarray(canvas_result.image_data.astype(np.uint8)).convert("RGB")
        
        with st.chat_message("assistant"):
            try:
                response = model.generate_content(["Solve this math problem step-by-step as a tutor.", img])
                st.markdown(response.text)
                st.session_state.chat_history.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {e}")
