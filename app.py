import streamlit as st
import google.generativeai as genai

# Configuración de la API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.set_page_config(page_title="Math AI Lab", layout="wide")
st.title("👨‍🏫 Math AI Lab: Pizarra y Tutor")

# Usaremos el modelo Pro que es el más compatible universalmente
try:
    model = genai.GenerativeModel('gemini-pro')
except:
    st.error("Error al cargar el modelo de IA.")

tab1, tab2 = st.tabs(["📝 Pizarra del Profesor", "🤖 Chat del Estudiante"])

with tab1:
    st.header("Generador de Clases")
    tema = st.text_input("¿Qué concepto matemático explicaremos hoy?", placeholder="Ej: Fracciones")
    
    if st.button("Generar Material de Pizarra"):
        try:
            with st.spinner("El profesor está escribiendo..."):
                response = model.generate_content(f"Explica de forma sencilla para estudiantes rurales: {tema}")
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Asegúrate de que tu API KEY sea correcta. Error: {e}")

with tab2:
    st.header("Asistente Virtual")
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input("Escribe tu duda"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        try:
            res = model.generate_content(prompt)
            st.session_state.messages.append({"role": "assistant", "content": res.text})
            with st.chat_message("assistant"): st.markdown(res.text)
        except Exception as e:
            st.error(f"Error en el chat: {e}")

st.divider()
st.caption("Laboratorio creado por Edgar Romero Valero - Maestría en Tecnología Educativa.")
