import streamlit as st
import google.generativeai as genai
import matplotlib.pyplot as plt
import numpy as np

# Configuración de la API (Se conectará a Streamlit Secrets después)
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    API_KEY = "PEGA_AQUI_TU_LLAVE_SOLO_PARA_PRUEBAS"

genai.configure(api_key=API_KEY)

st.title("👨‍🏫 Math AI Lab: Pizarra y Tutor")

tab1, tab2 = st.tabs(["Pizarra del Profesor", "Chat del Estudiante"])

with tab1:
    st.header("Pizarra Digital Inteligente")
    tema = st.text_input("¿Qué vamos a explicar hoy?")
    if st.button("Generar Material"):
        model = genai.GenerativeModel('gemini-1.5-flash')
        res = model.generate_content(f"Explica brevemente {tema} con un ejemplo.")
        st.write(res.text)
        # Gráfico de ejemplo
        fig, ax = plt.subplots()
        ax.plot(np.random.simple_iter(10), np.random.simple_iter(10))
        st.pyplot(fig)

with tab2:
    st.header("Asistente Virtual")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])
    
    pregunta = st.chat_input("¿Tienes alguna duda?")
    if pregunta:
        st.session_state.messages.append({"role": "user", "content": pregunta})
        model = genai.GenerativeModel('gemini-1.5-flash')
        respuesta = model.generate_content(pregunta)
        st.session_state.messages.append({"role": "assistant", "content": respuesta.text})
        st.rerun()
