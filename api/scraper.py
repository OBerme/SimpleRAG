import asyncio
import urllib.parse
import json
from pathlib import Path
from playwright.async_api import async_playwright

# Se usa async_playwright para las operaciones asíncronas
# El módulo os o pathlib se usa para manejo de archivos/carpetas
# El módulo urllib.parse se usa para codificar la búsqueda

async def get_links_to_folder(search: str, folder_path: str):
    """
    Navega a la página de búsqueda, "escucha" una petición de API específica
    y guarda las URLs extraídas en un archivo JSON.
    """
    # 1. Preparar
    search_codificate = urllib.parse.quote(search)
    folder = Path(folder_path)
    
    # Crear la carpeta si no existe
    folder.mkdir(parents=True, exist_ok=True)
    
    output_filepath = folder / "extracted_urls.json"
    all_collected_urls = []
    
    # Usamos un objeto Event de asyncio como mecanismo de "trampa"
    # para simular el resolve() de la Promesa de JavaScript.
    api_response_captured = asyncio.Event()

    print("🚀 Iniciando Playwright...")
    async with async_playwright() as p:
        # Iniciamos el navegador (por defecto es headless=True)
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # 2. CONFIGURAR EL "CEPO" (LA TRAMPA)
        # Usamos page.on("response") al igual que en Puppeteer JS
        
        def handle_response(response):
            """Función callback que se ejecuta en cada respuesta de red."""
            url = response.url
            method = response.request.method

            # Filtramos solo la API que nos interesa (POST y v2/search)
            if (
                method == "POST" and
                ("/rest/search/v2" in url or "global-search" in url)
            ):
                print("⚡ ¡Petición de API detectada!")
                
                # Para evitar bloquear el hilo principal y manejar la lógica
                # asíncrona dentro del callback, usamos asyncio.create_task.
                asyncio.create_task(extract_and_save_data(response))
        
        async def extract_and_save_data(response):
            """Lógica de extracción y guardado, ejecutada de forma asíncrona."""
            nonlocal all_collected_urls # Permitir modificar la lista fuera de esta función
            
            try:
                # Obtenemos el cuerpo JSON de la respuesta
                json_body = await response.json()

                # ✅ LÓGICA DE EXTRACCIÓN
                if json_body.get("results") and isinstance(json_body["results"], list):
                    
                    # Extraemos solo el clickUri
                    new_urls = [item.get("clickUri") for item in json_body["results"] if item.get("clickUri")]
                    
                    # Añadimos a la lista principal
                    all_collected_urls.extend(new_urls)

                    print(f"⚡ Encontradas {len(new_urls)} URLs en este lote.")

                    # Guardamos en fichero
                    # El modo 'w' sobreescribe el contenido en cada iteración, como en el JS
                    with open(output_filepath, 'w', encoding='utf-8') as f:
                        json.dump(all_collected_urls, f, indent=2)

                    print(f"💾 Fichero guardado: {output_filepath}")

                    # 🎯 ¡HECHO! Activamos el Evento para liberar el script
                    api_response_captured.set()
                
            except Exception as e:
                # Si falla el parseo, ignoramos y seguimos escuchando
                # print(f"Error procesando JSON: {e}") 
                pass


        # Conectamos el "oído" al navegador
        page.on("response", handle_response)
        
        # 3. NAVEGAR (El "disparador")
        print("Navegando...")
        
        url_a_navegar = (
            "https://a3responde.wolterskluwer.com/es/s/global-search/" 
            + search_codificate 
            + "&sort=relevancy&numberOfResults=100"
        )
        
        # En Playwright usamos page.goto y wait_until para esperar la carga
        await page.goto(
            url_a_navegar, 
            wait_until="networkidle" # Similar a networkidle2 en Puppeteer
        )

        # 4. ESPERAR A LA CAPTURA
        print("⏳ Esperando a que la API responda y capturemos los datos...")
        
        try:
            # Aquí el script se pausa hasta que llamamos a 'api_response_captured.set()'
            await api_response_captured.wait() 
            print("✅ Proceso completado con éxito.")
        except asyncio.CancelledError:
            print("❌ Algo salió mal esperando los datos.")
        
        # 5. CERRAR
        await browser.close()

# --- Ejecución Principal ---
# if __name__ == "__main__":
#     # Ejemplo de uso:
#     search_term = "contrato de trabajo"
#     output_dir = "enlaces_extraidos"
    
#     # Se utiliza asyncio.run() para ejecutar la función asíncrona principal
#     asyncio.run()