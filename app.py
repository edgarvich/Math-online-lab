import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Fracciones Lab", layout="wide")

# Configuración con el modelo que SÍ funciona en tu servidor
api_key = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-2.5-flash')

# --- ESTADO DEL APRENDIZAJE ---
if "tema" not in st.session_state:
    st.session_state.tema = "Fracciones"
    st.session_state.mensajes = []

st.title(f"Laboratorio de {st.session_state.tema} 🍕")
st.write(f"Hola **{st.session_state.get('nombre', 'Edgar')}**, hoy nos enfocaremos solo en entender las fracciones.")

# Mostrar historial
for m in st.session_state.mensajes:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Entrada del Estudiante
if prompt := st.chat_input("Dime tu duda sobre fracciones..."):
    st.session_state.mensajes.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # INSTRUCCIÓN: Solo fracciones, números grandes, paso a paso.
        guion = (
            f"Eres un tutor experto en fracciones para {st.session_state.get('nombre', 'Edgar')}. "
            "NO hables de ecuaciones ni de secuencias. "
            "Usa números GRANDES con $$ para cada paso. "
            "Explica por qué los denominadores deben ser iguales antes de sumar."
        )
        response = model.generate_content(f"{guion}. Pregunta: {prompt}")
        st.markdown(response.text)
        st.session_state.mensajes.append({"role": "assistant", "content": response.text})
        
        # Imagen de apoyo obligatoria para fracciones
        if "/" in prompt:
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Fraction_addition.svg/1200px-Fraction_addition.svg.png", 
                     caption="Visualización: ¿Por qué necesitamos partes iguales?", width=500)
