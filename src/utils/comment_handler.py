import re
from reportlab.lib.pagesizes import letter

def esconder_comentarios(source_code: str) -> str:
    """
    Elimina los comentarios de bloque y de una línea de un fragmento de código fuente, reemplazándolos
    con espacios para mantener la estructura de líneas del código original.

    Args:
        source_code (str): Cadena de texto que contiene el código fuente con comentarios de bloque 
                           y de línea.

    Returns:
        str: Código fuente sin comentarios, con espacios en lugar de los comentarios eliminados, 
             preservando el número de líneas original.

    Detalles:
        - Los comentarios de bloque `/* ... */` son reemplazados por espacios y la misma cantidad 
          de saltos de línea que el comentario, asegurando que la numeración de líneas se mantenga.
        - Los comentarios de una sola línea `// ...` se eliminan junto con el contenido de esa línea.

    Ejemplo de uso:
        >>> source_code = '''
        ... /* Comentario de bloque */
        ... int a = 5; // Comentario de línea
        ... '''
        >>> print(esconder_comentarios(source_code))
        ...
        int a = 5; 
    """
    # Reemplazar comentarios de bloque (/* ... */) con saltos de línea equivalentes
    source_code = re.sub(r'/\*.*?\*/', lambda match: '\n' * match.group(0).count('\n'), source_code, flags=re.DOTALL)
    
    # Reemplazar comentarios de una línea (// ...) eliminándolos
    source_code = re.sub(r'//.*', '', source_code)
    
    return source_code
