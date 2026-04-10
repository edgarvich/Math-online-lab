import streamlit as st
import google.generativeai as genai

# 1. Configuración de la API
if "GOOGLE_API_KEY" in st.secrets:
    # Forzamos la configuración para que no busque en v1beta
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 2. Configuración de la página
st.set_page_config(page_title="Math AI Lab", page_icon="🎓")
st.title("👨‍🏫 Math AI Lab: Pizarra y Tutor")

# 3. Cargar el modelo de forma estable
# Usar 'gemini-1.5-flash' sin el prefijo models/ suele ser más compatible en versiones nuevas
model = genai.GenerativeModel('gemini-1.5-flash')

# 4. Interfaz
tema = st.text_input("Tema de hoy:", placeholder="Ej: suma de fracciones")

if st.button("Crear Pizarra"):
    if tema:
        try:
            with st.spinner("Generando explicación..."):
                # Especificamos el contenido
                res = model.generate_content(f"Explica de forma sencilla: {tema}")
                st.markdown("### 📝 Contenido de la Pizarra:")
                st.write(res.text)
        except Exception as e:
            # Si falla, intentamos con el nombre largo por si acaso
            try:
                model_alt = genai.GenerativeModel('models/gemini-1.5-flash')
                res = model_alt.generate_content(f"Explica brevemente {tema}")
                st.markdown("### 📝 Explicación:")
                st.write(res.text)
            except:
                st.error(f"Error de conexión con Google: {e}")
    else:
        st.warning("Por favor, escribe un tema.")

st.divider()
st.caption("Proyecto de Maestría - Edgar Romero Valero")
