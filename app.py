import streamlit as st
import google.generativeai as genai

# Configuración de Pizarra Profesional
st.set_page_config(page_title="Tutor Pro Math-Lab", layout="centered")

# Conexión al cerebro Pro
api_key = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-1.5-pro')

# --- REGISTRO Y PERSONALIZACIÓN ---
if "nombre" not in st.session_state:
    st.title("🎓 Math-Online-Lab: Acceso Estudiante")
    nombre = st.text_input("¡Hola! Soy tu tutor virtual. ¿Cómo te llamas?")
    if st.button("Empezar Clase"):
        st.session_state.nombre = nombre
        st.session_state.paso = 0 # Seguimiento de avance
        st.rerun()
    st.stop()

st.title(f"Pizarra de {st.session_state.nombre} ✏️")

# --- LÓGICA DE TUTORÍA PASO A PASO ---
if prompt := st.chat_input("Plantea tu ejercicio (ej: 1/2 + 1/3)"):
    with st.chat_message("assistant"):
        # Instrucción Maestra para simular Pizarra
        instruccion = (
            f"Eres un Tutor Virtual de la Universidad de Delaware. El alumno es {st.session_state.nombre}. "
            "Usa un estilo de 'Pizarra': Números GRANDES con LaTeX, emojis y flechas. "
            "NO des la respuesta final. Explica solo el PRIMER PASO y pregunta al alumno qué sigue."
        )
        
        try:
            response = model.generate_content(f"{instruccion}. Ejercicio: {prompt}")
            
            # Formato de Pizarra Visual
            st.markdown(f"### 📔 Explicación para {st.session_state.nombre}:")
            st.info(response.text)
            
            # Imagen de apoyo dinámica (solo para fracciones)
            if "/" in prompt:
                st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Fraction_addition.svg/1200px-Fraction_addition.svg.png", 
                         caption="Visualización del proceso en la pizarra", width=500)
                
                
        except Exception as e:
            st.error(f"Error de conexión: {e}")

# --- BOTÓN PARA EL DOCENTE ---
with st.sidebar:
    if st.button("📊 Ver Reporte de Fallas"):
        st.write(f"Estudiante: {st.session_state.nombre}")
        st.write("Estado: Analizando fracciones heterogéneas.")
