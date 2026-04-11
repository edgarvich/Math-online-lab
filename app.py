import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

st.set_page_config(page_title="Math Lab Global", layout="wide")

# Configuración de API (Gemini 2.5 Flash por velocidad y razonamiento)
api_key = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-2.5-flash')

# --- VOZ AUTOMÁTICA ---
def hablar(texto):
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance('{texto.replace("'", "")}');
    msg.lang = 'es-ES';
    msg.rate = 1.0;
    window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js_code, height=0)

# --- LOGIN PERSONALIZADO ---
if "nombre" not in st.session_state:
    st.title("Math-Online-Lab 🎓")
    nombre = st.text_input("Ingresa tu nombre para iniciar tu ruta de aprendizaje:")
    if st.button("Comenzar"):
        st.session_state.nombre = nombre
        st.session_state.historial = []
        st.rerun()
    st.stop()

st.title(f"Centro de Matemáticas: {st.session_state.nombre} 🧠")

# --- LÓGICA DE ÁREAS ---
if prompt := st.chat_input("¿Qué área vamos a dominar hoy? (Fracciones, Álgebra, Geometría...)"):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Instrucción para cubrir TODAS las áreas con Scaffolding
        instruccion = (
            f"Eres el Tutor Maestro de {st.session_state.nombre}. Dominas todas las áreas: "
            "Aritmética, Álgebra, Geometría y Estadística. "
            "Usa números GRANDES con $$ (LaTeX). Explica con analogías visuales."
        )
        
        try:
            response = model.generate_content(f"{instruccion}. Pregunta: {prompt}")
            texto = response.text
            st.markdown(texto)
            hablar(texto.replace("$", "").replace("*", ""))
            
            # Soporte Visual Dinámico por área
            if any(x in prompt.lower() for x in ["fraccion", "denominador"]):
                
            elif "ecuacion" in prompt.lower() or "x" in prompt.lower():
                
            elif "geometria" in prompt.lower() or "area" in prompt.lower():
                
                
        except Exception as e:
            st.error(f"Error: {e}")
