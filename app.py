import streamlit as st
import google.generativeai as genai
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np

# Configuración de página
st.set_page_config(page_title="Math-Online-Lab", layout="wide")

# Llave de API
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Falta GEMINI_API_KEY en Secrets.")
    st.stop()

# --- LA CLAVE DEL ÉXITO: FORZAR V1 ---
# Configuramos la librería para que ignore v1beta por completo
genai.configure(api_key=api_key, transport='rest')

# Definimos el modelo usando la versión de producción (v1)
# Si 'gemini-1.5-flash' falla, el sistema probará la versión específica de texto/imagen
try:
    model = genai.GenerativeModel(model_name='gemini-1.5-flash')
except:
    model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')

st.title("Math-Online-Lab 🧠")
st.caption("Prototipo de Tutoría - Universidad de Delaware")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Pizarra")
    canvas_result = st_canvas(
        stroke_width=5, stroke_color="#000000", background_color="#ffffff",
        height=400, drawing_mode="freedraw", key="canvas",
    )
    if st.button("Limpiar"):
        st.rerun()

with col2:
    st.subheader("Tutor")
    if st.button("🚀 ANALIZAR"):
        if canvas_result.image_data is not None:
            # Procesar imagen
            img_raw = canvas_result.image_data.astype(np.uint8)
            img = Image.fromarray(img_raw).convert("RGB")
            
            with st.spinner("Conectando con el servidor estable..."):
                try:
                    # En lugar de usar scaffolding complejo, pedimos una respuesta directa 
                    # para verificar que la conexión por fin sirve.
                    response = model.generate_content(["Actúa como tutor. ¿Qué problema ves en esta imagen? Explícalo.", img])
                    st.success("¡Conexión exitosa!")
                    st.markdown(response.text)
                except Exception as e:
                    # Si esto falla, forzamos la última opción: el modelo 'gemini-pro-vision'
                    try:
                        alt_model = genai.GenerativeModel('gemini-pro-vision')
                        response = alt_model.generate_content(["Explica este problema:", img])
                        st.markdown(response.text)
                    except Exception as e2:
                        st.error(f"Error definitivo: {e2}")
