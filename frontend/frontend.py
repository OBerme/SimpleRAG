import streamlit as st
import requests
from datetime import datetime

# --- Configuración de URLs ---
# URL de tu API original (la que procesa el prompt)
API_URL = "http://api-chatgpt:8000"
API_POINT_ENTRY_URL = f"{API_URL}/getResponseWithQuery"

# URL de la nueva API para guardar conversaciones en MongoDB
# Asumimos que correrá en el puerto 8001 localmente
CONVERSATIONS_API_URL = "http://db-backend:8001"

st.title("¡¡¡¡¡Vamos con el pedazo de promt!!!")

# --- Funciones Helper para MongoDB ---

def create_new_conversation():
    """Crea una nueva conversación en la base de datos y retorna su ID."""
    try:
        title = f"Chat {datetime.now().strftime('%d/%m %H:%M')}"
        response = requests.post(
            f"{CONVERSATIONS_API_URL}/conversations/create",
            json={"title": title, "user_id": "default_user"}
        )
        if response.status_code == 200:
            return response.json()["conversation_id"]
    except requests.exceptions.ConnectionError:
        st.error("No se pudo conectar con la base de datos de conversaciones (MongoDB API).")
    return None

def get_conversations():
    """Obtiene la lista de conversaciones guardadas."""
    try:
        response = requests.get(f"{CONVERSATIONS_API_URL}/conversations/list?user_id=default_user")
        if response.status_code == 200:
            return response.json()["conversations"]
    except:
        return []
    return []

def save_message_to_db(conversation_id, role, content):
    """Guarda un mensaje individual en la base de datos."""
    if not conversation_id:
        return
    try:
        requests.post(
            f"{CONVERSATIONS_API_URL}/conversations/{conversation_id}/messages",
            json={"role": role, "content": content}
        )
    except:
        pass

def load_messages_from_db(conversation_id):
    """Carga el historial de mensajes de una conversación específica."""
    try:
        response = requests.get(f"{CONVERSATIONS_API_URL}/conversations/{conversation_id}/messages")
        conversation_id
        if response.status_code == 200:
            # Convertimos el formato de la DB al formato de session_state
            db_messages = response.json()["messages"]
            return [{"role": msg["role"], "content": msg["content"]} for msg in db_messages]
    except:
        return []
    return []

# --- Gestión del Estado de la Sesión ---

if "current_conversation_id" not in st.session_state:
    st.session_state.current_conversation_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar ---

with st.sidebar:
    st.title('🤖💬 OpenAI Chatbot')
    
    # Botón para crear nuevo chat
    if st.button("➕ Nuevo chat", use_container_width=True):
        new_id = create_new_conversation()
        if new_id:
            st.session_state.current_conversation_id = new_id
            st.session_state.messages = [] # Limpiamos la vista actual
            st.rerun() # Recargamos para mostrar el nuevo estado

    st.divider()
    st.subheader("Historial de Conversaciones")

    # Cargar y mostrar lista de conversaciones como botones
    saved_conversations = get_conversations()
    
    if not saved_conversations:
        st.caption("No hay conversaciones guardadas.")
    
    for chat in saved_conversations:
        # Definimos el estilo del botón (resaltar si es el actual)
        chat_id = chat["id"]
        title = chat["title"]
        msg_count = chat.get("message_count", 0)
        
        # Usamos un key único para cada botón
        if st.button(f"💬 {title} ({msg_count})", key=chat_id, use_container_width=True):
            st.session_state.current_conversation_id = chat_id
            st.session_state.messages = load_messages_from_db(chat_id)
            st.rerun()

    st.divider()
    st.success('Proceed to entering your prompt message!', icon='👉')

# --- Lógica Principal del Chat ---

# Si no hay conversación activa, creamos una automáticamente al inicio o pedimos crearla
if st.session_state.current_conversation_id is None:
    # Opcional: Crear una automáticamente si es la primera vez
    if st.button("Comenzar una nueva conversación"):
        new_id = create_new_conversation()
        if new_id:
            st.session_state.current_conversation_id = new_id
            st.rerun()
else:
    # Mostrar mensajes del historial actual
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input del usuario
    if prompt := st.chat_input("Quiero dar de alta un trabajador en la seguridad social"):
        # 1. Mostrar y guardar mensaje del usuario en session_state
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # 2. Guardar mensaje del usuario en MongoDB
        save_message_to_db(st.session_state.current_conversation_id, "user", prompt)

        # 3. Obtener respuesta de la API
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            try:
                # Llamada a tu API original
                response = requests.get(API_POINT_ENTRY_URL, params={"query": prompt})
                data = response.json()
                
                # Procesamiento de la respuesta según tu código original
                answer = data.get("response", "No se encontró el campo 'response' en la respuesta")
                if isinstance(answer, list) and len(answer) > 0:
                    answer = answer[0]
                elif isinstance(answer, list) and len(answer) == 0:
                    answer = "La API devolvió una lista vacía."
                
                message_placeholder.markdown(answer)
                
                # 4. Guardar respuesta en session_state y MongoDB
                st.session_state.messages.append({"role": "assistant", "content": answer})
                save_message_to_db(st.session_state.current_conversation_id, "assistant", answer)
                
                # Forzar recarga del sidebar para actualizar conteo de mensajes (opcional, puede ser molesto si recarga todo)
                # st.rerun() 
                
            except Exception as e:
                error_msg = f"Error al conectar con la API: {str(e)}"
                message_placeholder.error(error_msg)
