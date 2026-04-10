import streamlit as st
import google.generativeai as genai

# 1. CONFIGURACIÓN DE SEGURIDAD (API KEY)
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
    else:
        st.error("⚠️ Error: No se encontró la clave GOOGLE_API_KEY en los Secrets.")
except Exception as e:
    st.error(f"❌ Error al configurar la API: {e}")

# 2. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Math AI Lab", page_icon="👨‍🏫", layout="wide")

# Título Principal
st.title("👨‍🏫 Math AI Lab: Pizarra y Tutor")
st.markdown("---")

# 3. CREACIÓN DE PESTAÑAS (TABS)
tab1, tab2 = st.tabs(["📝 Pizarra del Profesor", "🤖 Chat del Estudiante"])

# --- PESTAÑA 1: PIZARRA DEL PROFESOR ---
with tab1:
    st.header("Generador de Clases")
    st.write("Escribe un tema para que la IA genere una explicación clara para tus alumnos.")
    
    tema = st.text_input("¿Qué concepto matemático explicaremos hoy?", placeholder="Ej: Suma de fracciones")
    
    if st.button("Generar Material de Pizarra"):
        if tema:
            try:
                with st.spinner("Preparando la pizarra..."):
                    # Usamos 'gemini-1.5-flash-latest' que es más estable
                    model = genai.GenerativeModel('gemini-1.5-flash-latest')
                    prompt = f"Actúa como un profesor de primaria rural. Explica de forma muy sencilla, paso a paso y con un ejemplo cotidiano: {tema}"
                    response = model.generate_content(prompt)
                    
                    st.success("¡Pizarra lista!")
                    st.markdown("### 📝 Contenido Sugerido:")
                    st.write(response.text)
            except Exception as e:
                st.error(f"Hubo un problema al conectar con la IA: {e}")
        else:
            st.warning("Por favor, escribe un tema primero.")

# --- PESTAÑA 2: CHAT DEL ESTUDIANTE ---
with tab2:
    st.header("Asistente Virtual de Matemáticas")
    st.write("Ideal para que tus alumnos resuelvan dudas paso a paso.")

    # Inicializar el historial de chat si no existe
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar mensajes previos
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada de texto del alumno
    if prompt_alumno := st.chat_input("¿Qué parte no entendiste?"):
        # Guardar mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": prompt_alumno})
        with st.chat_message("user"):
            st.markdown(prompt_alumno)

        # Generar respuesta de la IA
        try:
            with st.chat_message("assistant"):
                model = genai.GenerativeModel('
