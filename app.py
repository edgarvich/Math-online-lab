import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder
from PIL import Image

# Configuración
st.set_page_config(page_title="Math Tutor AI", layout="centered")

# API Setup
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Configura la clave en Secrets.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("Math-Online-Lab Chat 🎓")

# Historial del Chatbot
if "messages" not in st.session_state:
    st.session_state.messages = []

# Interfaz de Voz
st.write("🎤 **Pulsa para hablar con el tutor:**")
audio = mic_recorder(start_prompt="Hablar", stop_prompt="Detener", key='recorder')

# Mostrar mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Procesar entrada
if prompt := st.chat_input("Escribe tu problema (ej: 1/2 + 1/3)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Instrucción de tutoría
            response = model.generate_content(f"Eres un tutor experto. Ayúdame a resolver esto paso a paso: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")

if audio:
    st.info("Nota de voz recibida. (Procesando...)")
    # Aquí el tutor respondería a la intención de voz
