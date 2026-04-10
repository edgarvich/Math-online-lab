import streamlit as st
import google.generativeai as genai

# Configuración de la página
st.set_page_config(page_title="Math AI Lab", layout="wide")

# Conectar con la API de forma segura
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Falta la API KEY en los Secrets de Streamlit.")

st.title("👨‍🏫 Math AI Lab: Pizarra y Tutor")

# Usar el modelo con el nombre más simple posible
model = genai.GenerativeModel('gemini-1.5-flash')

tab1, tab2 = st.tabs(["📝 Pizarra del Profesor", "🤖 Chat del Estudiante"])

with tab1:
    st.header("Generador de Clases")
    tema = st.text_input("¿Qué concepto explicaremos hoy?", placeholder="Ej: Suma de fracciones")
    
    if st.button("Generar Material de Pizarra"):
        try:
            with st.spinner("El profesor virtual está escribiendo..."):
                # Forzamos una respuesta simple
                response = model.generate_content(f"Explica brevemente {tema}")
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Error técnico: {e}")
            st.info("Nota: Si el error dice 404, espera 1 minuto a que se instalen las nuevas librerías.")

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
            st.error(f"Error: {e}")

st.divider()
st.caption("Laboratorio creado por Edgar Romero Valero - Maestría en Tecnología Educativa.")
