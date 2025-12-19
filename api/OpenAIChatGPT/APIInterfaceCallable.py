import os
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPEN_AI_KEY = os.getenv('OPEN_AI_KEY')
OPEN_AI_MODEL = os.getenv('OPEN_AI_MODEL')
client = OpenAI(api_key=OPEN_AI_KEY)

# Configuración del modelo de OpenAI
# Puedes elegir un modelo rápido y eficiente como GPT-3.5 o un modelo más potente como GPT-4
DEBUG_MODE=True
# O puedes usar: 'gpt-4o' (Omni) o 'gpt-4-turbo'

# La clave API se cargará automáticamente de la variable de entorno OPENAI_API_KEY
# (Asegúrate de configurar esta variable en tu .env o Docker Compose)

def obtener_contenidos_y_combinar(lista_archivos_contenidos_matrix):
    """
    Combina el contenido de los archivos en un solo string, limitando a los primeros 5.
    (La lógica es idéntica a la versión de Gemini).
    """
    
    # max_list_matrix_files = 
    contenido_total = ""
    for next_contenido_fichero in lista_archivos_contenidos_matrix:
        nombre_archivo = next_contenido_fichero[0]
        try:
            # Encapsulamos cada documento para que el modelo sepa dónde empieza y termina
            contenido_total += f"--- INICIO DOCUMENTO: {nombre_archivo} ---\n"
            contenido_total += next_contenido_fichero[1] + "\n"
            contenido_total += f"--- FIN DOCUMENTO: {nombre_archivo} ---\n\n"
        except Exception:
            # En este contexto, si el contenido ya está en la matriz, esto rara vez se usa
            print(f"Advertencia: Error al procesar el contenido de: {nombre_archivo}")
    return contenido_total

async def evaluar_documentos(contenido_combinado: str, query: str, instruccion_sistema: str):
    """
    Llama a la API de OpenAI para evaluar los documentos y generar la respuesta.
    """
    try:

        # 1. Definir la Instrucción del Sistema (System Instruction)
        # Hemos refinado ligeramente tu prompt para que sea más claro y directo para GPT.
        print("Instrucciones: ", instruccion_sistema)

        # 2. Definir el Prompt del Usuario (User Prompt)
        prompt_usuario = (
            f"Pregunta del usuario:\n\n{query}\n\n"
            f"DOCUMENTOS A EVALUAR:\n\n{contenido_combinado}"
        )
        
        
        messages_list = [
            # Mensaje 1: El Rol de Sistema (Tus instrucciones de comportamiento)
            {"role": "system", "content": instruccion_sistema},
            
            # Mensaje 2: La Consulta del Usuario (Tus datos a procesar)
            {"role": "user", "content": prompt_usuario}
        ]
        
        if DEBUG_MODE: print("Prompt usuario: ", prompt_usuario)
        
        print(f"Enviando solicitud al modelo {OPEN_AI_MODEL}...")
        # print("Input messages: ", messages_list)
        # 3. Llamada al endpoint de chat completions (es asíncrona)
        response = client.responses.create(
            model=OPEN_AI_MODEL,
            # input=[
            #     {"role": "system", "content": instruccion_sistema},
            #     {"role": "user", "content": prompt_usuario}
            # ,]
            input=messages_list
            # temperature=0.0
            # input=prompt_usuario
        )
        

        # # 4. Extraer el Contenido
        # # La respuesta de OpenAI es diferente; el texto está en response.choices[0].message.content
        contenido = response.output_text
        
        if DEBUG_MODE: print("Contenido: ", contenido)
        # print("\n--- ✅ RESPUESTA DEL MODELO (OpenAI) ---")
        # print(contenido)
        # print("---------------------------------------")
        
        return contenido
        

    # except APIError as e:
    #     print(f"Ocurrió un error en la API de OpenAI: {e}")
    #     return f"Error al procesar la solicitud: {e.message}"
    except Exception as e:
        print(f"Ocurrió un error general: {e}")
        return "Error desconocido durante la llamada a OpenAI."


# Función de enrutamiento que utiliza la lógica combinada
#Pre: list_matrix_files:should be a matrix with the name and the content of the file, like this way:
#           [name_file, content_file]
# query: should be query of the user
# instruccion_sistema: should be the instructions for the AI that it should keep in mind.
#Post: it will return an string with the response of the AI, or an string with the iternal error.
async def getResponseUsingFiles(list_matrix_files, query, instruccion_sistema):
    contenido_para_gemini = obtener_contenidos_y_combinar(list_matrix_files)
    
    if contenido_para_gemini.strip():
        # Llamamos a la función asíncrona y la esperamos (await)
        return await evaluar_documentos(contenido_para_gemini, query, instruccion_sistema)
    else:
        print("No se encontró contenido en los archivos para enviar.")
        return "No se proporcionó contenido para evaluar."