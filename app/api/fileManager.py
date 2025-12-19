import os
import glob


class FileManager:
    @staticmethod
    def cargar_documentos_markdown_contenido(directorio: str):
        
        """
        Busca y lee todos los archivos .md en el directorio especificado 
        y los devuelve como una lista de strings para Qdrant.
        
        Args:
            directorio: La ruta donde se encuentran tus archivos Markdown.
            
        Returns:
            Una lista de strings, donde cada elemento es el contenido 
            de un archivo Markdown.
        """
        documentos_cargados = []
        
        # 1. Definir el patrón de búsqueda para archivos .md
        # glob.glob busca todos los archivos que coinciden con el patrón
        ruta_busqueda = os.path.join(directorio, "*.md")
        
        # 2. Iterar sobre todos los archivos encontrados
        for ruta_archivo in glob.glob(ruta_busqueda):
            try:
                # 3. Abrir el archivo y leer su contenido
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    file_size = os.path.getsize(ruta_completa)
                    if file_size != 0:
                        contenido = f.read()
                        
                        # Opcional: Limpiar espacios en blanco extra al inicio/fin
                        contenido = contenido.strip()
                        
                        # 4. Añadir el contenido a la lista
                        documentos_cargados.append(contenido)
                    
            except Exception as e:
                print(f"Error al leer el archivo {ruta_archivo}: {e}")
                
        return documentos_cargados
    
    #Pre:
    #Post: este metodo devuelve una matriz tal que asi:
    #   ejemplo[0] == [document_name, document_content ]
    # va a devolver una lista que tiene listas dentro y cada lista que tiene dentro
    # tiene como primer dato el nombre del documento y como segundo el chunk de ese documento
    @staticmethod
    def get_matrix_documents(directorio: str):
        base_name_with_ext = os.path.basename(directorio)
            
        # 2. Obtener solo el nombre (sin la extensión .md)
        # os.path.splitext() divide la ruta en (root, ext)
        document_name = os.path.splitext(base_name_with_ext)[0]
        """
        Busca y lee todos los archivos .md en el directorio especificado 
        y los devuelve como una lista de strings para Qdrant.
        
        Args:
            directorio: La ruta donde se encuentran tus archivos Markdown.
            
        Returns:
            Una lista de strings, donde cada elemento es el contenido 
            de un archivo Markdown.
        """
        documentos_cargados = []
        
        # 1. Definir el patrón de búsqueda para archivos .md
        # glob.glob busca todos los archivos que coinciden con el patrón
        ruta_busqueda = os.path.join(directorio, "*.md")
        
        # 2. Iterar sobre todos los archivos encontrados
        for ruta_archivo in glob.glob(ruta_busqueda):
            try:
                    
                # 1. Obtener solo el nombre del archivo (con extensión)
                base_name_with_ext = os.path.basename(ruta_archivo)
                
                # 2. Obtener solo el nombre (sin la extensión .md)
                # os.path.splitext() divide la ruta en (root, ext)
                document_name = os.path.splitext(base_name_with_ext)[0]
                
                # 3. Abrir el archivo y leer su contenido
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    file_size = os.path.getsize(ruta_archivo)
                    
                    if file_size != 0:
                        contenido = f.read()
                        
                        # Opcional: Limpiar espacios en blanco extra al inicio/fin
                        contenido = contenido.strip()
                        
                        # 4. Añadir el contenido a la lista
                        documentos_cargados.append([document_name, contenido])
                    
            except Exception as e:
                print(f"Error al leer el archivo {document_name}: {e}")
                
        return documentos_cargados
    
    @staticmethod
    def deleteAllFiles(folder_path):
        if not os.path.exists(folder_path):
            print(f"Error: The folder '{folder_path}' does not exist.")
            return

        if not os.path.isdir(folder_path):
            print(f"Error: '{folder_path}' is not a directory.")
            return
        try:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                # Only delete files, skip directories
                if os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                        print(f"Deleted file: {file_path}")
                    except OSError as e:
                        print(f"Failed to delete {file_path}: {e}")
            print("✅ All files removed successfully.")
        except Exception as e:
            print(f"Unexpected error: {e}")
            
    def recopilar_nombres_markdown(directorio: str) -> list[str]:
        """
        Busca todos los archivos .md en el directorio especificado 
        y devuelve solo sus nombres (sin la ruta completa).

        Args:
            directorio: La ruta donde se encuentran tus archivos Markdown.

        Returns:
            Una lista de strings, donde cada elemento es el nombre del archivo (ej. 'documento_a.md').
        """
        nombres_archivos = []
        
        # 1. Definir el patrón de búsqueda para archivos .md
        ruta_busqueda = os.path.join(directorio, "*.md")
        
        # 2. Iterar sobre todos los archivos encontrados (obteniendo la ruta completa)
        for ruta_completa in glob.glob(ruta_busqueda):
            try:
                # 3. EXTRAER SOLO EL NOMBRE DEL ARCHIVO:
                file_size = os.path.getsize(ruta_completa)
                    
                if file_size != 0:
                    # Opción 1 (Usando os.path, como en tu código original):
                    nombre_archivo = os.path.basename(ruta_completa)
                    
                    # Opción 2 (Usando pathlib, más moderno):
                    # nombre_archivo = Path(ruta_completa).name
                    
                    # 4. Añadir el nombre a la lista
                    nombres_archivos.append(nombre_archivo)
                
            except Exception as e:
                print(f"Error al procesar la ruta {ruta_completa}: {e}")
                
        return nombres_archivos