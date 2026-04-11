import streamlit as st
import google.generativeai as genai

# Configuración
st.set_page_config(page_title="Math-Online-Lab Personalizado", layout="wide")

# API Setup
api_key = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-2.5-flash')

# --- SISTEMA DE REGISTRO / LOGIN ---
if "nombre_usuario" not in st.session_state:
    st.title("Bienvenido al Math-Online-Lab 🎓")
    nombre = st.text_input("Por favor, ingresa tu nombre para comenzar:")
    if st.button("Ingresar"):
        if nombre:
            st.session_state.nombre_usuario = nombre
            st.session_state.registro_fallas = []
            st.session_state.messages = []
            st.rerun()
    st.stop()

# --- INTERFAZ PRINCIPAL ---
st.title(f"Hola, {st.session_state.nombre_usuario} 👋")
st.caption("Tu Tutor IA personalizado está listo.")

# Sidebar para el Docente (Protegido por contraseña simple)
with st.sidebar:
    st.header("Panel del Docente")
    pwd = st.text_input("PIN de acceso:", type="password")
    if pwd == "1234": # Pin de ejemplo
        st.write(f"### Reporte de {st.session_state.nombre_usuario}")
        if st.session_state.registro_fallas:
            for falla in st.session_state.registro_fallas:
                st.warning(f"Falla detectada: {falla}")
        else:
            st.success("No hay fallas registradas aún.")

# Historial del Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada de Chat
if prompt := st.chat_input("Escribe tu duda aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # PERSONALIZACIÓN: Inyectamos el nombre en las instrucciones
            instruccion = (
                f"Eres un tutor experto. El nombre del estudiante es {st.session_state.nombre_usuario}. "
                f"Dirígete a él por su nombre frecuentemente. No des la respuesta, usa scaffolding."
            )
            
            response = model.generate_content(f"{instruccion}. Pregunta: {prompt}")
            texto_tutor = response.text
            st.markdown(texto_tutor)
            
            # LOGICA DE DETECCIÓN DE FALLAS (Para el Docente)
            if "no entiendo" in prompt.lower() or "difícil" in prompt.lower():
                st.session_state.registro_fallas.append(prompt)

            st.session_state.messages.append({"role": "assistant", "content": texto_tutor})
        except Exception as e:
            st.error(f"Error: {e}")
