import streamlit as st
import google.generativeai as genai

# Forzamos la configuración más básica
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("Prueba de Conexión")

# Usamos el modelo 'gemini-pro' que es el más antiguo y compatible
if st.button("Probar IA"):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Hola, di 'Conexión exitosa'")
        st.write(response.text)
    except Exception as e:
        st.error(f"Error detectado: {e}")
