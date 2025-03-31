import re
from reportlab.lib.pagesizes import letter
from utils.handle_file import COMBINED_PATTERN, TOKEN_TYPES

def analizador_lexico(source_code: str) -> list:
    """
    Realiza un análisis léxico sobre el código fuente proporcionado, extrayendo los tokens que lo componen
    y generando una tabla de símbolos con información detallada sobre cada token encontrado.

    La función recorre el código fuente línea por línea, identificando y clasificando los tokens mediante
    expresiones regulares definidas en `COMBINED_PATTERN`. Los tokens desconocidos o inválidos provocan
    un error con detalles sobre la ubicación del problema (línea y columna) en el código fuente.

    Args:
        source_code (str): Cadena de texto que contiene el código fuente a analizar.

    Returns:
        list: Una lista de tuplas, donde cada tupla representa un token con el siguiente formato:
            (tipo de token, valor del token, número de línea, número de columna).
            - El tipo de token se refiere a su categoría (por ejemplo, palabra clave, operador, identificador).
            - El valor del token es el valor literal encontrado en el código.

    Excepciones:
        - `ValueError`: Se lanza si se encuentra un token desconocido en el código fuente, con un mensaje
        de error que indica el valor del token y su ubicación (línea y columna).
        - `ValueError`: Se lanza si se detecta un valor incorrecto para un token tipo `char`. Solo se aceptan:
        - Valores vacíos representados como `''`
        - Valores con un solo carácter entre comillas simples, por ejemplo, `'a'`.

    Ejemplo de uso:
        >>> source_code = "int x = 10; // Asignación"
        >>> tokens = analizador_lexico(source_code)
        >>> for token in tokens:
        >>>     print(token)
        ('PR', 'int', 1, 1)
        ('ID', 'x', 1, 5)
        ('AS', '=', 1, 7)
        ('NU', '10', 1, 9)
        ('DL', ';', 1, 11)

    Consideraciones:
        - Los comentarios de línea son ignorados durante el análisis.
        - La columna de cada token es calculada en base a un índice que comienza en 1.
        - La función utiliza `TOKEN_TYPES` para mapear el tipo de token encontrado a una descripción estándar, 
        como 'PR' para palabras reservadas, 'ID' para identificadores, 'AS' para asignación, etc.
    """

    symbol_table = []  # Lista para almacenar la tabla de símbolos
    lines = source_code.splitlines()  # Dividir el código fuente en líneas
    
    for line_number, line in enumerate(lines, start=1):  # Iterar sobre cada línea
        for match in re.finditer(COMBINED_PATTERN, line):  # Buscar coincidencias de los tokens
            token_type = match.lastgroup  # Tipo de token encontrado
            token_value = match.group(token_type)  # Valor del token encontrado

            # Ignorar los comentarios
            if token_type == "comment":
                continue

            # Verificación de tokens desconocidos
            if token_type == "unknown":
                column_number = match.start() + 1  # Columna empieza en 1
                raise ValueError(f"Token desconocido '{token_value}' en línea {line_number}, columna {column_number}.")

            # Verificación para caracteres
            if token_type == "char":
                # Aceptar un valor vacío o un solo carácter
                if len(token_value) not in [3, 2]:  # Longitud: 1 (carácter) + 2 (comillas simples) o 0 (vacío) + 2 (comillas simples)
                    column_number = match.start() + 1  # Columna empieza en 1
                    raise ValueError(f"Carácter inválido '{token_value}' en línea {line_number}, columna {column_number}.")

            # Agregar el token a la tabla de símbolos
            if token_type is not None:
                column_number = match.start() + 1  # Columna empieza en 1
                symbol_table.append((TOKEN_TYPES[token_type], token_value, line_number, column_number))
    
    return symbol_table
