import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página
st.set_page_config(page_title="Math AI Lab", page_icon="🎓")
st.title("👨‍🏫 Math AI Lab: Pizarra y Tutor")

# 2. Configuración de la API (Sencilla y Directa)
if "GOOGLE_API_KEY" in st.secrets:
    # Usamos la configuración estándar que funciona en todas las regiones
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("No se encontró la clave de API.")

# 3. Cargar el modelo estable
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. Interfaz de usuario
tema = st.text_input("¿Qué vamos a aprender hoy?", placeholder="Ej: Suma de fracciones")

if st.button("Generar Material"):
    if tema:
        try:
            with st.spinner("El profesor virtual está escribiendo..."):
                # Generamos el contenido
                response = model.generate_content(f"Actúa como un profesor de primaria. Explica de forma sencilla: {tema}")
                st.markdown("### 📝 Contenido Sugerido para la Pizarra:")
                st.write(response.text)
        except Exception as e:
            st.error(f"Hubo un detalle al conectar con Google. Por favor, intenta de nuevo en un momento.")
            # Mostramos el error técnico solo en consola para no ensuciar la pizarra
            print(f"Error técnico: {e}")
    else:
        st.warning("Por favor, escribe un tema primero.")

st.divider()
st.caption("Proyecto de Maestría en Tecnología Educativa - Edgar Romero Valero")
