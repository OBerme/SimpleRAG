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
#     return """
#          Para darte de alta en la Seguridad Social hay que decidir primero de qué tipo de alta se trata, ya que los procedimientos difieren según sea autónomo, régimen general (MA – alta) o alta por Sistema Red. A continuación te resumo las opciones más habituales y los pasos prácticos para cada una, para que puedas escoger la que corresponde a tu caso.    

# 1) Alta de un trabajador autónomo (trabajador por cuenta propia)

# - Crear la ficha del trabajador: en la ficha nueva, asigna las características necesarias para un autónomo. En el apartado de Cotización deja en blanco los campos correspondientes al Grupo de Tarifa y al Epígrafe de Accidentes, ya que estos autónomos no cotizan al Régimen General.

# - Informar un concepto salarial si aplica: si vas a informar la Seguridad Social del autónomo mediante un concepto salarial, en la ruta Tablas/Conceptos/Conceptos Salariales utiliza la opción Previsión IRPF y asigna el código correspondiente para que el sistema tenga en cuenta la previsión de IRPF (por ejemplo, el código 457). Si en tu empresa el concepto se aplica como retribución en especie, en los indicadores del concepto (para el código 457) marca el indicador Cpto. Especies y especifica si es a cargo de la Empresa o del Trabajador. Pulsa Aceptar para guardar.

# - Consideraciones finales: este proceso es directo y se centra en adaptar la ficha para que el sistema entienda que no hay cotización al Régimen General y que, si corresponde, se gestione la previsión de IRPF. Si necesitas tratar al autónomo como partícipe de una nómina específica (p. ej., remuneración en especie), puedes usar los indicadores indicados.       

# 2) Alta de un trabajador en MA – Alta (Régimen General y Agrario)

# - Campos obligatorios: en los movimientos de alta informa el código de convenio oficial aplicable al trabajador. Si el convenio de la empresa ya está registrado, se rellenará automáticamente; si no, tendrás que seleccionar un convenio de la lista o introducirlo manualmente. Ten en cuenta que si informas manualmente un convenio que no existe, el sistema puede mostrar el aviso “No existe el convenio en la empresa”, pero el fichero se generará correctamente.

# - CNO y contratación: el campo CNO se rellenará automáticamente a partir de la información de CNO (ocupación) en Contratación/Listado contrato de la ficha del trabajador.

# - Preparar movimiento MA desde la ficha: al crear la ficha o al modificar la fecha de alta y guardar, la aplicación mostrará un aviso para preparar el movimiento; al pulsar Aceptar, el movimiento quedará en una “bolsa” de acciones preparadas para enviar.

# - Nueva Acción de Afiliaciones: ve a Nómina / Comunic@ción / Afiliaciones y selecciona Nueva Acción. Elige al trabajador (o a la empresa), la acción MA – Alta Sucesiva (Régimen General y Agrario), la fecha y el indicador de subrogación si corresponde. Pulsa Aceptar para preparar la acción. Luego, utiliza Sustituir la lista de afiliaciones o Agregar afiliaciones a la lista para seleccionar los trabajadores y generar los ficheros de afiliación.

# - Enfoque para altas masivas: si necesitas dar de alta a varios trabajadores a la vez, utiliza el formato Excel para MA – Alta sucesiva (Régimen General y Agrario): Exporta el formato, completa los datos de alta, importa el archivo y genera las altas. Esto facilita la gestión masiva.

# - Verificación y envío: recuerda que al entrar en Afiliaciones, por defecto se mostrará la relación de movimientos pendientes; puedes acotar la búsqueda. Una vez lista la selección, genera el alta y, si aplica, genera un fichero AFI para enviar a través de Siltra o del canal que uses en tu empresa. En la ficha del trabajador podrás ver la fecha de envío en Controles (Afiliación Sistema Red Enviado) y, cuando corresponda, podrás proceder a los procesos de envío.

