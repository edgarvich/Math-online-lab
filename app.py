import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página
st.set_page_config(page_title="Math-Online-Lab", layout="wide")

# 2. Configuración de API
api_key = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-2.5-flash')

# --- 3. BANCO DE IMÁGENES EDUCATIVAS ---
IMAGENES = {
    "fracciones": "https://img.freepik.com/vector-premium/suma-fracciones-distinto-denominador-metodo-minimo-comun-multiplo-matematicas_102902-2341.jpg",
    "basico": "https://calculo.cc/temas/temas_primaria/fracciones/imagenes/suma_resta_mismo_denominador.gif"
}

# --- 4. SISTEMA DE LOGIN ---
if "nombre_usuario" not in st.session_state:
    st.title("Math-Online-Lab 🎓")
    nombre = st.text_input("Ingresa tu nombre:")
    if st.button("Empezar"):
        if nombre:
            st.session_state.nombre_usuario = nombre
            st.session_state.messages = []
            st.rerun()
    st.stop()

# --- 5. INTERFAZ DE CHAT ---
st.title(f"Tutoría para {st.session_state.nombre_usuario} 👋")

# Mostrar historial
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Si el mensaje tiene una imagen guardada y el usuario decidió verla
        if "img_url" in message and st.session_state.get(f"ver_img_{i}", False):
            st.image(message["img_url"], width=500)

# Entrada de Chat
if prompt := st.chat_input("Escribe tu duda aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Instrucción de tutoría personalizada
            contexto = f"Eres un tutor experto. Llama a {st.session_state.nombre_usuario} por su nombre. Explica sin dar la respuesta. Si el tema es difícil, dile que tienes una imagen de apoyo si la necesita."
            response = model.generate_content(f"{contexto}. Duda: {prompt}")
            
            respuesta_texto = response.text
            st.markdown(respuesta_texto)
            
            # Guardamos la respuesta en el historial
            new_msg = {"role": "assistant", "content": respuesta_texto}
            
            # Si el tema es de fracciones, preparamos la imagen oculta
            if "1/2" in prompt or "fracción" in respuesta_texto.lower():
                new_msg["img_url"] = IMAGENES["fracciones"]
            
            st.session_state.messages.append(new_msg)
            st.rerun() # Refrescamos para mostrar el botón de ayuda visual
        except Exception as e:
            st.error(f"Error: {e}")

# --- 6. BOTÓN DE APOYO VISUAL (Solo aparece si el tutor tiene una imagen lista) ---
if st.session_state.messages and "img_url" in st.session_state.messages[-1]:
    st.write("---")
    if st.button(f"🔍 {st.session_state.nombre_usuario}, ¿deseas ver una imagen de apoyo para este paso?"):
        # Guardamos que el usuario quiere ver la imagen del último mensaje
        last_idx = len(st.session_state.messages) - 1
        st.session_state[f"ver_img_{last_idx}"] = True
        st.rerun()
