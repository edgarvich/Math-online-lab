import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Math Online Lab")

api_key = st.secrets.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# USANDO EL MODELO DETECTADO EN EL SERVIDOR
model = genai.GenerativeModel('models/gemini-2.5-flash')

st.title("Math-Online-Lab Chat 🎓")

if prompt := st.chat_input("Escribe: YOU SOLVE 1/2 + 1/3"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(f"Eres un tutor experto. Explica paso a paso: {prompt}")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
