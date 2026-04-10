import streamlit as st
import google.generativeai as genai

# 1. Configuración de la API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.set_page_config(page_title="Math AI Lab", page_icon="🎓")
st.title("👨‍🏫 Math AI Lab: Pizarra y Tutor")

# 2. MODELO UNIVERSAL (Este tiene mayor compatibilidad regional)
model = genai.GenerativeModel('gemini-pro')

tema = st.text_input("¿Qué vamos a aprender hoy?", placeholder="Ej: Suma de fracciones")

if st.button("Generar Material"):
    if tema:
        try:
            with st.spinner("Conectando con el servidor de Google..."):
                # Pedimos la explicación
                response = model.generate_content(f"Actúa como un profesor. Explica brevemente: {tema}")
                st.markdown("### 📝 Contenido Sugerido:")
                st.write(response.text)
        except Exception as e:
            # Si gemini-pro también falla, es la API KEY
            st.error("Error de autenticación. Por favor, revisa que tu API KEY en Secrets sea correcta y no tenga espacios.")
            st.info("Asegúrate de que en Secrets diga: GOOGLE_API_KEY = 'Tu_Clave_Aquí'")
    else:
        st.warning("Escribe un tema primero.")

st.divider()
st.caption("Proyecto de Maestría en Tecnología Educativa - Edgar Romero Valero")
