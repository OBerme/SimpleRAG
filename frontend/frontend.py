import streamlit as st
import requests

API_URL = "http://api:8000"
API_POINT_ENTRY_URL = f"{API_URL}/getResponseWithQuery"

st.title("¡¡¡¡¡Vamos con el pedazo de promt!!!")

with st.sidebar:
    st.title('🤖💬 OpenAI Chatbot')
    st.button("Este es tu anterior chat")
    # if 'OPENAI_API_KEY' in st.secrets:
    #     st.success('API key already provided!', icon='✅')
    #     openai.api_key = st.secrets['OPENAI_API_KEY']
    # else:
    #     openai.api_key = st.text_input('Enter OpenAI API token:', type='password')
    #     if not (openai.api_key.startswith('sk-') and len(openai.api_key)==51):
    #         st.warning('Please enter your credentials!', icon='⚠️')
    #     else:
    st.success('Proceed to entering your prompt message!', icon='👉')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Quiero dar de alta un trabajador en la seguridad social"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # for response in openai.ChatCompletion.create(
            # model="gpt-3.5-turbo",
            # messages=[{"role": m["role"], "content": m["content"]}
            #           for m in st.session_state.messages], stream=True):
            # full_response += response.choices[0].delta.get("content", "")
        response = requests.get(API_POINT_ENTRY_URL, params={"query": prompt})
        
        data = response.json()
                
        # Suponiendo que tu API devuelve algo como {"response": "texto..."}
        # Cambia "response" por la clave exacta que devuelva tu FastAPI
        answer = data.get("response", "No se encontró el campo 'response' en la respuesta")
        answer = answer[0]
        # Lo mostramos como Markdown
        message_placeholder.markdown(answer)
        
        # Guardamos en el historial del chat
        st.session_state.messages.append({"role": "assistant", "content": answer})
    # st.session_state.messages.append({"role": "assistant", "content": full_response})