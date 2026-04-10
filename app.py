import streamlit as st
import google.generativeai as genai

# CONFIGURACIÓN DE LA API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.set_page_config(page_title="Math AI Lab", layout="wide")
st.title("👨‍🏫 Math AI Lab: Pizarra y Tutor")

# FUNCIÓN SEGURA PARA CARGAR EL MODELO
def obtener_modelo():
    # Intentamos con el modelo más nuevo, si falla usamos el Pro
    for nombre in ['gemini-1.5-flash', 'gemini-pro']:
        try:
            model = genai.GenerativeModel(nombre)
            return model
        except:
            continue
    return None

model = obtener_modelo()

tab1, tab2 = st.tabs(["📝 Pizarra del Profesor", "🤖 Chat del Estudiante"])

with tab1:
    st.header("Generador de Clases")
    tema = st.text_input("¿Qué concepto explicaremos hoy?", placeholder="Ej: Suma de fracciones")
    
    if st.button("Generar Material de Pizarra"):
        if model:
            try:
                with st.spinner("Conectando..."):
                    response = model.generate_content(f"Explica como profesor: {tema}")
                    st.markdown(response.text)
            except Exception as e:
                st.error(f"Error al generar: {e}")
        else:
            st.error("No se pudo conectar con los modelos de Google.")

with tab2:
    st.header("Asistente Virtual")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input("Duda del alumno"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        if model:
            res = model.generate_content(prompt)
            st.session_state.messages.append({"role": "assistant", "content": res.text})
            with st.chat_message("assistant"): st.markdown(res.text)

st.divider()
st.caption("Laboratorio creado por Edgar Romero Valero - Maestría en Tecnología Educativa.")
