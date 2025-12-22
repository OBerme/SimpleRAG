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
    return """
    Para dar de alta un trabajador en la Seguridad Social, tienes tres maneras posibles y cada una requiere un conjunto de datos y pasos. Elige la que mejor se ajuste a tu caso (alta individual o masiva).

        1) Alta individual desde la ficha del trabajador (Sistema Red)
        - Abre la ficha del trabajador y accede a la opción para enviarla a la Seguridad Social:
        - Ir a la ruta correspondiente y selecciona la acción MA – Alta Sucesiva.
        - Pulsa Preparar para enviar y, si procede, modifica la fecha de alta y otros datos que aparezcan.
        - Confirma con Aceptar. En ese momento la acción queda preparada y se acumula para tramitarla desde la sección de Afiliaciones.
        - Después ve a Nómina/Comunic@ción/Afiliaciones y usa Nueva Acción (si fuera necesario) para completar el alta.
        - En la ventana selecciona el trabajador o la empresa, la acción “MA – Alta Sucesiva (Régimen General y Agrario)” y la fecha del alta. Si corresponde, indica un indicativo de subrogación.
        - Pulsa Aceptar. Verás que la acción queda en la lista de acciones preparadas.
        - Selecciona los trabajadores a los que quieres dar de alta y pulsa Generar para crear el fichero de alta (AFI) y/o enviarlo.
        - Pasos finales y control:
        - En la lista de acciones, utiliza la opción Generar para producir el fichero AFI. En este punto, podrás enviar la remesa o procesarla en el sistema correspondiente (Siltra) si aplica.
        - En la ficha del trabajador, en Controles, podrás ver la fecha en que se generó la acción y, una vez enviada, la fecha de envío en el campo correspondiente.
        - Datos clave que suelen requerirse:
        - Código de convenio de la empresa (debería estar disponible; si no, puedes seleccionar un convenio de la lista de convenios de la empresa).
        - CNO (ocupación): se llena automáticamente desde la información de contratación/listado de contrato de la ficha; si no, deberá informarse manualmente.
        - Fecha del alta y fecha de efectos, y cualquier otro dato que la plataforma pida (centro, centro de coste, jornada, etc., según configuración).
        - Observaciones útiles:
        - Si no existe el convenio en la empresa, al seleccionar un código manual podría aparecer un mensaje, pero el fichero se generará de todos modos.
        - Si vas a hacer altas de varios trabajadores, puedes usar la vía de Excel para agilizar el proceso (ver apartado masivo).

        2) Alta mediante Afiliaciones – Nueva Acción
        - Ve a Nómina/Comunic@ción/Afiliaciones y elige Nueva Acción.
        - Selecciona el trabajador o la empresa y la acción MA – Alta Sucesiva (Régimen General y Agrario); indica la fecha del alta y, si aplica, el indicativo de subrogación.
        - Pulsa Aceptar para preparar la acción.
        - En la siguiente pantalla, elige Sustituir la lista de afiliaciones o Agregar afiliaciones a la lista para incluir a los trabajadores deseados.
        - Recuerda que, al entrar en la pantalla de afiliaciones, verás una lista de movimientos pendientes de generar de todas las empresas del mes en curso y del mes anterior; si necesitas, acota la búsqueda.
        - Cuando tengas la lista deseada, selecciona a los trabajadores y pulsa Generar. Se creará el fichero AFI del movimiento MA.
        - Opcional: desde el área de Afiliaciones también podrás Exportar/Importar para gestionar masivamente y luego generar la remesa para enviar.
        - Datos clave:
        - Código de convenio debe estar informado (si el convenio ya está asignado al trabajador, se mostrará automáticamente; si no, puedes elegir uno de la empresa).
        - CNO se rellenará en función de la ocupación indicada en la ficha.
        - Beneficio de esta vía: facilita el alta de varios trabajadores en un único proceso, manteniendo un control claro de qué acciones están preparadas y pendientes de enviar.

        3) Alta masiva vía formato Excel (Format 202 – MA – Alta sucesiva)
        - En Nómina/Comunic@ción/Afiliaciones, usa Importar/Exportar y elige Exportar el formato 202 – MA – Alta sucesiva (Régimen General y Agrario).
        - Completa el Excel con los datos requeridos: empresa/centro/trabajadores, fecha de alta, jornada, y otros campos obligatorios indicados; recuerda que, si el trabajador tiene una jornada parcial o reducida, debes completar los campos correspondientes.
        - Guarda el Excel y usa Importar para cargarlo en el sistema.
        - Selecciona los trabajadores importados y pulsa Generar para crear el fichero AFI correspondiente.
        - Si todo está correcto, la generación te confirmará que el alta está listo para enviar. Posteriormente podrás enviar la remesa a la Seguridad Social (a través del flujo habitual de Siltra si corresponde).
        - Datos clave:
        - Debes indicar el código de convenio para cada trabajador; si ya existe en la empresa, se rellenará automáticamente; si no, tendrás que asignarlo manualmente.
        - El campo CNO (ocupación) se toma de la ficha; si hay discrepancias, asegúrate de ajustar la ocupación en el listado de contrato.      
        - Ventajas:
        - Ideal cuando se da de alta a varios trabajadores en poco tiempo, manteniendo consistencia entre datos y movimientos.
        - Consideraciones finales:
        - Tras generar, en la ficha de cada trabajador podrás ver la fecha en que se generó la acción (Afiliación System Red Enviado) y en el área de Controles de la ficha, la trazabilidad del alta.
        - En todos los casos, el ficheros AFI se crean en la ruta correspondiente del sistema y luego puedes procesarlos o enviarlos según tu flujo de trabajo.

        Qué necesitas para empezar (resumen)
        - Datos del trabajador o de los trabajadores: nombre, fecha de alta, centro de trabajo, código de convenio, ocupación (CNO) y, si se aplica, la jornada.
        - Acceso a las rutas de nómina y afiliaciones (con permisos para crear acciones MA – Alta Sucesiva).
        - Conocimientos sobre si es un alta individual o masiva (para seleccionar la vía adecuada: ficha, acción nueva o Excel).
        - Si trabajas con Sistema Red, confirma que la empresa está configurada para MA – Alta Sucesiva y que puedes generar el fichero AFI y enviarlo.

        Si necesitas, puedo adaptar estos pasos a tu versión exacta del sistema o aclararte cuál es la ruta exacta en tu interfaz. En ese caso, dime si es una alta individual o masiva y si trabajas con Sistema Red o con otro régimen, y te doy una guía más precisa paso a paso.
        
        ---------------
        Alta trabajadores
    """


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