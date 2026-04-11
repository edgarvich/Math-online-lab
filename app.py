import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO
st.set_page_config(page_title="Math-Online-Lab: AI Tutor Pro", layout="wide")

# 2. CONFIGURACIÓN DE LA IA (GEMINI 2.5 FLASH)
# Asegúrate de configurar la clave en los Secrets de Streamlit con el nombre GEMINI_API_KEY
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ Falta la configuración de la API Key en los Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# Optimización de respuesta: corta y precisa para ahorrar cuota y latencia
generation_config = {
    "temperature": 0.3,
    "max_output_tokens": 300,
}
model = genai.GenerativeModel('models/gemini-2.5-flash', generation_config=generation_config)

# --- FUNCIÓN DE VOZ AUTOMÁTICA ---
def hablar(texto):
    # Limpiamos el texto para que el sintetizador de voz no lea códigos raros
    texto_limpio = texto.replace("$", "").replace("*", "").replace("\n", " ").replace("#", "")
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance('{texto_limpio}');
    msg.lang = 'es-ES';
    msg.rate = 1.0;
    window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js_code, height=0)

# --- INICIALIZACIÓN DE ESTADOS (SOLUCIÓN A ATTRIBUTE-ERROR) ---
if "estado" not in st.session_state:
    st.session_state.estado = "registro"
    st.session_state.fallas_diagnostico = []
    st.session_state.pregunta_actual = 0
    st.session_state.nombre = "Estudiante" # Valor por defecto seguro
    st.session_state.historial = []

# --- PANTALLA 1: REGISTRO ---
if st.session_state.estado == "registro":
    st.title("🎓 Bienvenido al Math-Online-Lab")
    st.subheader("Tu tutor inteligente para el éxito en matemáticas")
    nombre_input = st.text_input("Hola, ¿cuál es tu nombre?")
    if st.button("Comenzar Evaluación"):
        if nombre_input:
            st.session_state.nombre = nombre_input
            st.session_state.estado = "diagnostico"
            st.rerun()
        else:
            st.warning("Por favor, ingresa tu nombre para continuar.")
    st.stop()

# --- PANTALLA 2: DIAGNÓSTICO INICIAL ---
if st.session_state.estado == "diagnostico":
    preguntas = [
        {"q": "Suma: 1/4 + 2/4", "a": "3/4", "tema": "Fracciones Homogéneas"},
        {"q": "¿Común denominador para 1/2 y 1/3?", "a": "6", "tema": "MCD / Denominadores"},
        {"q": "Si x + 5 = 15, ¿cuánto vale x?", "a": "10", "tema": "Ecuaciones"},
        {"q": "Área de un cuadrado de lado 4", "a": "16", "tema": "Geometría"},
        {"q": "Resultado de 9 x 0", "a": "0", "tema": "Propiedades Multiplicación"}
    ]
    
    idx = st.session_state.pregunta_actual
    st.title(f"Evaluación de Nivel: {st.session_state.nombre}")
    st.progress((idx + 1) / len(preguntas))
    
    st.subheader(preguntas[idx]["q"])
    respuesta = st.text_input("Tu respuesta:", key=f"diag_{idx}")
    
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

# --- PANTALLA 3: TUTORÍA CON RESILIENCIA (RAG + ESCUDO DE CUOTA) ---
st.title(f"Centro de Aprendizaje: {st.session_state.nombre} 🧠")

# Panel lateral con el perfil real detectado
with st.sidebar:
    st.header("📊 Perfil Educativo")
    if st.session_state.fallas_diagnostico:
        st.warning("Temas a reforzar:")
        for f in set(st.session_state.fallas_diagnostico):
            st.write(f"• {f}")
    else:
        st.success("¡Nivel base sólido!")
    
    if st.button("Reiniciar Todo"):
        st.session_state.clear()
        st.rerun()

# Mostrar historial de chat
for chat in st.session_state.historial:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# Entrada de pregunta
if prompt := st.chat_input("Escribe tu duda matemática aquí..."):
    st.session_state.historial.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Recuperación de contexto (RAG simplificado)
        fallas = ", ".join(set(st.session_state.fallas_diagnostico))
        instruccion = (
            f"Eres un tutor breve para {st.session_state.nombre}. "
            f"El alumno tiene debilidad en: {fallas}. "
            "Usa números grandes con $$ y responde en máximo 3 pasos claros."
        )
        
        try:
            with st.spinner("Consultando al tutor..."):
                response = model.generate_content(f"{instruccion}. Pregunta: {prompt}")
                texto_final = response.text
                st.markdown(texto_final)
                hablar(texto_final)
                st.session_state.historial.append({"role": "assistant", "content": texto_final})
                
                # Imagen de apoyo automática según el tema
                if "/" in prompt or "fraccion" in prompt.lower():
                    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Fraction_addition.svg/1200px-Fraction_addition.svg.png", width=400)
                
        except Exception as e:
            # ESCUDO CONTRA ERROR 429
            if "429" in str(e) or "ResourceExhausted" in str(e):
                st.warning("🚀 ¡Vas muy rápido! El tutor está recargando. Por favor, reintenta en 15 segundos.")
            else:
                st.error(f"Aviso técnico: {e}")
