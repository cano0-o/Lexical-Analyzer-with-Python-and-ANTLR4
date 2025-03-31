import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
from collections import Counter
from utils.handle_file import COMBINED_PATTERN, TOKEN_TYPES

def escribir_resultados(symbol_table: list, output_file: str) -> None:
    """
    Genera un archivo PDF con los resultados del análisis léxico, incluyendo la frecuencia de los diferentes
    tipos de tokens encontrados en el código fuente, una gráfica visual de dicha frecuencia, y una lista detallada
    de los tokens con su ubicación en el código.

    Esta función toma como entrada la tabla de símbolos generada por el análisis léxico (una lista de tuplas),
    y crea un archivo PDF que contiene:
    - La frecuencia de cada tipo de token.
    - Una gráfica de barras que visualiza las frecuencias de los tokens.
    - Una lista completa de todos los tokens con su tipo, valor y posición (línea y columna).

    Args:
        symbol_table (list): Lista de tuplas generada por el analizador léxico. Cada tupla contiene:
                            - tipo de token (str): El tipo de token, como palabra reservada o identificador.
                            - valor del token (str): El valor exacto del token en el código.
                            - línea (int): Línea en la que se encuentra el token.
                            - columna (int): Columna donde inicia el token en el código.
        output_file (str): Ruta y nombre del archivo PDF de salida.

    Returns:
        None: La función no devuelve ningún valor, sino que guarda los resultados en un archivo PDF.

    Excepciones:
        - Si no se puede crear el archivo PDF, se lanzará una excepción relacionada con permisos o errores de escritura.
        - Si ocurre un error al generar la gráfica de frecuencias, como un fallo al guardar la imagen, se lanzará una excepción.

    Consideraciones:
        - La función genera un archivo temporal `output/token_frequencies.png` para la gráfica de frecuencias,
        y se debe asegurar de que la carpeta `output/` existe y tiene permisos de escritura.
        - Cada página en el PDF tiene un límite de espacio, y si la lista de tokens es extensa, se generarán nuevas páginas automáticamente.

    Ejemplo de uso:
        >>> symbol_table = [('PR', 'int', 1, 1), ('ID', 'x', 1, 5), ('AS', '=', 1, 7), ...]
        >>> escribir_resultados(symbol_table, 'resultados_lexicos.pdf')

    Formato de salida:
        - La lista de tokens en el PDF se presenta en el formato "[línea,columna] tipo: valor".
        - Los tipos de token incluyen valores como PR (palabra reservada), ID (identificador), AS (asignación), etc.
    """

    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter
    y = height - 40  # Posición vertical inicial

    # Inicializar contadores para cada tipo de token
    categories = {token_name: 0 for token_name in TOKEN_TYPES.values()}

    # Contar la frecuencia de cada tipo de token
    for token_type, token_value, line, column in symbol_table:
        if token_type in categories:
            categories[token_type] += 1

    # Escribir resultados en el PDF
    c.drawString(40, y, "Resultados del análisis léxico:")
    y -= 20  # Espacio entre líneas

    # Escribir la lista con la frecuencia de tokens
    c.drawString(40, y, "Frecuencia de Tokens:")
    y -= 10

    # Escribir cada tipo de token y su frecuencia
    for token_name, count in categories.items():
        c.drawString(40, y, f"{token_name}: {count}")
        y -= 10

    y -= 10  # Espacio después de la lista

    # Mostrar la cantidad total de tokens
    total_tokens = sum(categories.values())
    c.drawString(40, y, f"Total de tokens: {total_tokens}")
    y -= 20  # Espacio después del total

    # Graficar la frecuencia de tipos de tokens
    plt.figure(figsize=(10, 5))
    plt.bar(categories.keys(), categories.values())
    plt.title("Frecuencia de Tokens")
    plt.xlabel("Tipos de Tokens")
    plt.ylabel("Frecuencia")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Guardar la gráfica como imagen
    plt.savefig("output/token_frequencies.png")
    plt.close()

    # Insertar la gráfica en el PDF
    c.drawImage("output/token_frequencies.png", 40, y - 200, width=500, height=200)  # Ajusta las dimensiones según sea necesario
    y -= 210  # Ajustar la posición después de la imagen

    # Escribir la lista completa de tokens con sus posiciones
    c.drawString(40, y, "Lista de Tokens:")
    y -= 20  # Espacio antes de la lista de tokens

    for token_type, token_value, line, column in symbol_table:
        # Modificación del formato de salida
        c.drawString(40, y, f"[{line},{column}] {token_type}: {token_value}")
        y -= 20  # Espacio entre líneas
        if y < 40:  # Si se alcanza el borde inferior, crea una nueva página
            c.showPage()
            y = height - 40

    c.showPage()  # Inicia una nueva página al final
    c.save()
