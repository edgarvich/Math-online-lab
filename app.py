import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

# Configuración ligera
st.set_page_config(page_title="Math Lab Fast", layout="centered")

api_key = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# --- OPTIMIZACIÓN DE VELOCIDAD ---
generation_config = {
  "temperature": 0.3, # Menos "creatividad", más precisión
  "top_p": 0.9,
  "max_output_tokens": 250, # Respuestas cortas = carga rápida
}

model = genai.GenerativeModel(
    model_name='models/gemini-2.5-flash',
    generation_config=generation_config
)

def hablar(texto):
    texto_limpio = texto.replace("$", "").replace("*", "").replace("\n", " ")
    js_code = f"<script>var msg = new SpeechSynthesisUtterance('{texto_limpio}'); msg.lang='es-ES'; window.speechSynthesis.speak(msg);</script>"
    components.html(js_code, height=0)

# --- FLUJO SIMPLIFICADO ---
if "nombre" not in st.session_state:
    st.title("Math-Lab 🎓")
    nombre = st.text_input("Tu nombre:")
    if st.button("Entrar"):
        st.session_state.nombre = nombre
        st.rerun()
    st.stop()

st.subheader(f"Tutor Virtual: {st.session_state.nombre}")

if prompt := st.chat_input("Duda rápida..."):
    with st.chat_message("assistant"):
        try:
            # Instrucción de precisión
            instruccion = f"Eres un tutor breve para {st.session_state.nombre}. Responde en máximo 3 pasos usando $$ para números."
            
            response = model.generate_content(f"{instruccion}. Pregunta: {prompt}")
            st.markdown(response.text)
            hablar(response.text)
            
            # Imagen solo si es estrictamente necesario
            if "/" in prompt:
                st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Fraction_addition.svg/1200px-Fraction_addition.svg.png", width=400)

        except Exception as e:
            st.warning("Servidor ocupado. Reintenta en 10 segundos.")
