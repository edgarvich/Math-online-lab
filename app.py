import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración de la página
st.set_page_config(page_title="Math Online Lab", layout="centered")

# Título y descripción para tu portafolio de UD
st.title("Math-Online-Lab 🎓")
st.write("Prototipo de Tutoría IA para entornos educativos.")

# Recuperar la llave desde Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Configura la clave API en los Secrets de Streamlit.")
else:
    genai.configure(api_key=api_key)
    # Usamos el modelo más estable para la nube
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Subida de imagen
    img_file = st.file_uploader("Sube una imagen de un problema matemático:", type=['png', 'jpg', 'jpeg'])

    if img_file:
        image = Image.open(img_file)
        st.image(image, caption="Imagen cargada", use_column_width=True)
        
        if st.button("🚀 Analizar con el Tutor"):
            with st.spinner("El tutor está analizando el problema..."):
                try:
                    # Instrucción pedagógica (Scaffolding)
                    prompt = "Eres un tutor experto. Analiza la imagen y guía al estudiante paso a paso sin dar la respuesta directamente."
                    response = model.generate_content([prompt, image])
                    st.success("Análisis completo:")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error de conexión: {e}")
