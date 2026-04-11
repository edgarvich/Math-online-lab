import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# 1. Configuración de la interfaz profesional
st.set_page_config(page_title="Math-Online-Lab: AI Tutor", layout="wide")

# 2. Configuración de Seguridad y API
# Asegúrate de tener tu GEMINI_API_KEY en los Secrets de Streamlit
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ Configura la GEMINI_API_KEY en los secretos de Streamlit.")
    st.stop()

genai.configure(api_key=api_key)
# Usamos el modelo 2.5 Flash por su equilibrio entre velocidad y razonamiento
model = genai.GenerativeModel('models/gemini-2.5-flash')

# --- FUNCIÓN DE VOZ AUTOMÁTICA (JavaScript) ---
def hablar(texto):
    # Limpiamos el texto de caracteres especiales de Markdown para que la voz sea fluida
    texto_limpio = texto.replace("$", "").replace("*", "").replace("#", "").replace("\n", " ")
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance('{texto_limpio}');
    msg.lang = 'es-ES';
    msg.rate = 1.0;
    window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js_code, height=0)

# --- GESTIÓN DE ESTADOS (RAG y Flujo) ---
if "estado" not in st.session_state:
    st.session_state.estado = "registro"
    st.session_state.fallas_diagnostico = []
    st.session_state.pregunta_actual = 0
    st.session_state.nombre = ""

# --- PANTALLA 1: REGISTRO ---
if st.session_state.estado == "registro":
    st.title("🎓 Bienvenido al Math-Online-Lab")
    st.subheader("Tu tutor inteligente con memoria adaptativa")
    nombre_input = st.text_input("Para empezar, ¿cuál es tu nombre?")
    if st.button("Comenzar Evaluación"):
        if nombre_input:
            st.session_state.nombre = nombre_input
            st.session_state.estado = "diagnostico"
            st.rerun()
        else:
            st.warning("Por favor, ingresa tu nombre.")
    st.stop()

# --- PANTALLA 2: DIAGNÓSTICO INICIAL ---
if st.session_state.estado == "diagnostico":
    preguntas = [
        {"q": "Suma: 1/4 + 2/4", "a": "3/4", "tema": "Fracciones Homogéneas"},
        {"q": "¿Cuál es el común denominador para 1/2 y 1/3?", "a": "6", "tema": "MCD (Mínimo Común Denominador)"},
        {"q": "Si x + 5 = 15, ¿cuánto vale x?", "a": "10", "tema": "Ecuaciones básicas"},
        {"q": "¿Cuál es el área de un cuadrado si su lado mide 4?", "a": "16", "tema": "Geometría (Áreas)"},
        {"q": "Resultado de 7 multiplicado por 0", "a": "0", "tema": "Propiedades de la multiplicación"}
    ]
    
    idx = st.session_state.pregunta_actual
    st.title(f"Evaluación de Nivel: {st.session_state.nombre} ✏️")
    st.progress((idx + 1) / len(preguntas))
    
    with st.container():
        st.info(f"Pregunta {idx + 1} de {len(preguntas)}")
        st.subheader(preguntas[idx]["q"])
        respuesta = st.text_input("Escribe solo el número o fracción resultante:", key=f"q_{idx}")
        
        if st.button("Enviar Respuesta"):
            if respuesta.strip() != preguntas[idx]["a"]:
                st.session_state.fallas_diagnostico.append(preguntas[idx]["tema"])
            
            if idx < len(preguntas) - 1:
                st.session_state.pregunta_actual += 1
                st.rerun()
            else:
                st.success("✅ ¡Diagnóstico completado! Entrando al aula virtual...")
                st.session_state.estado = "tutoria"
                st.rerun()
    st.stop()

# --- PANTALLA 3: TUTORÍA ADAPTATIVA (RAG) ---
st.title(f"Pizarra Virtual: {st.session_state.nombre} 🧠")

# Barra lateral con el perfil del estudiante (Análisis de fallas)
with st.sidebar:
    st.header("📊 Perfil de Aprendizaje")
    st.write(f"**Estudiante:** {st.session_state.nombre}")
    if st.session_state.fallas_diagnostico:
        st.error("Temas que debemos reforzar:")
        for falla in set(st.session_state.fallas_diagnostico):
            st.write(f"• {falla}")
    else:
        st.success("¡Excelente nivel! No se detectaron fallas iniciales.")
    
    if st.button("Reiniciar Laboratorio"):
        st.session_state.clear()
        st.rerun()

# Historial de Chat (Opcional, para ver la conversación)
if "historial" not in st.session_state:
    st.session_state.historial = []

for msg in st.session_state.historial:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada del Chat
if prompt := st.chat_input("¿Qué ejercicio quieres resolver ahora?"):
    st.session_state.historial.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # LÓGICA RAG: Recuperamos las fallas para inyectarlas al modelo
        contexto_fallas = ", ".join(set(st.session_state.fallas_diagnostico))
        
        instruccion_maestra = (
            f"Eres el Tutor IA Maestro de {st.session_state.nombre}. "
            f"IMPORTANTE: El alumno falló en el diagnóstico inicial en: {contexto_fallas}. "
            "Usa esta información para explicar con más paciencia esos temas. "
            "Usa siempre números GRANDES con LaTeX ($$) y emojis. "
            "No des la respuesta de inmediato, usa andamiaje (scaffolding)."
        )
        
        try:
            with st.spinner("Pensando..."):
                response = model.generate_content(f"{instruccion_maestra}. Pregunta del alumno: {prompt}")
                respuesta_texto = response.text
                st.markdown(respuesta_texto)
                hablar(respuesta_texto)
                st.session_state.historial.append({"role": "assistant", "content": respuesta_texto})
            
            # --- SOPORTE VISUAL INTELIGENTE ---
            if any(x in prompt.lower() for x in ["fraccion", "denominador", "/"]):
                st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Fraction_addition.svg/1200px-Fraction_addition.svg.png", 
                         caption="Visualización de Fracciones Heterogéneas")
            elif any(x in prompt.lower() for x in ["ecuacion", "x", "="]):
                st.info("💡 Recuerda: Una ecuación es como una balanza en equilibrio.")
                
        except Exception as e:
            if "429" in str(e) or "ResourceExhausted" in str(e):
                st.warning("🚀 El tutor está procesando mucha información. Por favor, espera 30 segundos y vuelve a preguntar.")
            else:
                st.error(f"Aviso técnico: {e}")
