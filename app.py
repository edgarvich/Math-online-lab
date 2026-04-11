import streamlit as st
import google.generativeai as genai
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np

# Configuración básica
st.set_page_config(page_title="Math Lab", layout="wide")

# Verificación de la llave
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Configura GEMINI_API_KEY en los Secrets de Streamlit.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Inicialización del modelo (Sin prefijos complicados)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("Math-Online-Lab 🎓")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Pizarra")
    canvas_result = st_canvas(
        stroke_width=5, stroke_color="#000000", background_color="#ffffff",
        height=400, drawing_mode="freedraw", key="canvas",
    )
    analyze_btn = st.button("🚀 Analizar")

with col2:
    st.subheader("Tutoría")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    if analyze_btn and canvas_result.image_data is not None:
        img = Image.fromarray(canvas_result.image_data.astype(np.uint8)).convert("RGB")
        
        with st.chat_message("assistant"):
            try:
                # Prompt directo para evitar errores de procesamiento
                prompt_text = "Eres un tutor. Analiza la imagen y explica el problema paso a paso."
                response = model.generate_content([prompt_text, img])
                st.markdown(response.text)
                st.session_state.chat_history.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error técnico: {e}")
