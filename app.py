import streamlit as st
import google.generativeai as genai

# 1. Configuración de la API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 2. Configuración estética
st.set_page_config(page_title="Math AI Lab", page_icon="🎓", layout="wide")

st.title("👨‍🏫 Math AI Lab: Laboratorio de Innovación")
st.markdown("---")

# 3. Modelo
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. Pestañas para el proyecto
tab1, tab2 = st.tabs(["📝 Pizarra Virtual", "🤖 Tutor Inteligente"])

with tab1:
    st.header("Generador de Lecciones")
    tema = st.text_input("Tema de hoy:", placeholder="Ej: Las fracciones en la vida diaria")
    if st.button("Crear Pizarra"):
        with st.spinner("Preparando material..."):
            res = model.generate_content(f"Eres un profesor creativo. Explica de forma visual y sencilla: {tema}")
            st.markdown(res.text)

with tab2:
    st.header("Chat con el Tutor")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input("¿Qué duda tienes?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        response = model.generate_content(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        with st.chat_message("assistant"): st.markdown(response.text)

st.sidebar.info("Proyecto de Maestría en Tecnología Educativa - Edgar Romero Valero")
