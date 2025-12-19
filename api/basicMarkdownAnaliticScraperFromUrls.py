import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai import JsonCssExtractionStrategy

from crawl4ai.content_filter_strategy import PruningContentFilter

from Analitics.finderActualizado import find_end_index_of_word, find_end_index_of_word_reverse

import re
from urllib.parse import urlparse

import json
import time # 👈 Import the time module

debug_mode = False

def url_to_filename(url: str, max_length: int = 150) -> str:
    """
    Convierte una URL potencialmente mal formada en un nombre de archivo seguro y limpio.

    Args:
        url (str): La URL de entrada (ej: https://www.ejemplo.com/pagina?id=123).
        max_length (int): Longitud máxima del nombre de archivo resultante.

    Returns:
        str: Un nombre de archivo limpio y seguro (ej: www_ejemplo_com_pagina_id_123).
    """
    # 1. Parsear la URL para obtener el camino y la consulta
    parsed_url = urlparse(url)
    
    # 2. Combinar el netloc (dominio), el camino y la consulta para una representación completa
    #    Se reemplazan los separadores de ruta y host por guiones bajos
    path_and_query = parsed_url.netloc + parsed_url.path + parsed_url.query
    
    # 3. Eliminar caracteres iniciales/finales indeseados como '/' o '_'
    path_and_query = path_and_query.strip('/').strip('_')

    # 4. Reemplazar caracteres no alfanuméricos ni guiones (excepto puntos) por guiones bajos
    #    Esto elimina :, ?, &, =, #, etc., que son problemáticos en nombres de archivo
    safe_filename = re.sub(r'[^\w\-.]+', '_', path_and_query)
    
    # 5. Reducir guiones bajos múltiples a uno solo para limpieza
    safe_filename = re.sub(r'_{2,}', '_', safe_filename)
    
    # 6. Truncar el nombre del archivo si es demasiado largo
    if len(safe_filename) > max_length:
        # Mantener solo el comienzo
        safe_filename = safe_filename[:max_length].rstrip('_')
        
    # Asegurarse de que no termine en guion bajo si se truncó
    safe_filename = safe_filename.rstrip('_')
    
    return safe_filename


def getDefaultMarkdownConfig():
    md_generator = DefaultMarkdownGenerator(
        options={
            "ignore_links": True,
            "escape_html": False,
            "body_width": 80
        }
    )
    # schema = {
    #     "name": "Crypto Holder via XPath",
    #     "baseSelector": "lightning-formatted-rich-text",
    #     "fields": [
    #         {
    #             "name": "dataExtracted",
    #             "selector": "[lwc-4nfn2rc40ch]",
    #             "type": "html"
    #         }
    #     ]
    # }
    
    schema = {
        "name": "Crypto Holder via XPath",
        "baseSelector": "article",
        "fields": [
            {
                "name": "dataExtracted",
                "selector": "css:.Ag2a3INNUVA",
                "type": "html"
            }
        ]
    }
    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)
    
        
    config = CrawlerRunConfig(
        markdown_generator=md_generator,
        cache_mode = CacheMode.BYPASS,
        extraction_strategy=extraction_strategy,
        wait_for="css:.slds-rich-text-editor__output"
    )
    
    return config



def getPruneMarkdownConfig():
    prune_filter = PruningContentFilter(
        threshold=0.5,
        threshold_type="fixed",  # or "dynamic"
        min_word_threshold=50
    )
    md_generator = DefaultMarkdownGenerator(
        content_source="fit_html",
        content_filter=prune_filter,
        options={
            "ignore_links": True,
            "escape_html": False,
            "body_width": 80,
            "skip_internal_links": False
        }
    )
    schema = {
        "name": "Crypto Holder via XPath",
        # "baseSelector": "lightning-formatted-rich-text",
        "baseSelector": "span[lwc-4nfn2rc40ch]",
        "fields": [
            {
                "name": "dataExtracted",
                # "selector": "[lwc-4nfn2rc40ch]",
                "selector": "div.Ag2a3INNUVA",
                "type": "html"
            }
        ]
    }
    
    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)
    
        
    config = CrawlerRunConfig(
        markdown_generator=md_generator,
        
        cache_mode = CacheMode.BYPASS,
        extraction_strategy=extraction_strategy,
        wait_for="css:.slds-rich-text-editor__output"
    )
    
    return config


median_init = 220
median_final = 2761
desves_init = 83
desves_final = 113

median_init_min = median_init - desves_init
median_init_max = median_init + desves_init

median_final_min = median_final - desves_final
median_final_max = median_final + desves_final




def getIndexOfInit(array_content):
    keyWord = "ACTUALIZADO"
    content = str(array_content[median_init_min:median_init_max])
    try:
        index = find_end_index_of_word(content, keyWord) + median_init_min
        return index + 20 
    except:
        # print("Contenido: ", content)
        print("Error al conseguir el index inicial")
        return 0
    
    return finalIndex

#To be done with R studio
def getIndexOfFinal(array_content):
    keyWord = "LikeDislike"
    array_content_length = len(array_content)
    extraWords = 43
    if array_content_length >= median_final_min:
        content = str(array_content[median_final_min:median_final_max])
        try:
            finalIndex = len(array_content) - find_end_index_of_word_reverse(content, keyWord)  + median_final_min - extraWords
            return finalIndex
        except:
            # print("Contenido: ", content)
            print("Error al conseguir el index final")
            print("Probando una solucion definitiva")
            index = find_end_index_of_word(str(array_content), keyWord) 
            finalIndex = array_content_length - index + extraWords
            return finalIndex
    else:
        print("Probando una solucion definitiva")
        index = find_end_index_of_word(str(array_content), keyWord) 
        finalIndex = array_content_length - index + extraWords
        return finalIndex
    
    

async def scarpeMarkdownBasicInfo(urls, outputFolderRelativePath):
    config = getPruneMarkdownConfig()

    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun_many(urls, config=config)
        
        for res in results:
            try:
                
                file_name = url_to_filename(res.url)
                document_name = outputFolderRelativePath  + "/" + file_name + ".md"
                
                data_to_save = res.markdown
                longitud_inicial = len(data_to_save)
                if debug_mode: print("Longitud: ", longitud_inicial) 
                initIndex = getIndexOfInit(data_to_save)
                finalIndex = getIndexOfFinal(data_to_save) 
                
                try:
                    if debug_mode: print("Initial index: ", initIndex)
                    data_to_save = data_to_save[initIndex:-finalIndex]
                    # data_to_save = data_to_save[:]
                    if debug_mode:  print("Longitud final: ", len(data_to_save)) 
                    with open(document_name, 'w', encoding='utf-8') as file:
                        file.write(data_to_save)
                except:
                    with open("./errors.log", 'w', encoding='utf-8') as file:
                        file.write("Error consiguiendo la longitud final: " + file_name + ", longitud inicial: " + longitud_inicial + " ,index inicial: " + initIndex + " ,index final: " + finalIndex)
                    continue
                
            except:
                continue
            