# - Consejos prácticos: asegúrate de disponer del código de convenio correcto y de que la fecha de alta esté alineada con la contratación real. Si tu empresa tiene variantes de convenios o subrogaciones, revisa esos campos para evitar inconsistencias en las nóminas y en la Seguridad Social.

# 3) Alta de un trabajador por Sistema Red (Siltra)

# - Opción desde la ficha: en Datos/ Trabajadores/ Mantenimiento Datos, accede a Afiliación Sistema Red. Despliega Acción y selecciona MA – Alta Sucesiva; pulsa Preparar para enviar. La acción quedará acumulada en una bolsa de acciones listas para procesar.

# - Opción desde Afiliaciones: ve a Seguridad Social / Afiliaciones y pulsa Nuevo. Selecciona el trabajador (o trabajadores) y la acción MA – Alta Sucesiva, indica la fecha de alta y pulsa Preparar para enviar. Una vez preparadas, selecciona a los trabajadores y pulsa Generar. Se creará un fichero AFI en la ruta RED/VIPTC2/AFI (o la ruta que tenga tu instalación). Este fichero es lo que se envía a la Seguridad Social a través del canal correspondiente.

# - Envío y controles: tras generar, accede a Siltra para procesar las remesas de Afiliación. En la ficha del trabajador, en la sección de Controles, verás la fecha de envío de la Afiliación Sistema Red. Una vez enviado, podrás ver el estado “Afiliación Sistema Red Enviado”. Si todo está correcto, el siguiente paso es confirmar en Siltra y cerrar el ciclo de alta.

# - Consejos prácticos: es crucial completar el código de convenio en la acción MA; si el centro ya tiene ese código informando, normalmente se rellena automáticamente. Verifica también que la ocupación y el CNO estén correctos en la ficha para que coincidan con las altas y con las nóminas.

# Si me dices cuál es el caso concreto (autónomo, Régimen General/Agrario o Sistema Red) y qué herramientas/datos tienes a mano (convenio, fecha de alta, ocupación, código CNO), te guío paso a paso con las acciones exactas que debes ejecutar y te dejo una lista de comprobación adaptada a tu entorno.

