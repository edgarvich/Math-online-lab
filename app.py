import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# 1. Configuración de página
st.set_page_config(page_title="Math Lab Adaptativo", layout="wide")

# 2. Configuración de la IA (Gemini 2.5 Flash)
api_key = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-2.5-flash')

# --- VOZ ---
def hablar(texto):
    js_code = f"""<script>
    var msg = new SpeechSynthesisUtterance('{texto.replace("'", "")}');
    msg.lang = 'es-ES';
    window.speechSynthesis.speak(msg);
    </script>"""
    components.html(js_code, height=0)

# --- INICIALIZACIÓN DE ESTADOS ---
if "estado" not in st.session_state:
    st.session_state.estado = "registro"  # registro -> diagnostico -> tutoria
    st.session_state.fallas_diagnostico = []
    st.session_state.pregunta_actual = 0

# --- PANTALLA 1: REGISTRO ---
if st.session_state.estado == "registro":
    st.title("🎓 Bienvenido al Math-Online-Lab")
    nombre = st.text_input("Hola, ¿cómo te llamas?")
    if st.button("Comenzar Evaluación"):
        if nombre:
            st.session_state.nombre = nombre
            st.session_state.estado = "diagnostico"
            st.rerun()
    st.stop()

# --- PANTALLA 2: DIAGNÓSTICO (5 Preguntas clave) ---
if st.session_state.estado == "diagnostico":
    preguntas = [
        {"q": "Suma: 1/4 + 2/4", "a": "3/4", "tema": "Fracciones Homogéneas"},
        {"q": "Denominador común para 1/2 y 1/3", "a": "6", "tema": "MCD"},
        {"q": "Si x + 5 = 15, ¿cuánto vale x?", "a": "10", "tema": "Ecuaciones"},
        {"q": "Área de un cuadrado de lado 4", "a": "16", "tema": "Geometría"},
        {"q": "Resultado de 7 x 0", "a": "0", "tema": "Aritmética básica"}
    ]
    
    idx = st.session_state.pregunta_actual
    st.title(f"Evaluación Inicial para {st.session_state.nombre}")
    st.progress((idx + 1) / len(preguntas))
    
    st.subheader(preguntas[idx]["q"])
    respuesta = st.text_input("Tu respuesta:", key=f"ans_{idx}")
    
    if st.button("Siguiente"):
        if respuesta.strip() != preguntas[idx]["a"]:
            st.session_state.fallas_diagnostico.append(preguntas[idx]["tema"])
        
        if idx < len(preguntas) - 1:
            st.session_state.pregunta_actual += 1
            st.rerun()
        else:
            st.session_state.estado = "tutoria"
            st.rerun()
    st.stop()

# --- PANTALLA 3: TUTORÍA CON RAG (Basada en Fallas) ---
st.title(f"Tutoría Personalizada: {st.session_state.nombre} 🧠")

with st.sidebar:
    st.header("Perfil del Estudiante")
    if st.session_state.fallas_diagnostico:
        st.warning("Temas a reforzar:")
        for f in set(st.session_state.fallas_diagnostico):
            st.write(f"• {f}")
    else:
        st.success("¡Nivel excelente! Listo para retos avanzados.")

if prompt := st.chat_input("¿Qué quieres practicar ahora?"):
    with st.chat_message("assistant"):
        # RAG: Inyectamos los resultados del diagnóstico en la IA
        contexto_fallas = ", ".join(st.session_state.fallas_diagnostico)
        instruccion = (
            f"Eres el tutor de {st.session_state.nombre}. En el diagnóstico, falló en: {contexto_fallas}. "
            "Usa andamiaje (scaffolding). No des la respuesta, guía visualmente con $$."
        )
        
        response = model.generate_content(f"{instruccion}. Pregunta: {prompt}")
        st.markdown(response.text)
        hablar(response.text.replace("$", ""))
        
        # Apoyo Visual automático
        if "fraccion" in prompt.lower() or "fraccion" in contexto_fallas.lower():
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Fraction_addition.svg/1200px-Fraction_addition.svg.png")
