import streamlit as st
import google.generativeai as genai

# Configuración de la API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.set_page_config(page_title="Math AI Lab", layout="wide")
st.title("👨‍🏫 Math AI Lab: Pizarra y Tutor")

# MÉTODO UNIVERSAL: Intentamos cargar el modelo de forma robusta
try:
    # Este es el nombre estándar que no debería fallar en la v1 estable
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("No se pudo inicializar el modelo. Revisa la configuración de la API.")

tab1, tab2 = st.tabs(["📝 Pizarra del Profesor", "🤖 Chat del Estudiante"])

with tab1:
    st.header("Generador de Clases")
    tema = st.text_input("¿Qué concepto explicaremos hoy?", placeholder="Ej: Suma de fracciones")
    
    if st.button("Generar Material de Pizarra"):
        if tema:
            try:
                with st.spinner("El profesor virtual está escribiendo..."):
                    # Forzamos el uso del método generate_content estándar
                    response = model.generate_content(f"Actúa como un profesor amable. Explica: {tema}")
                    st.markdown(response.text)
            except Exception as e:
                st.error(f"Error de conexión: {e}")
                st.info("💡 Consejo: Si ves un error 404, ve al panel de Streamlit y dale a 'Reboot App'.")
        else:
            st.warning("Escribe un tema primero.")

with tab2:
    st.header("Asistente Virtual")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])

    if prompt := st.chat_input("¿En qué puedo ayudarte?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        try:
            res = model.generate_content(prompt)
            st.session_state.messages.append({"role": "assistant", "content": res.text})
            with st.chat_message("assistant"): st.markdown(res.text)
        except:
            st.error("El chat no está disponible en este momento.")

st.divider()
st.caption("Laboratorio creado por Edgar Romero Valero - Maestría en Tecnología Educativa.")
