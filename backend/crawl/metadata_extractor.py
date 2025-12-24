import requests
from bs4 import BeautifulSoup

# def get_page_title(url):
#     try:
#         # 1. Hacemos la petición a la web
#         response = requests.get(url, timeout=5)
        
#         # 2. Pasamos el HTML a BeautifulSoup
#         soup = BeautifulSoup(response.text, 'html.parser')
        
#         # 3. Pillamos el contenido de la etiqueta <title>
#         # .string saca solo el texto: "Trabajador autónomo: alta y configuración..."
#         if soup.title:
#             return soup.title.string.strip()
        
#         return "Título no disponible"
#     except Exception as e:
#         return f"Error: {e}"
    
    
def generate_title_from_url(url):
    try:
        # 1. Quitamos posibles barras al final y pillamos la última parte
        slug = url.strip("/").split("/")[-1]
        
        # 2. Reemplazamos guiones por espacios
        title = slug.replace("-", " ")
        
        # 3. Ponemos la primera letra en mayúscula (Capitalize)
        return title.capitalize()
    except:
        return url # Si algo falla, devolvemos el link tal cual