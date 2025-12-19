from fastapi import FastAPI

from fileManager import FileManager
# from GoogleGemini.googleGeminiFilesUploaderFinal import getResponseUsingFiles, evaluar_documentos, obtener_contenidos_y_combinar
from OpenAIChatGPT.APIInterfaceCallable import getResponseUsingFiles, evaluar_documentos, obtener_contenidos_y_combinar
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
    await getFilesFromUrlsFile()
    response = await uploadFiles2API(query)
    return {"response":response}

#@app.get("/getLinksFromQuery")
async def getLinksFromQuery(query):
    await get_links_to_folder(query, output_file)
    return {"status": "Done"}

#@app.get("/getFilesFromUrlsFile")
async def getFilesFromUrlsFile():
    json_urls_path = "./" +  output_file + "/extracted_urls.json"
    with open(json_urls_path, 'r') as file:
        urls = json.load(file)[:5] # conseguimos solo los 5 links mas relevantes
        await scarpeMarkdownBasicInfo(urls,folder_to_save)
    return {"status": "Done"}


#@app.get("/uploadFiles2API")
async def uploadFiles2API(query):
    instruccion_sistema = """
            Eres un analista de documentos experimentado.
            Tu tarea es estudiar los documentos proporcionados para informarte.
            Si los documentos no contienen información suficiente para responder, utiliza tu conocimiento general
            del tema para dar una respuesta completa, pero indica al final qué tipo de documentos se necesitan.
            
            #¿CÓMO DEBE DE SER LA RESPUESTA?
            ##ESTILO DE LA RESPUESTA
            Tiene que ser lo más natural posible.
            
            ##COSAS QUE SE PUEDEN QUITAR DE LA SALIDA
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
            
            ##FORMATO DE LA RESPUESTA
            Quiero que como mínimo la respuesta sea de 512 palabras y como máximo sea de 1024 palabras.
        """
        
            
        #Quiero que menciones de que documentos has sacado la información. De los documentos que te he pasado.
        
    # files = FileManager.recopilar_nombres_markdown(folder_to_save)
    # list_files = [ folder_to_save + '/' + next_file_name for next_file_name in files]
    
    # list_files = list_files[:3]
    list_files = FileManager.get_matrix_documents(folder_to_save)
    print("List files: ", list_files )

    response = await getResponseUsingFiles(list_files, query, instruccion_sistema)
    FileManager.deleteAllFiles(folder_to_save)
    # return {"response": response}
    return {response}





