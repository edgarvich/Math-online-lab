import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

st.set_page_config(page_title="Math Lab Global", layout="wide")

# Configuración de API
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

# --- LOGIN ---
if "nombre" not in st.session_state:
    st.title("Math-Online-Lab 🎓")
    nombre = st.text_input("Ingresa tu nombre para iniciar:")
    if st.button("Comenzar"):
        st.session_state.nombre = nombre
        st.session_state.historial = []
        st.rerun()
    st.stop()

st.title(f"Centro de Matemáticas: {st.session_state.nombre} 🧠")

if prompt := st.chat_input("¿Qué vamos a aprender hoy?"):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        instruccion = (
            f"Eres el Tutor Maestro de {st.session_state.nombre}. Dominas todas las áreas: "
            "Aritmética, Álgebra, Geometría y Estadística. "
            "Usa números GRANDES con $$ (LaTeX). Explica de forma visual y breve."
        )
        
        try:
            response = model.generate_content(f"{instruccion}. Pregunta: {prompt}")
            texto = response.text
            st.markdown(texto)
            hablar(texto.replace("$", "").replace("*", ""))
            
            # --- SOPORTE VISUAL CORREGIDO ---
            if any(x in prompt.lower() for x in ["fraccion", "denominador"]):
                st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Fraction_addition.svg/1200px-Fraction_addition.svg.png", caption="Suma de Fracciones")
            
            elif any(x in prompt.lower() for x in ["ecuacion", "x", "algebra"]):
                st.image("https://i.ibb.co/L8yHh9M/mcd-visual.png", caption="Equilibrio en Álgebra") # Cambia por una de balanza si tienes
            
            elif any(x in prompt.lower() for x in ["geometria", "area", "triangulo"]):
                st.image("https://i.ibb.co/SxbP8B4/decimal-number-line.png", caption="Conceptos Geométricos")

        except Exception as e:
            st.error(f"Error: {e}")
