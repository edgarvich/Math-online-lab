import streamlit as st
import google.generativeai as genai
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np

# Page Configuration
st.set_page_config(page_title="Math-Online-Lab", page_icon="🎓", layout="wide")

# --- SIDEBAR: Configuration ---
st.sidebar.title("Configuration")
user_api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")
api_key = user_api_key if user_api_key else st.secrets.get("GEMINI_API_KEY")
model_option = st.sidebar.selectbox("Select Model:", ["gemini-1.5-flash", "gemini-1.5-pro"])

if not api_key:
    st.warning("⚠️ Please enter your API Key in the sidebar.")
    st.stop()

# Initialize Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name=f"models/{model_option}")

st.title("Math-Online-Lab 🧠")
st.caption("Interactive Math Tutoring with Visual Recognition")

# --- LAYOUT ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Interactive Whiteboard")
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=3,
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

    # Handle Text Input
    prompt = st.chat_input("Ask a question about your drawing...")

    # LOGIC: If user sends whiteboard OR types a message
    if send_whiteboard or prompt:
        user_content = []
        
        # 1. Process the image if it exists
        if canvas_result.image_data is not None:
            # Convert canvas data to a PIL Image
            img_data = canvas_result.image_data.astype(np.uint8)
            img = Image.fromarray(img_data).convert("RGB")
            user_content.append(img)
        
        # 2. Process text prompt
        text_query = prompt if prompt else "Please analyze the math problem I drew on the whiteboard. Help me solve it step-by-step."
        user_content.append(text_query)

        # Update UI for user
        st.session_state.messages.append({"role": "user", "content": text_query})
        with st.chat_message("user"):
            st.markdown(text_query)

        # 3. Get AI Response
        with st.chat_message("assistant"):
            try:
                # System instructions embedded in the call
                instruction = "Act as a math tutor. Use scaffolding. Do not give the answer immediately. Analyze the provided image if available."
                response = model.generate_content([instruction] + user_content)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {e}")
