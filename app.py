import streamlit as st
import google.generativeai as genai
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np

# Configuración de página
st.set_page_config(page_title="Math-Online-Lab", layout="wide")

# Conexión con la llave de API
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Error: Configura GEMINI_API_KEY en los Secrets de Streamlit.")
    st.stop()

genai.configure(api_key=api_key)

# MÉTODO EXPERTO: Buscar el modelo activo dinámicamente
@st.cache_resource
def load_expert_model():
    # Buscamos el modelo que acepte imágenes y texto sin importar el nombre exacto
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            # Preferimos gemini-1.5-flash por su rapidez
            if '1.5-flash' in m.name:
                return genai.GenerativeModel(m.name)
    # Si no lo encuentra por nombre, usa el primer modelo disponible
    return genai.GenerativeModel('gemini-1.5-flash')

model = load_expert_model()

st.title("Math-Online-Lab 🧠")
st.caption("Versión Optimizada para Proyectos de Maestría")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Pizarra Interactiva")
    canvas_result = st_canvas(
        stroke_width=5,
        stroke_color="#000000",
        background_color="#ffffff",
        height=400,
        drawing_mode="freedraw",
        key="canvas",
    )
    if st.button("Limpiar Pizarra"):
        st.rerun()

with col2:
    st.subheader("Sesión de Tutoría")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    if st.button("🚀 Analizar y Resolver"):
        if canvas_result.image_data is not None:
            # Convertir el dibujo a imagen procesable
            img_raw = canvas_result.image_data.astype(np.uint8)
            img = Image.fromarray(img_raw).convert("RGB")
            
            with st.chat_message("assistant"):
                try:
                    # Instrucción de tutoría experta
                    prompt = "Eres un tutor de matemáticas experto. Analiza la imagen. No des la respuesta. Guía al estudiante paso a paso (scaffolding)."
                    response = model.generate_content([prompt, img])
                    
                    st.markdown(response.text)
                    st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    # Muestra el error real del sistema para diagnóstico final
                    st.error(f"Error del Sistema: {e}")
