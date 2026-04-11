import streamlit as st
import google.generativeai as genai
from streamlit_drawable_canvas import st_canvas
from streamlit_mic_recorder import mic_recorder
from PIL import Image
import numpy as np

# Configuración de la página
st.set_page_config(page_title="Math-Online-Lab", layout="wide")

# Configuración de API
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("Configura GEMINI_API_KEY en Secrets.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("Math-Online-Lab 🎓")
st.caption("Tutoría Matemática con IA: Pizarra, Chat y Voz")

# --- INTERFAZ DE COLUMNAS ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Pizarra de Razonamiento")
    canvas_result = st_canvas(
        stroke_width=4, stroke_color="#000000", background_color="#ffffff",
        height=350, drawing_mode="freedraw", key="canvas"
    )
    
    st.write("🎤 **¿Tienes una duda? Háblale al tutor:**")
    audio = mic_recorder(start_prompt="Grabar voz", stop_prompt="Detener", key='recorder')

with col2:
    st.subheader("Chat con el Tutor")
    
    # Memoria del Chatbot
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostrar historial
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Función para procesar la entrada (Voz o Texto)
    def procesar_tutor(texto_usuario, imagen=None):
        with st.chat_message("assistant"):
            try:
                # Prompt de Scaffolding (Andamiaje pedagógico)
                instruccion = "Eres un tutor experto. No des la respuesta. Haz preguntas para que el alumno razone."
                contenido = [instruccion, texto_usuario]
                if imagen:
                    contenido.append(imagen)
                
                response = model.generate_content(contenido)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Error: {e}")

    # Si hay grabación de voz
    if audio:
        texto_voz = "He enviado una nota de voz con mi duda sobre el ejercicio."
        st.session_state.messages.append({"role": "user", "content": texto_voz})
        # (Nota: Para transcripción real de audio necesitaríamos Whisper, 
        # por ahora el tutor reacciona al envío del audio).
        procesar_tutor("El alumno te ha hablado. Analiza la imagen y responde a su duda.")

    # Chatbot (Entrada de texto)
    if prompt := st.chat_input("Escribe tu duda aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Si hay algo en la pizarra, se lo enviamos
        img = None
        if canvas_result.image_data is not None:
            img = Image.fromarray(canvas_result.image_data.astype(np.uint8)).convert("RGB")
        
        procesar_tutor(prompt, img)
