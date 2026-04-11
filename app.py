import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
from datetime import datetime

# Configuración Profesional
st.set_page_config(page_title="Math-Lab RAG Pro", layout="wide")

# Conexión al Cerebro (Gemini 2.5 Flash)
api_key = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-2.5-flash')

# --- FUNCIÓN DE VOZ ---
def hablar(texto):
    js_code = f"""<script>
    var msg = new SpeechSynthesisUtterance('{texto.replace("'", "")}');
    msg.lang = 'es-ES';
    window.speechSynthesis.speak(msg);
    </script>"""
    components.html(js_code, height=0)

# --- SISTEMA DE "MEMORIA" (Simulación de RAG persistente) ---
if "historial_fallas" not in st.session_state:
    st.session_state.historial_fallas = []

# --- LOGIN ---
if "nombre" not in st.session_state:
    st.title("Math-Online-Lab: Sistema Adaptativo 🎓")
    nombre = st.text_input("Ingresa tu nombre para recuperar tu progreso:")
    if st.button("Iniciar Sesión"):
        st.session_state.nombre = nombre
        st.rerun()
    st.stop()

st.title(f"Pizarra de Aprendizaje: {st.session_state.nombre} 🧠")

# --- INTERFAZ DE TUTORÍA CON RAG ---
if prompt := st.chat_input("Plantea tu ejercicio o duda matemática..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # RECUPERACIÓN (Retrieval): Buscamos fallas previas en la memoria
        fallas_contexto = ", ".join(st.session_state.historial_fallas[-3:]) # Últimas 3 fallas
        
        # AUMENTO (Augmentation): Inyectamos las fallas en el prompt
        instruccion = (
            f"Eres un Tutor IA con memoria RAG para {st.session_state.nombre}. "
            f"El alumno ha fallado anteriormente en: {fallas_contexto}. "
            "Usa esta información para dar una explicación que ataque sus puntos débiles. "
            "Usa números GRANDES con $$ y lenguaje motivador."
        )
        
        try:
            response = model.generate_content(f"{instruccion}. Pregunta actual: {prompt}")
            texto_tutor = response.text
            st.markdown(texto_tutor)
            hablar(texto_tutor.replace("$", "").replace("*", ""))
            
            # --- ANÁLISIS AUTOMÁTICO DE FALLAS (Para el RAG) ---
            # Si el tutor detecta que el alumno no entendió, guarda la falla
            if "no entiendo" in prompt.lower() or "difícil" in prompt.lower():
                st.session_state.historial_fallas.append(prompt)
                st.sidebar.warning(f"Falla registrada: {prompt}")

            # Soporte Visual Dinámico
            if "/" in prompt:
                st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Fraction_addition.svg/1200px-Fraction_addition.svg.png", caption="Visualización del concepto")
                

        except Exception as e:
            st.error(f"Error: {e}")

# --- PANEL DEL DOCENTE (Análisis RAG) ---
with st.sidebar:
    st.header("Análisis de Progreso")
    st.write(f"**Alumno:** {st.session_state.nombre}")
    if st.session_state.historial_fallas:
        st.write("### Mapa de errores detectados:")
        for f in st.session_state.historial_fallas:
            st.write(f"❌ {f}")
    else:
        st.success("Aún no hay fallas registradas.")
