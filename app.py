import streamlit as st
import google.generativeai as genai
from google.api_core import client_options

# 1. Configuración de la API forzando la versión ESTABLE (v1)
if "GOOGLE_API_KEY" in st.secrets:
    # Esta línea es el "truco": le dice a la librería que ignore v1beta
    options = client_options.ClientOptions(api_version='v1')
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"], client_options=options)

st.set_page_config(page_title="Math AI Lab", page_icon="🎓")
st.title("👨‍🏫 Math AI Lab: Pizarra y Tutor")

# 2. Cargar el modelo
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Error al cargar el motor de IA.")

# 3. Interfaz
tema = st.text_input("Tema de hoy:", placeholder="Ej: suma de fracciones")

if st.button("Crear Pizarra"):
    if tema:
        try:
            with st.spinner("Generando contenido estable..."):
                response = model.generate_content(f"Explica de forma sencilla: {tema}")
                st.markdown("### 📝 Contenido de la Pizarra:")
                st.write(response.text)
        except Exception as e:
            st.error(f"Error de conexión: {e}")
            st.info("💡 Consejo: Si el error persiste, dale a 'Reboot app' en el panel de Streamlit.")
    else:
        st.warning("Escribe un tema primero.")

st.divider()
st.caption("Proyecto de Maestría - Edgar Romero Valero")
