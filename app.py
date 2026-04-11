import streamlit as st
import google.generativeai as genai
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np

# Configuración de página profesional
st.set_page_config(page_title="Math-Online-Lab", layout="wide")

# Recuperar llave de los Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ Falta la configuración: Agrega GEMINI_API_KEY en Secrets.")
    st.stop()

# CONFIGURACIÓN FORZADA PARA EVITAR EL ERROR 404
# Forzamos el uso de la API v1 (estable) en lugar de v1beta
genai.configure(api_key=api_key, transport='rest') 

# Intentamos con el nombre de modelo más compatible del mercado
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    model = genai.GenerativeModel('models/gemini-1.5-flash')

st.title("Math-Online-Lab 🧠")
st.caption("Sistema de Tutoría para Educación Rural - Prototipo UD")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Pizarra de Razonamiento")
    canvas_result = st_canvas(
        stroke_width=5,
        stroke_color="#000000",
        background_color="#ffffff",
        height=400,
        drawing_mode="freedraw",
        key="canvas",
    )
    if st.button("Limpiar"):
        st.rerun()

with col2:
    st.subheader("Interacción con el Tutor")
    
    if st.button("🚀 ANALIZAR AHORA"):
        if canvas_result.image_data is not None:
            # Procesamiento de imagen
            img_raw = canvas_result.image_data.astype(np.uint8)
            img = Image.fromarray(img_raw).convert("RGB")
            
            with st.spinner("Conectando con el servidor de Google..."):
                try:
                    # Instrucciones directas de tutoría
                    instruccion = (
                        "Eres un tutor experto en matemáticas. Analiza la imagen. "
                        "Explica el concepto del mínimo común denominador para resolver el problema."
                    )
                    # Llamada multimodal
                    response = model.generate_content([instruccion, img])
                    st.success("¡Análisis completado!")
                    st.markdown(response.text)
                except Exception as e:
                    # Si esto falla, el error nos dirá exactamente qué falta en el servidor
                    st.error(f"Detalle técnico del error: {e}")
