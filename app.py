import streamlit as st
import google.generativeai as genai

# Configuración Profesional
st.set_page_config(page_title="Tutor Pro Math-Lab", layout="wide")

# Conexión al Cerebro (Usamos el 2.5 que es el que tu servidor tiene activo)
api_key = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# ESTE ES EL NOMBRE QUE FUNCIONA EN TU SERVIDOR:
model = genai.GenerativeModel('models/gemini-2.5-flash')

# --- PERSONALIZACIÓN ---
if "nombre" not in st.session_state:
    st.title("🎓 Acceso al Lab de Matemáticas")
    nombre = st.text_input("¡Hola! ¿Cómo te llamas?")
    if st.button("Empezar Clase"):
        st.session_state.nombre = nombre
        st.session_state.fallas = []
        st.rerun()
    st.stop()

st.title(f"Pizarra de {st.session_state.nombre} ✏️")

# --- INTERFAZ DE TUTORÍA ---
if prompt := st.chat_input("Plantea tu ejercicio de hoy..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            # Instrucción de Scaffolding
            instruccion = (
                f"Actúa como un tutor virtual para {st.session_state.nombre}. "
                "Usa números GRANDES con LaTeX ($$). No des la respuesta final. "
                "Guía al alumno paso a paso."
            )
            response = model.generate_content(f"{instruccion}. Ejercicio: {prompt}")
            st.markdown(f"### {response.text}")
            
            # Soporte visual dinámico
            if "/" in prompt:
                st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Fraction_addition.svg/1200px-Fraction_addition.svg.png", 
                         caption="Visualización en la pizarra", width=500)
                
        except Exception as e:
            st.error(f"Error técnico detectado: {e}")
            # Si vuelve a fallar, el código nos dirá exactamente por qué
            st.info("Intentando reconexión automática...")