# ---------------
# Alta de trabajador...
# @@@@@@@@@@@@@@@
# https://a3responde.wolterskluwer.com/es/s/article/como-crear-un-trabajador-autonomo, https://a3responde.wolterskluwer.com/es/s/article/afiliaciones-como-generar-el-movimiento-ma-alta-de-los-trabajadores, https://a3responde.wolterskluwer.com/es/s/article/como-hacer-una-afiliacion-de-un-trabajador-por-sistema-red
#     """

    return """
    No existe una opción explícita de “mínimos de stock” o “punto de pedido” descrita en las herramientas evaluadas. Con lo que se especifica en las funciones de stock, puedes gestionar y monitorizar niveles de inventario, pero no aparece un campo directo para fijar un mínimo por artículo ni una alerta automática de reposición. Aun así, puedes aplicar un enfoque práctico utilizando las funciones disponibles para mantener controlados tus niveles y planificar la reposición de forma semi-automatizada o manual.

    Qué puedes hacer con las opciones y la gestión de stock

    - Configuración general de stock: puedes definir si los nuevos productos afectan al stock, elegir la valoración por defecto (por ejemplo, último precio de compra, precio de compra, precio de venta) y permitir stocks negativos. Estas configuraciones influyen en cómo se gestiona y registra el stock, pero no establecen una cantidad mínima por artículo. Sirven para dejar claro el comportamiento del sistema frente a entradas de inventario y a la valoración, lo que a su vez facilita la planificación y el análisis de costos cuando determines tus mínimos.

    - Ficha de artículo y stock: en la ficha de cada artículo se indica si el artículo afecta al stock y muestra el stock actual, así como las reservas de pedidos de compra y de venta y la previsión. También se registra la valoración y se observa el estado de stock. Con estas informaciones puedes decidir, artículo por artículo, qué nivel de stock consideras mínimo para no interrumpir ventas o producción. En la práctica, deberás fijar un umbral mínimo fuera del sistema (en tu propio registro o en un plan de compras) y revisarlo con regularidad utilizando la visión general del stock y la previsión.

    - Gestión de inventarios: puedes calcular inventario, exportarlo e importarlo a Excel. Esta funcionalidad es útil para realizar revisiones periódicas y verificar caídas de stock frente a tus umbrales mínimos. Si quieres monitorizar de forma estructurada, puedes hacer un recuento de inventario y, a partir de los datos exportados, identificar cuáles artículos están por debajo de tus niveles mínimos y planificar compras o ajustes.

    - Gestión de stock y consultas: la opción de consultar stock te permite ver el stock de todos los artículos y exportarlo a Excel. También puedes ver movimientos de stock filtrando por artículo y por rango de fechas. Estas vistas son clave para detectar cuando un artículo baja de tu mínimo deseado y para entender la dinámica de entradas y salidas (ventas, compras, mermas, devoluciones) que afectan a tus umbrales.

    - Regularizaciones: si hay discrepancias entre el stock físico y el registrado, la regularización te permite corregir esas diferencias. Mantener el inventario exacto es fundamental para que los mínimos que definas sean fiables y para evitar reposiciones innecesarias o faltantes por errores en el conteo.

    Cómo establecer un flujo práctico para mínimos (sin una opción automática en el sistema)

    - Define un mínimo por artículo fuera del sistema: para cada artículo, decide una cantidad mínima a mantener basada en consumo histórico, plazos de reposición y tolerancia de seguridad. Este mínimo se puede anotar en un registro externo o en una columna adicional dentro de tu propio sistema de control de inventarios si el ERP lo permite.

    - Monitorea stock actual y previsto: usa la visión de stock para revisar el stock real y el “previsto” para cada artículo. Si el stock actual está por debajo de tu mínimo, planifica la reposición. Usa la exportación de stock para generar listas de pedido o para preparar importaciones de actualización de inventario con cantidades de compra necesarias.

    - Revisa movimientos y demanda: con Movimiento de stock y con las exportaciones de stock, analiza tendencias de venta y uso. Si observas caídas continuas o picos de demanda, ajusta tu mínimo o el plan de reaprovisionamiento en consecuencia para evitar faltantes.

    - Plan de compras basado en mínimos: si tu entorno lo permite, complementa la revisión de stock con un procedimiento de compras donde, cada vez que exportas y comparas stock con mínimos, generas un pedido de compra para aquellos artículos por debajo del umbral. Si no hay reglas automáticas, este paso puede hacerse manualmente pero con un proceso definido para no perder reposiciones.

    Qué documentos o guías conviene consultar para afinar el proceso

    - Busca una guía específica del módulo de inventario que describa “niveles mínimos”, “punto de pedido” o “alertas de reposición” si tu versión de A3factura los soporta. Es posible que exista un campo adicional o una configuración avanzada no cubierta por las secciones evaluadas.

    - Revisa manuales de usuario o guías de flujo de compras e inventario que expliquen cómo activar alertas, si existen, o cómo integrar mínimos con órdenes de compra automáticas.     

    - Si en tu entorno hay personalización o integraciones, considera la posibilidad de añadir una regla externa o un informe programado que compare stock actual con mínimos definidos y notifique a compras cuando se cruza el umbral.

    En resumen, no hay una configuración directa de “mínimos de stock” en las funciones descritas. Sin embargo, puedes establecer mínimos de forma manual para cada artículo y apoyarte en la consulta de stock, la gestión de inventarios y las exportaciones para monitorizar y activar reposiciones. Mantén el inventario cuidado con regularizaciones para asegurar que los mínimos sean válidos y confiables. Si necesitas una solución automática, conviene buscar en la documentación específica del módulo o consultar con soporte para ver si existe una funcionalidad de puntos de pedido o alertas que se pueda activar en tu versión.---------------Niveles mínimos@@@@@@@@@@@@@@@https://a3responde.wolterskluwer.com/es/s/article/funcionamiento-stock-en-a3factura-a3factura
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