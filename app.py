import streamlit as st
import google.generativeai as genai

# 1. Configuración de la API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 2. Configuración estética
st.set_page_config(page_title="Math AI Lab", page_icon="🎓")
st.title("👨‍🏫 Math AI Lab: Pizarra y Tutor")

# 3. Modelo (NOMBRE CORREGIDO)
model = genai.GenerativeModel('models/gemini-1.5-flash')

# 4. Interfaz
tema = st.text_input("Tema de hoy:", placeholder="Ej: suma de fracciones")

if st.button("Crear Pizarra"):
    if tema:
        try:
            with st.spinner("El profesor está escribiendo..."):
                # Usamos el modelo corregido
                res = model.generate_content(f"Explica brevemente {tema} con un ejemplo.")
                st.markdown("### 📝 Explicación:")
                st.write(res.text)
        except Exception as e:
            st.error(f"Error técnico: {e}")
    else:
        st.warning("Escribe un tema primero.")

st.divider()
st.caption("Proyecto de Maestría - Edgar Romero Valero")
