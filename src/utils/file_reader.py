def lector_archivos(file_path: str) -> str:
    """
    Lee el contenido de un archivo de texto especificado por su ruta.

    La función intenta abrir y leer un archivo en formato de texto utilizando la codificación UTF-8.
    Si el archivo no se encuentra o no se puede abrir debido a un error de entrada/salida, se captura la excepción 
    y se informa al usuario sin interrumpir el programa.

    Args:
        file_path (str): Ruta del archivo que se desea leer.

    Returns:
        str: El contenido del archivo como una cadena de texto si se lee correctamente, o `None` si ocurre un error.

    Excepciones:
        FileNotFoundError, IOError: Se captura si el archivo no existe o hay problemas de permisos.
                                    Se imprime un mensaje de error en la consola.

    Ejemplo de uso:
        >>> file_path = 'documento.txt'
        >>> contenido = lector_archivos(file_path)
        >>> if contenido is not None:
        >>>     print(contenido)
        >>> else:
        >>>     print("No se pudo leer el archivo.")
    """
    try:
        # Intentar abrir y leer el archivo
        with open(file_path, 'r', encoding='utf8') as file:
            return file.read()
    except (FileNotFoundError, IOError):
        # Captura de errores si el archivo no puede ser abierto
        print(f"Error: No se pudo acceder al archivo '{file_path}'.")
        return None
