import streamlit as st
import google.generativeai as genai
from streamlit_drawable_canvas import st_canvas

# Page Configuration
st.set_page_config(page_title="Math-Online-Lab", page_icon="🎓", layout="wide")

# --- SIDEBAR: Configuration ---
st.sidebar.title("Configuration")
user_api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

# Use Secrets if available, otherwise use manual input
api_key = user_api_key if user_api_key else st.secrets.get("GEMINI_API_KEY")

# Selection of model with the correct 'models/' prefix to avoid the NotFound error
model_option = st.sidebar.selectbox("Select Model:", ["gemini-1.5-flash", "gemini-1.5-pro"])

if not api_key:
    st.warning("⚠️ Please enter your Google AI Studio API Key in the sidebar.")
    st.stop()

# Initialize Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    model_name=f"models/{model_option}",
    system_instruction=(
        "You are an expert Math Tutor. Your goal is to build conceptual reasoning. "
        "Do not provide the answer immediately. Instead, use scaffolding—ask questions "
        "and guide the student step-by-step. Use Markdown for clear math formulas."
    )
)

st.title("Math-Online-Lab 🧠")
st.caption("Interactive Math Tutoring & Digital Whiteboard")

# --- LAYOUT: Whiteboard on Left, Chat on Right ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Interactive Whiteboard")
    st.write("Draw your problem or scratchpad here:")
    
    # Whiteboard Component
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=3,
        stroke_color="#000000",
        background_color="#ffffff",
        height=400,
        drawing_mode="freedraw",
        key="canvas",
    )
    if st.button("Clear Whiteboard"):
        st.rerun()

with col2:
    st.subheader("Math Tutor Chat")
    
    # Initialize Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User Input
    if prompt := st.chat_input("Explain this math concept..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {e}")
