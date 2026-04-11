import streamlit as st
import google.generativeai as genai
import streamlit.components.v1 as components
import time

# ... (Configuración inicial igual al código anterior)

# --- FUNCIÓN PARA GENERAR RESPUESTA CON REINTENTO AUTOMÁTICO ---
def obtener_respuesta_tutor(instruccion, pregunta):
    try:
        # Intentamos la conexión
        response = model.generate_content(f"{instruccion}. Pregunta: {pregunta}")
        return response.text, False # Retorna el texto y 'False' porque NO hay error
    except Exception as e:
        # Si hay error de cuota (429), avisamos al sistema
        return str(e), True

# --- INTERFAZ DEL CHAT ---
if prompt := st.chat_input("Duda rápida..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        instruccion = f"Eres un tutor breve para {st.session_state.nombre}. Responde claro y con $$."
        
        # Llamamos a la función de ayuda
        respuesta, hubo_error = obtener_respuesta_tutor(instruccion, prompt)
        
        if hubo_error:
            if "429" in respuesta or "ResourceExhausted" in respuesta:
                st.warning("⚠️ El tutor está recargando energías. Por favor, espera 15 segundos y presiona ENTER de nuevo.")
                # Esto es clave: no guardamos el error en el historial para no bloquear la app
            else:
                st.error(f"Aviso técnico: {respuesta}")
        else:
            # SI NO HAY ERROR: Mostramos la respuesta y activamos la voz
            st.markdown(respuesta)
            hablar(respuesta)
            
            # Soporte visual dinámico
            if "/" in prompt:
                st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Fraction_addition.svg/1200px-Fraction_addition.svg.png", width=400)
