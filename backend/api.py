from fastapi import FastAPI

from fileManager import FileManager
# from GoogleGemini.googleGeminiFilesUploaderFinal import getResponseUsingFiles, evaluar_documentos, obtener_contenidos_y_combinar
# from OpenAIChatGPT.APIInterfaceCallable import getResponseUsingFiles, evaluar_documentos, obtener_contenidos_y_combinar
from OpenAIChatGPT.APIInterfaceCallableMockApp import getResponseUsingFiles, evaluar_documentos, obtener_contenidos_y_combinar
# # from OpenAIChatGPT.APIInterfaceCallableFilesVersion import getResponseUsingFiles

from basicMarkdownAnaliticScraperFromUrls import scarpeMarkdownBasicInfo 

from scraper import get_links_to_folder
import re
import json

from fastapi.middleware.cors import CORSMiddleware

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
    await getLinksFromQuery(query)
    links = await getListLinksFile()
    links = links[:3]
    
    print("Links: ", links)
    
    await getFilesFromUrlsFile(links)
    response = await uploadFiles2API(query, links)
    return {"response":response}

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
            Separame el resumen, entre 1 y 3 palabras del texto principal con el siguiente patrón :"---------------"
            
            
            ### LINKS DE CADA DOCUMENTO
            Y quiero que me incluyas los links de los documentos que se ajusten mejor y que has utilizado para responder al usuario.
            
            La respuesta final tiene que ser muy parecida a este ejemplo:
            texto principal...
            ---------------
            resumen en 1-3 palabras...
            @@@@@@@@@@@@@@@
            link 1, link 2, link 3
        """
        
            
        #Quiero que menciones de que documentos has sacado la información. De los documentos que te he pasado.
        
    # files = FileManager.recopilar_nombres_markdown(folder_to_save)
    # list_files = [ folder_to_save + '/' + next_file_name for next_file_name in files]
    
    # list_files = list_files[:3]
    list_files = FileManager.get_matrix_documents(folder_to_save)
    print("List files: ", list_files )

    response = await getResponseUsingFiles(list_files, query, instruccion_sistema, links)
    FileManager.deleteAllFiles(folder_to_save)
    # return {"response": response}
    return {response}



@app.get("/getSumUpText")
async def getResponseWithQuery(text):
    instruccion_sistema = """
        Eres una persona que resume textos diariamente y sabes como resumir un texto en 1 y 3 palabras.
        Tu tarea es resumir el texto que te voy a proporcionar.
    """ + text
            
        #Quiero que menciones de que documentos has sacado la información. De los documentos que te he pasado.
        
    # list_files = list_files[:3]
    list_files = FileManager.get_matrix_documents(folder_to_save)
    print("List files: ", list_files )

    response = await getResponseUsingFiles(list_files, query, instruccion_sistema)
    FileManager.deleteAllFiles(folder_to_save)
    # return {"response": response}
    return {response}





