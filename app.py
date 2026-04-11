import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components

st.set_page_config(page_title="Math-Online-Lab Voz", layout="wide")

# Configuración de API
api_key = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-2.5-flash')

# --- FUNCIÓN DE VOZ (JavaScript) ---
def leer_en_voz_alta(texto):
    # Este script usa el sintetizador nativo del navegador (Chrome/Edge/Safari)
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance('{texto.replace("'", "")}');
    msg.lang = 'es-ES';
    msg.rate = 0.9; 
    window.speechSynthesis.speak(msg);
    </script>
    """
    components.html(js_code, height=0)

# --- INTERFAZ ---
st.title(f"Tutoría por Voz para {st.session_state.get('nombre', 'Edgar')} 🔊")

if prompt := st.chat_input("Dime tu duda sobre fracciones..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Instrucción enfocada solo en fracciones
            guion = (
                f"Eres un tutor experto en fracciones. Llama a {st.session_state.get('nombre', 'Edgar')} por su nombre. "
                "Usa números GRANDES con $$. Explica paso a paso de forma muy breve."
            )
            response = model.generate_content(f"{guion}. Pregunta: {prompt}")
            texto_respuesta = response.text
            
            # 1. Mostrar Texto
            st.markdown(texto_respuesta)
            
            # 2. Mostrar Imagen de Apoyo
            if "/" in prompt:
                st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Fraction_addition.svg/1200px-Fraction_addition.svg.png", 
                         caption="Visualización: El concepto de partes iguales", width=500)
                

            # 3. ACTIVAR VOZ AUTOMÁTICA
            # Limpiamos símbolos raros para que la voz sea fluida
            texto_para_voz = texto_respuesta.replace("$", "").replace("#", "").replace("*", "")
            leer_en_voz_alta(texto_para_voz)
            
        except Exception as e:
            st.error(f"Error: {e}")
