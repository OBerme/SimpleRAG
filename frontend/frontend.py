import streamlit as st
import requests
import traceback  
from datetime import datetime
# from API.APIParser import get_list_response

DEBUG_MODE = True
DEBUG_MODE_RESPONSE = False

# --- Configuración de URLs ---
# URL de tu API original (la que procesa el prompt)
# API_URL = "http://api-chatgpt:8000"
API_URL = "http://172.17.0.1:8000"
API_POINT_ENTRY_URL = f"{API_URL}/getResponseWithQuery"

# URL de la nueva API para guardar conversaciones en MongoDB
# Asumimos que correrá en el puerto 8001 localmente
# CONVERSATIONS_API_URL = "http://db-backend:8001"
CONVERSATIONS_API_URL = "http://mongo-db-backend:8001"


def create_new_conversation(first_query, title):
    """Crea la conversación en DB usando el primer mensaje como referencia para el título."""
    try:
        # Usamos los primeros 20 caracteres del prompt como título para que sea descriptivo
        # title = f"{first_query[:20]}..." if len(first_query) > 20 else first_query
        response = requests.post(
            f"{CONVERSATIONS_API_URL}/conversations/create",
            json={"title": title, "user_id": "default_user"}
        )
        if response.status_code == 200:
            return response.json()["conversation_id"]
    except Exception as e:
        st.error("Error al registrar la nueva conversación en la base de datos.", e)
    return None

def get_conversations():
    try:
        response = requests.get(f"{CONVERSATIONS_API_URL}/conversations/list?user_id=default_user")
        return response.json()["conversations"] if response.status_code == 200 else []
    except:
        return []
    
def save_message_to_db(conversation_id, role, content):
    if not conversation_id: return
    try:
        requests.post(
            f"{CONVERSATIONS_API_URL}/conversations/{conversation_id}/messages",
            json={"role": role, "content": content}
        )
    except: pass

def load_messages_from_db(conversation_id):
    try:
        response = requests.get(f"{CONVERSATIONS_API_URL}/conversations/{conversation_id}/messages")
        if response.status_code == 200:
            return [{"role": m["role"], "content": m["content"]} for m in response.json()["messages"]]
    except: return []
    return []


# --- Gestión del Estado de la Sesión ---

# current_conversation_id será None al inicio (Estado de "Chat Nuevo")
if "current_conversation_id" not in st.session_state:
    st.session_state.current_conversation_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar ---

with st.sidebar:
    st.title('🤖💬 Chatbot a3responde')
    
    # Al pulsar "Nuevo Chat", simplemente reseteamos el estado a None (puntero a chat nuevo)
    if st.button("➕🚀 Nueva conversacion", use_container_width=True):
        
        st.session_state.current_conversation_id = None
        st.session_state.title = None
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.subheader("Historial")
    for chat in get_conversations():
        if st.button(f"💬 {chat['title']}", key=chat["id"], use_container_width=True):
            st.session_state.current_conversation_id = chat["id"]
            st.session_state.title = chat['title']
            st.session_state.messages = load_messages_from_db(chat["id"])
            st.rerun()

if "title" in st.session_state and st.session_state.title is not None:
    st.title(st.session_state.title)

# Mostrar mensajes existentes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
# Input del usuario
if prompt := st.chat_input("¿En qué puedo ayudarte?"):
    
    # Añadimos y mostramos el mensaje del usuario inmediatamente
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Respuesta del Asistente
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            response = requests.get(API_POINT_ENTRY_URL, params={"query": prompt})
            
            if DEBUG_MODE_RESPONSE : st.write(response)
            
            data = (response.json())['response']
            if 'error' not in data :
                
                
                    
                answer = data['answer'] # Aprovechamos para limpiar los \n
                title = data['chat_title']
                links = data['links']
                
                # answer= "esto seria la respuesta del texto"
                # links=["link 1", "link 2", "link 3"]
                # title="nombre del chat"
                
                # st.session_state.messages.append({"role": "assistant", "content": response}) # mostrar código de resultado
                
                
                # # Formatear la respuesta final
                full_answer = f"{answer}\n\n**Enlaces de interés:**\n\n"
                for link in links:
                    full_answer += f"📄 [{link.get('title')}]({link.get('raw_link')})\n\n"
                
                message_placeholder.markdown(full_answer)

                # --- GESTIÓN DE BASE DE DATOS ---
                if st.session_state.current_conversation_id is None:
                    # Si es nuevo, creamos la conversación con el título de la IA
                    new_id = create_new_conversation(prompt, title)
                    if new_id:
                        st.session_state.current_conversation_id = new_id
                        st.session_state.title = title
                        
                
                # Guardar en memoria y DB
                save_message_to_db(st.session_state.current_conversation_id, "user", prompt)
                save_message_to_db(st.session_state.current_conversation_id, "assistant", full_answer)
                st.session_state.messages.append({"role": "assistant", "content": full_answer})
                
                # Forzamos rerun para que el título de la página se actualice arriba
                st.rerun()
            else:
                st.write(data['error']['message'])
                
        # except Exception as e:
        #     if DEBUG_MODE:
        #         # Capturamos el error completo
        #         error_detallado = traceback.format_exc()
                
        #         # Lo imprimimos en la consola/terminal para que tú lo veas
        #         print(error_detallado)
                
        #         # En Streamlit, puedes mostrarlo en un desplegable para que no ensucie la UI
        #         with st.expander("Ver detalles del error"):
        #             st.code(error_detallado)
                
        #         message_placeholder.error(f"Error: {e}")
                
        #     else:
        #         message_placeholder.error(f"Error: {e}")
# else:
#     if "title" not in st.session_state or st.session_state.title is None:
st.title("WEB EN MANTENIMIENTO!!!!!")
st.write("Los resultados de la web están siendo testeados. Si quiere probar la versión definitiva escriba a Óscar Bermejo Domínguez https://teams.microsoft.com/l/chat/48:notes/conversations?context=%7B%22contextType%22%3A%22chat%22%7D")


    