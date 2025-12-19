import requests
import streamlit as st

API_URL = "http://api:8000"
API_POINT_ENTRY_URL = f"{API_URL}/getResponseWithQuery"

st.title("¡¡¡¡¡Vamos con el pedazo de promt!!!")

prompt = st.chat_input("Pregunta lo que quieras!")
if prompt:
    st.write("Generando la respuesta... Espere un segundo")
    response = requests.get(API_POINT_ENTRY_URL, params={"query": prompt})
    json = response.json()
    print("Respuesta en json: ", json)
    contenido  = json['response']
    st.write("ChatGPT supersayayin: ", contenido)

# if not access_token or not user_id:
#     st.error("Please log in to view saved books.")
#     st.stop()


# with st.chat_message("user"):
#     st.write("Hello 👋")
# headers = {"Authorization": f"Bearer {access_token}"}
# response = requests.get(SAVED_BOOKS_URL, params={"user_id": user_id}, headers=headers)

# if response.status_code != 200:
#     st.error("Failed to load saved books.")
#     st.stop()

# saved_books = response.json()

# for book in saved_books:
#     st.subheader(book["title"])
#     st.write(f"**Author(s):** {book['authors']}")
#     st.write(f"**Published:** {book.get('published_date', 'N/A')}")
#     st.markdown("---")