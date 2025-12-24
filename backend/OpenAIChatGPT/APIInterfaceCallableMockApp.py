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
    Para configurar los mínimos de stock de forma efectiva conviene distinguir entre dos conceptos clave: el stock mínimo y el punto de pedido (ROP, por sus siglas en inglés). El stock mínimo es la reserva mínima que quieres mantener en almacén para hacer frente a variaciones de demanda o imprevistos sin quedarte sin inventorios, mientras que el punto de pedido es la cantidad de existencias que, al alcanzarse, activa una reposición para evitar quedarse sin stock antes de recibir el pedido. En la práctica, se suelen vincular ambos conceptos a una política de reabastecimiento que persiga un nivel de servicio deseado y unas condiciones de coste razonables.

    Pasos prácticos para configurarlos

    1) Define el objetivo de servicio por artículo
    No todos los productos requieren el mismo nivel de servicio. Clasifica tu catálogo (por ejemplo, A, B y C) y asigna objetivos de servicio distintos. Los artículos de mayor valor o con mayor rotación—los de clase A—tienden a requerir niveles de servicio superiores y, por tanto, mayores stock mínimos y puntos de pedido más conservadores.

    2) Reúne y limpia los datos
    Necesitas datos históricos de demanda por artículo (diaria o semanal), el plazo de entrega del proveedor (lead time) y la variabilidad de la demanda. También importa conocer las fechas de entrega reales, la fiabilidad de tus proveedores y, si aplica, estacionalidad. Registra también el stock actual, costes de pedido y costes de mantenimiento de inventario.

    3) Calcula la demanda durante el lead time
    Demanda durante el lead time (DLT) = demanda diaria promedio x lead time (en días). Si tu lead time es en días hábiles, úsalo así; si es en días naturales, ajusta el cálculo. 

    4) Evalúa la variabilidad y calcula el stock de seguridad
    - Desviación típica de la demanda diaria (σD) durante el periodo considerado.
    - Lead time en días (L).
    - σDL = σD x sqrt(L) (demanda durante el lead time).
    - Elige un nivel de servicio deseado (por ejemplo, 95% o 99%). El valor z correspondiente se obtiene de la tabla normal (aproximadamente 1.65 para 95%, 2.33 para 99%).        
    - Stock de seguridad (SS) = z x σDL.

    5) Determina el punto de pedido (ROP)
    - Demanda durante el lead time (DLT) = promedio diario x lead time.
    - ROP = DLT + SS.
    Cuando el inventario disponible alcance el ROP, ejecuta la reposición para volver a alcanzar un nivel de stock seguro.

    6) Define el stock mínimo
    - Opción conservadora: igual al SS (mantenes una reserva puramente de seguridad).
    - Opción operativa: establece un mínimo que cubra parte de la demanda durante un periodo de revisión adicional (por ejemplo, 1–2 semanas) para compensar posibles retrasos o variaciones.
    - Si tu revisión de inventario es periódica, puede ser razonable fijar el stock mínimo como SS más una cobertura adicional para el periodo entre revisiones.

    7) Configuración en el sistema
    - Campo de stock mínimo: fija el mínimo deseado por artículo.
    - Punto de pedido: introduce el valor ROP calculado.
    - Cantidad a pedir: define la cantidad de pedido (EOQ o una cantidad acordada con proveedores) que repondrá desde el nivel actual hasta el máximo deseado.
    - Máximo de stock: establece un tope para evitar sobreacumulación.
    - Política de revisión: selecciona si es una revisión continua (ERP dispara pedido al alcanzar ROP) o si es una revisión periódica (revisa a intervalos fijos y reordena para regresar al nivel máximo).

    8) Mecanismos de revisión y ajuste
    - Monitoriza regularmente (semanal o quincenal) los artículos con mayor rotación y mayor variabilidad.
    - Ajusta SS y ROP ante cambios en lead times, confiabilidad de proveedores o cambios de demanda estacional.
    - Si trabajas con productos perecibles o con caducidad, añade consideraciones de obsolescencia y rotación en tus cálculos.

    9) Ejemplos operativos
    Ejemplo simplificado: artículo X
    - Demanda diaria promedio: 25 unidades
    - Lead time: 10 días
    - σD: 8 unidades
    - Nivel de servicio: 95% (z ≈ 1.65)
    - σDL = σD x sqrt(L) ≈ 8 x sqrt(10) ≈ 25.3
    - SS ≈ 1.65 x 25.3 ≈ 41–42 unidades
    - DLT ≈ 25 x 10 = 250 unidades
    - ROP ≈ 250 + 42 ≈ 292 unidades
    - Stock mínimo recomendado: 292–300 unidades (dependiendo de si quieres incluir una cobertura adicional)
    - Cantidad a pedir: si tu política es EOQ, calcula la cantidad óptima y ajústala para no superar el stock máximo.

    10) Seguimiento y mejora continua
    - Revisa métricas como tasas de stockouts, rotación de inventario y coste total de inventario.
    - Ajusta SS y ROP cuando cambien las condiciones de suministro o la demanda.
    - Implementa alertas automáticas para cuando el inventario caiga por debajo del stock mínimo o esté por debajo del ROP.

    Qué documentos serían útiles para afinar la configuración
    - Datos de demanda histórica por artículo (últimos 12–24 meses) y su variabilidad.
    - Lead times y fiabilidad de cada proveedor.
    - Políticas de servicio por categoría de producto.
    - Costes de pedido y costes de mantenimiento de inventario.
    - Niveles de stock actuales y estructuras de lote/embalaje.
    - Cualquier regla de negocio especial (caducidad, lotes, restricciones de compra).

    Si quieres, te puedo ayudar a crear una plantilla de cálculo en tu hoja de cálculo o a orientar la configuración en tu ERP con ejemplos adaptados a tu catálogo.

    ---------------

    Punto de pedido
    @@@@@@@@@@@@@@@
    https://a3responde.wolterskluwer.com/es/s/article/como-crear-un-trabajador-autonomo, https://a3responde.wolterskluwer.com/es/s/article/como-hacer-una-afiliacion-de-un-trabajador-por-sistema-red, https://a3responde.wolterskluwer.com/es/s/article/190-gastos-de-seguridad-social-se-duplican-en-a01-a02, https://a3responde.wolterskluwer.com/es/s/article/afiliaciones-como-generar-el-movimiento-ma-alta-de-los-trabajadores
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