import streamlit as st
import requests
from datetime import datetime
# from API.APIParser import get_list_response
SPLIT_KEY_STR = '---------------'
SPLIT_LINKS_STR = '@@@@@@@@@@@@@@@'
SPLIT_LINKS_SEPARATOR = ','

def get_list_response(response):
    split_sum_up = response.split(SPLIT_KEY_STR, 2)
    sum_up = split_sum_up[1]
    split_links = sum_up.split(SPLIT_LINKS_STR,2)
    
    return [ split_sum_up[0], split_links[0], split_links[1]]


def get_list_links(links):
    return links.split(SPLIT_LINKS_SEPARATOR, 2)

# --- Configuración de URLs ---
# URL de tu API original (la que procesa el prompt)
API_URL = "http://api-chatgpt:8000"
API_POINT_ENTRY_URL = f"{API_URL}/getResponseWithQuery"

# URL de la nueva API para guardar conversaciones en MongoDB
# Asumimos que correrá en el puerto 8001 localmente
CONVERSATIONS_API_URL = "http://db-backend:8001"


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
    except:
        st.error("Error al registrar la nueva conversación en la base de datos.")
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


        
# Input del usuario
if prompt := st.chat_input("¿En qué puedo ayudarte?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 2. Lógica de visualización y guardado
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 3. Respuesta del Asistente
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            response = requests.get(API_POINT_ENTRY_URL, params={"query": prompt})
            data = response.json()
            
            list_response = data.get("response", "Sin respuesta.")
            response_parsed = get_list_response(list_response[0])
            
            answer = response_parsed[0]
            
            # Limpieza de formato si viene en lista
            if isinstance(answer, list):
                answer = answer[0] if answer else "Lista vacía."
            
            title =  response_parsed[1]
            
            links =  response_parsed[2]
            list_links = get_list_links(links)
            
            ## Escribimos dónde se ha guardado la conversación
            answer += "\n" "Se ha guardado la conversación como: " + title
            
            answer += "\n" + "Links de utilidad: "
            for next_link in list_links:    
                answer += "\n" + next_link
                
            
            
            
            message_placeholder.markdown(answer)
            if st.session_state.current_conversation_id is None:
                
                new_id = create_new_conversation(prompt, title)
                if new_id:
                    st.session_state.current_conversation_id = new_id
                else:
                    st.error("No se pudo iniciar la conversación en la DB. El mensaje no se guardará.")
                    
            # 4. GUARDAR en DB (si tenemos ID)
            if st.session_state.current_conversation_id: 
                save_message_to_db(st.session_state.current_conversation_id, "user", prompt)
            
            # 4. Guardado final
            st.session_state.messages.append({"role": "assistant", "content": answer})
            save_message_to_db(st.session_state.current_conversation_id, "assistant", answer)
            
            
            
            
        except Exception as e:
            message_placeholder.error(f"Error de conexión: {e}")
else:
    if "title" in st.session_state and st.session_state.title is not None:
            st.title(st.session_state.title)
    else:
        st.title("🚀 Nueva Conversación")



# Mostrar mensajes existentes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    