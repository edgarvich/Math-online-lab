import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página profesional
st.set_page_config(page_title="Math-Online-Lab Visual", layout="wide")

# 2. Configuración de API
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ Configura GEMINI_API_KEY en Secrets.")
    st.stop()

genai.configure(api_key=api_key)
# Usando el modelo detectado en el servidor para evitar errores 404
model = genai.GenerativeModel('models/gemini-2.5-flash')

# --- 3. BANCO DE IMÁGENES EDUCATIVAS ---
# Estas son URLs reales para apoyo visual
IMAGEN_MCD = "https://i.ibb.co/L8yHh9M/mcd-visual.png" # Ejemplo de MCD visual
IMAGEN_UNIDADES = "https://i.ibb.co/P4Z9h6X/fraction-units.png" # Fracciones básicas

# --- 4. SISTEMA DE LOGIN (Personalización) ---
if "nombre_usuario" not in st.session_state:
    st.title("Bienvenido al Math-Online-Lab 🎓")
    nombre = st.text_input("Ingresa tu nombre para comenzar:")
    if st.button("Empezar"):
        if nombre:
            st.session_state.nombre_usuario = nombre
            st.session_state.messages = []
            st.rerun()
    st.stop()

# --- 5. INTERFAZ DE CHAT ---
st.title(f"Tutoría Visual para {st.session_state.nombre_usuario} 👋")
st.markdown("---")

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "img" in message:
            st.image(message["img"], width=500)

# Entrada de texto (Chatbot)
if prompt := st.chat_input("Escribe tu problema (ej: 1/2 + 1/3)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("El tutor está buscando la mejor imagen para explicarte..."):
            try:
                # INSTRUCCIÓN MAESTRA: Forzamos el uso de imágenes y números grandes
                instruccion = (
                    f"Eres un tutor de matemáticas visual para {st.session_state.nombre_usuario}. "
                    "Tu respuesta DEBE ser ultra-corta. Usa números grandes o viñetas. "
                    "Si el problema es de fracciones, di: 'Necesitas un DENOMINADOR COMÚN'."
                )
                
                response = model.generate_content(f"{instruccion}. Problema: {prompt}")
                texto_tutor = response.text
                
                # Formateamos el texto para que los números sean grandes (Usando Markdown)
                texto_visual = texto_tutor.replace(" -> ", " ➡ ").replace(" = ", " ⚌ ")
                st.markdown(texto_visual)
                
                # --- LÓGICA DE IMÁGENES AUTOMÁTICAS ---
                imagen_a_mostrar = None
                
                # Detectamos si es un problema de fracciones
                if any(palabra in prompt or palabra in texto_tutor.lower() for palabra in ["1/2", "denominador", "fraccion"]):
                    imagen_a_mostrar = IMAGEN_MCD
                
                # Mostramos la imagen pedagógica
                if imagen_a_mostrar:
                    st.image(imagen_a_mostrar, caption="Observa cómo los convertimos para que sean iguales", width=500)
                    st.session_state.messages.append({"role": "assistant", "content": texto_visual, "img": imagen_a_mostrar})
                else:
                    st.session_state.messages.append({"role": "assistant", "content": texto_visual})
                    
            except Exception as e:
                st.error(f"Error técnico: {e}")
