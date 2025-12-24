from fastapi import FastAPI

from fileManager import FileManager
# from GoogleGemini.googleGeminiFilesUploaderFinal import getResponseUsingFiles, evaluar_documentos, obtener_contenidos_y_combinar
from OpenAIChatGPT.APIInterfaceCallable import getResponseUsingFiles, evaluar_documentos, obtener_contenidos_y_combinar
# from OpenAIChatGPT.APIInterfaceCallableMockApp import getResponseUsingFiles, evaluar_documentos, obtener_contenidos_y_combinar
# # from OpenAIChatGPT.APIInterfaceCallableFilesVersion import getResponseUsingFiles

from OpenAIChatGPT.parser import get_json_model_response, get_list_links, get_list_response

#Librerias para conseguir los datos de las paginas
# from crawl.crawl_interface import get_links_to_folder, get_page_title
from crawl.scraper import get_links_to_folder
from crawl.metadata_extractor import generate_title_from_url

from basicMarkdownAnaliticScraperFromUrls import scarpeMarkdownBasicInfo


import re
import json
import logging

from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)
logging.basicConfig(filename='api.log', level=logging.ERROR)
logging.basicConfig(filename='api.log', level=logging.INFO)

DEBUG_MODE = True

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-streamlit-app.streamlit.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


output_file = "enlaces_extraidos"
folder_to_save = './documentos_guardados'


@app.get("/getResponseWithQuery")
async def getResponseWithQuery(query):
    json = None
    try:
        await getLinksFromQuery(query)
        links = await getListLinksFile()
        links = links[:3]

        print("Links: ", links)

        await getFilesFromUrlsFile(links)
        json = await uploadFiles2API(query, links)
        
        
    except Exception as error:
        print(error)
        logger.error(error)
        json = {
            "error":{
                "message" : "Ocurrio un problema dentro de la API " + str(error)
            }
        }
        
    return {"response":json}
    

#@app.get("/getLinksFromQuery")
async def getLinksFromQuery(query):
    await get_links_to_folder(query, output_file)
    return {"status": "Done"}

async def getListLinksFile():
    json_urls_path = "./" +  output_file + "/extracted_urls.json"
    urls = []
    with open(json_urls_path, 'r') as file:
        urls = json.load(file) # conseguimos solo los 5 links mas relevantes
    return urls

#@app.get("/getFilesFromUrlsFile")
async def getFilesFromUrlsFile(urls):
    await scarpeMarkdownBasicInfo(urls,folder_to_save)
    return {"status": "Done"}


#@app.get("/uploadFiles2API")
async def uploadFiles2API(query, links):
    instruccion_sistema = """
            Eres un analista de documentos experimentado.
            Tu tarea es estudiar los documentos proporcionados para informarte.
            Si los documentos no contienen información suficiente para responder, utiliza tu conocimiento general
            del tema para dar una respuesta completa, pero indica al final qué tipo de documentos se necesitan.

            # ¿CÓMO DEBE DE SER LA RESPUESTA?
            ## ESTILO DE LA RESPUESTA
            Tiene que ser lo más natural posible.

            ## COSAS QUE SE PUEDEN QUITAR DE LA SALIDA
            No hace falta que incluyas una breve introducción al usuario
            o un saludo o algo que no añada valor a la respuesta.
            Simplemente quiero que me des la respuesta directa al grano, sin datos superfluos.

            NO MENCIONES EN NINGÚN MOMENTO LOS DOCUMENTOS QUE TE HE PASADO.
            No explique algunos datos, como por
            ejemplo si el usuario te hacer una pregunta: "configurar los mínimos de mi stock".
            En este caso no se te pregunta nada sobre "qué es el stock".
            Otro ejemplo, si el usuario pregunta: "qué es el stock mínimo y cómo lo puedo configurar",
            ahí si que tienes que explicar por que el usu
            ario te lo pregunta.

            ## FORMATO DE LA RESPUESTA
            Quiero que como mínimo la respuesta sea de 512 palabras y como máximo sea de 1024 palabras.

            ### RESUMEN DE LA RESPUESTA
            Quiero que al final hagas un resumen entre 1 y 3 palabras.
            Separame el resumen, entre 1 y 3 palabras del texto principal con el siguiente patrón :"---------------". TIENEN QUE SER 15 - EN TOTAL


            ### LINKS DE CADA DOCUMENTO
            Y quiero que me incluyas los links de los documentos que se ajusten mejor y que has utilizado para responder al usuario.
            Y tiene que seguir el siguiente patrón para separar un :"@@@@@@@@@@@@@@@", TIENEN QUE SER 15 @ EN TOTAL
            TODOS LOS LINKS TIENEN QUE ESTAR SEPARADOS MEDIANTE UNA COMA, SIEMPRE. Por ejemplo: link1, link2, link3
            
            La respuesta final tiene que ser muy parecida a este ejemplo:
            "texto principal
            ---------------
            resumen en 1-3 palabras
            @@@@@@@@@@@@@@@
            link 1, link 2, link 3"
            IMPORTANTE: SIGUE SIEMPRE ÉSTA ESTRUCTURA Y NO HAGAS COSAS DIFERENTES. Ni metas una línea que ponga Resumen: ... ni nada por el estilo,
            SIGUE ESA ESTRUCTURA SIEMPRE.
        """

    list_files = FileManager.get_matrix_documents(folder_to_save)
    # print("List files: ", list_files )

    response= await getResponseUsingFiles(list_files, query, instruccion_sistema, links)
    # if DEBUG_MODE : logger.info(response)
    if DEBUG_MODE : print(response)

    FileManager.deleteAllFiles(folder_to_save)
    
    delegate_get_title_url = lambda url: generate_title_from_url(url)
    response_json = get_json_model_response(response, delegate_get_title_url)
    
    return response_json
    






