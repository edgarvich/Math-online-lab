import streamlit as st
import google.generativeai as genai
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np

st.set_page_config(page_title="Math Lab", layout="wide")

# Conexión directa
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Configura GEMINI_API_KEY en Secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Usamos el nombre 'gemini-1.5-flash-latest' para forzar la versión más nueva
model = genai.GenerativeModel('gemini-1.5-flash-latest')

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
    if analyze_btn and canvas_result.image_data is not None:
        img = Image.fromarray(canvas_result.image_data.astype(np.uint8)).convert("RGB")
        with st.chat_message("assistant"):
            try:
                # El prompt ahora es un comando simple para probar conexión
                response = model.generate_content(["Identifica el problema matemático en esta imagen y explícalo como un tutor.", img])
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
