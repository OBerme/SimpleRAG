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
         Para darte de alta en la Seguridad Social hay que decidir primero de qué tipo de alta se trata, ya que los procedimientos difieren según sea autónomo, régimen general (MA – alta) o alta por Sistema Red. A continuación te resumo las opciones más habituales y los pasos prácticos para cada una, para que puedas escoger la que corresponde a tu caso.    

1) Alta de un trabajador autónomo (trabajador por cuenta propia)

- Crear la ficha del trabajador: en la ficha nueva, asigna las características necesarias para un autónomo. En el apartado de Cotización deja en blanco los campos correspondientes al Grupo de Tarifa y al Epígrafe de Accidentes, ya que estos autónomos no cotizan al Régimen General.

- Informar un concepto salarial si aplica: si vas a informar la Seguridad Social del autónomo mediante un concepto salarial, en la ruta Tablas/Conceptos/Conceptos Salariales utiliza la opción Previsión IRPF y asigna el código correspondiente para que el sistema tenga en cuenta la previsión de IRPF (por ejemplo, el código 457). Si en tu empresa el concepto se aplica como retribución en especie, en los indicadores del concepto (para el código 457) marca el indicador Cpto. Especies y especifica si es a cargo de la Empresa o del Trabajador. Pulsa Aceptar para guardar.

- Consideraciones finales: este proceso es directo y se centra en adaptar la ficha para que el sistema entienda que no hay cotización al Régimen General y que, si corresponde, se gestione la previsión de IRPF. Si necesitas tratar al autónomo como partícipe de una nómina específica (p. ej., remuneración en especie), puedes usar los indicadores indicados.       

2) Alta de un trabajador en MA – Alta (Régimen General y Agrario)

- Campos obligatorios: en los movimientos de alta informa el código de convenio oficial aplicable al trabajador. Si el convenio de la empresa ya está registrado, se rellenará automáticamente; si no, tendrás que seleccionar un convenio de la lista o introducirlo manualmente. Ten en cuenta que si informas manualmente un convenio que no existe, el sistema puede mostrar el aviso “No existe el convenio en la empresa”, pero el fichero se generará correctamente.

- CNO y contratación: el campo CNO se rellenará automáticamente a partir de la información de CNO (ocupación) en Contratación/Listado contrato de la ficha del trabajador.

- Preparar movimiento MA desde la ficha: al crear la ficha o al modificar la fecha de alta y guardar, la aplicación mostrará un aviso para preparar el movimiento; al pulsar Aceptar, el movimiento quedará en una “bolsa” de acciones preparadas para enviar.

- Nueva Acción de Afiliaciones: ve a Nómina / Comunic@ción / Afiliaciones y selecciona Nueva Acción. Elige al trabajador (o a la empresa), la acción MA – Alta Sucesiva (Régimen General y Agrario), la fecha y el indicador de subrogación si corresponde. Pulsa Aceptar para preparar la acción. Luego, utiliza Sustituir la lista de afiliaciones o Agregar afiliaciones a la lista para seleccionar los trabajadores y generar los ficheros de afiliación.

- Enfoque para altas masivas: si necesitas dar de alta a varios trabajadores a la vez, utiliza el formato Excel para MA – Alta sucesiva (Régimen General y Agrario): Exporta el formato, completa los datos de alta, importa el archivo y genera las altas. Esto facilita la gestión masiva.

- Verificación y envío: recuerda que al entrar en Afiliaciones, por defecto se mostrará la relación de movimientos pendientes; puedes acotar la búsqueda. Una vez lista la selección, genera el alta y, si aplica, genera un fichero AFI para enviar a través de Siltra o del canal que uses en tu empresa. En la ficha del trabajador podrás ver la fecha de envío en Controles (Afiliación Sistema Red Enviado) y, cuando corresponda, podrás proceder a los procesos de envío.

- Consejos prácticos: asegúrate de disponer del código de convenio correcto y de que la fecha de alta esté alineada con la contratación real. Si tu empresa tiene variantes de convenios o subrogaciones, revisa esos campos para evitar inconsistencias en las nóminas y en la Seguridad Social.

3) Alta de un trabajador por Sistema Red (Siltra)

- Opción desde la ficha: en Datos/ Trabajadores/ Mantenimiento Datos, accede a Afiliación Sistema Red. Despliega Acción y selecciona MA – Alta Sucesiva; pulsa Preparar para enviar. La acción quedará acumulada en una bolsa de acciones listas para procesar.

- Opción desde Afiliaciones: ve a Seguridad Social / Afiliaciones y pulsa Nuevo. Selecciona el trabajador (o trabajadores) y la acción MA – Alta Sucesiva, indica la fecha de alta y pulsa Preparar para enviar. Una vez preparadas, selecciona a los trabajadores y pulsa Generar. Se creará un fichero AFI en la ruta RED/VIPTC2/AFI (o la ruta que tenga tu instalación). Este fichero es lo que se envía a la Seguridad Social a través del canal correspondiente.

- Envío y controles: tras generar, accede a Siltra para procesar las remesas de Afiliación. En la ficha del trabajador, en la sección de Controles, verás la fecha de envío de la Afiliación Sistema Red. Una vez enviado, podrás ver el estado “Afiliación Sistema Red Enviado”. Si todo está correcto, el siguiente paso es confirmar en Siltra y cerrar el ciclo de alta.

- Consejos prácticos: es crucial completar el código de convenio en la acción MA; si el centro ya tiene ese código informando, normalmente se rellena automáticamente. Verifica también que la ocupación y el CNO estén correctos en la ficha para que coincidan con las altas y con las nóminas.

Si me dices cuál es el caso concreto (autónomo, Régimen General/Agrario o Sistema Red) y qué herramientas/datos tienes a mano (convenio, fecha de alta, ocupación, código CNO), te guío paso a paso con las acciones exactas que debes ejecutar y te dejo una lista de comprobación adaptada a tu entorno.

---------------
Alta de trabajador...
@@@@@@@@@@@@@@@
https://a3responde.wolterskluwer.com/es/s/article/como-crear-un-trabajador-autonomo, https://a3responde.wolterskluwer.com/es/s/article/afiliaciones-como-generar-el-movimiento-ma-alta-de-los-trabajadores, https://a3responde.wolterskluwer.com/es/s/article/como-hacer-una-afiliacion-de-un-trabajador-por-sistema-red
    """


# Función de enrutamiento que utiliza la lógica combinada
#Pre: list_matrix_files:should be a matrix with the name and the content of the file, like this way:
#           [name_file, content_file]
# query: should be query of the user
# instruccion_sistema: should be the instructions for the AI that it should keep in mind.
#Post: it will return an string with the response of the AI, or an string with the iternal error.
async def getResponseUsingFiles(list_matrix_files, query, instruccion_sistema, links):
    contenido_para_gemini = obtener_contenidos_y_combinar(list_matrix_files)
    
    if contenido_para_gemini.strip():
        # Llamamos a la función asíncrona y la esperamos (await)
        return await evaluar_documentos(contenido_para_gemini, query, instruccion_sistema)
    else:
        print("No se encontró contenido en los archivos para enviar.")
        return "No se proporcionó contenido para evaluar."