import streamlit as st
import requests
from datetime import datetime

# --- Lógica Principal ---
# Título dinámico

# if "title" not in st.session_state:
#     st.session_state.title = "🚀 Nueva Conversación"
    
# if "current_conversation_id" not in st.session_state:
#     st.session_state.title = "🚀 Nueva Conversación"
# current_conversation_id será None al inicio (Estado de "Chat Nuevo")
# if "current_conversation_id" not in st.session_state:
#     st.session_state.current_conversation_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []
    # st.session_state.title = "🚀 Nueva Conversación"
    
    
    


# if st.session_state.current_conversation_id is None:
#     st.title(st.session_state.title)
    
#     st.info("Escribe algo para comenzar. El chat se guardará automáticamente.")
# else:
#     st.session_state.title  = "💬 Chat Activo"
#     st.title("probando probando" )


    
if st.button("Change title"):
    st.session_state.title  = "💬 Chat Activo"
else:
    st.session_state.title  = "🚀 Nueva Conversación"
    # st.title(st.session_state.title)
    # st.write("Why hello there")
    
st.write(st.session_state.title)
    


# def changeTitle(prompt):
#     # 1. Si es un chat nuevo (ID es None), lo creamos AHORA
#     if st.session_state.current_conversation_id is None:
#         new_id = create_new_conversation(prompt)
#         if new_id:
#             st.session_state.current_conversation_id = new_id
#         else:
#             st.error("No se pudo iniciar la conversación en la DB. El mensaje no se guardará.")

#     st.session_state.title = st.session_state.title_input
#     st.session_state.icon = st.session_state.icon_input