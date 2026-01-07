# -----------------------------------------------------
# FASE 1: BASE E INSTALACIÓN DE DEPENDENCIAS
# -----------------------------------------------------
# Usamos una imagen oficial de Python 3.11 Slim (más pequeña)
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# -----------------------------------------------------
# INSTALACIÓN DE DEPENDENCIAS DE SISTEMA PARA PLAYWRIGHT/CHROMIUM
# -----------------------------------------------------

# Copia solo el archivo requirements.txt primero. 
# Esto aprovecha el caching de Docker. Si las dependencias no cambian,
# esta fase no se vuelve a ejecutar.
COPY requirements.txt .

# Instala las dependencias de Python
# El flag --no-cache-dir reduce el tamaño final de la imagen
RUN pip install --no-cache-dir -r requirements.txt

# Si has incluido 'playwright' en requirements.txt, necesitas instalar sus navegadores:
# Si NO usas playwright, puedes omitir estas 3 líneas.
# RUN if grep -q "playwright" requirements.txt; then \
#     pip install playwright; \
#     playwright install; \
# fi

# -----------------------------------------------------
# FASE 2: COPIA DEL CÓDIGO DE LA APLICACIÓN
# -----------------------------------------------------

# Copia todo el código de tu proyecto al directorio de trabajo /app
# Asume que tu código está en el mismo directorio que el Dockerfile
COPY . .

# Expone el puerto que usará tu aplicación (por defecto 8000 para Uvicorn/FastAPI)
EXPOSE 8001

# -----------------------------------------------------
# FASE 3: COMANDO DE ARRANQUE
# -----------------------------------------------------
# Comando para iniciar la aplicación. 
# Reemplaza 'app:app' con la ruta a tu aplicación si es diferente 
# (por ejemplo, 'main:app' si tu archivo es main.py)
CMD ["fastapi", "dev", "api_converstions.py", "--host", "0.0.0.0", "--port", "8001"]