import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

# Configuración
st.set_page_config(page_title="Math Lab", layout="centered")

api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Configura GEMINI_API_KEY en Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# EL CAMBIO CLAVE: Usamos 'models/gemini-1.5-flash-latest' 
# Este nombre fuerza al servidor a buscar la versión más reciente disponible.
model = genai.GenerativeModel('models/gemini-1.5-flash-latest')

st.title("Math-Online-Lab Chat 🎓")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Botón de Voz
audio = mic_recorder(start_prompt="🎤 Hablar", stop_prompt="⏹️ Detener", key='recorder')

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de texto
if prompt := st.chat_input("Escribe tu duda..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Forzamos una respuesta de tutoría directa
            response = model.generate_content(f"Actúa como un tutor experto. Explica paso a paso: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Si vuelve a fallar, el error nos dirá qué modelos SÍ están disponibles
            st.error("Error de conexión. Intentando recuperar modelos disponibles...")
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            st.write(f"Modelos detectados en este servidor: {available_models}")
