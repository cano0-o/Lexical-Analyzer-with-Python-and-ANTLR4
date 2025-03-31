"""
Definiciones de palabras clave, operadores, delimitadores y patrones de expresiones regulares
para el análisis léxico de un lenguaje de programación.

1. Listas de palabras clave, operadores, y delimitadores:
   - `KEYWORDS`: Lista de palabras clave que incluye términos reservados como `int`, `if`, `else`, `for`, etc.
   - `LOGICAL_OPS`: Operadores lógicos (`&&`, `||`, `!`).
   - `ASIGNATION`: Operador de asignación (`=`).
   - `COMP_OPS`: Operadores de comparación (`>=`, `<=`, `==`, `!=`, `>`, `<`).
   - `DELIMITERS`: Caracteres delimitadores (`()`, `{}`, `;`, `,`, `:`).
   - `ARITH_OPS`: Operadores aritméticos (`+`, `-`, `*`, `/`, `%`).

2. Diccionario `TOKEN_TYPES`:
   Define las categorías de tokens en el análisis léxico. Los valores son abreviaturas para identificar cada tipo de token:
   - `"PR"`: Palabras clave
   - `"OL"`: Operadores lógicos
   - `"OA"`: Operadores aritméticos
   - `"OC"`: Operadores de comparación
   - `"DL"`: Delimitadores
   - `"ID"`: Identificadores
   - `"AS"`: Asignación
   - `"NU"`: Números
   - `"UK"`: Tokens desconocidos
   - `"CT"`: Caracteres
   - `"ST"`: Cadenas de texto

3. Expresiones regulares (`PATTERNS`):
   Cada tipo de token tiene una expresión regular asociada en esta lista. Cada entrada es una tupla (`pattern`, `type`):
   - `pattern`: Expresión regular que detecta un tipo específico de token.
   - `type`: Tipo de token definido en `TOKEN_TYPES`.

   Ejemplos:
   - `r'\b' + r'\b|\b'.join(KEYWORDS) + r'\b'` para palabras clave, garantizando coincidencias completas.
   - `r'"(.*?)"'` para capturar cadenas entre comillas dobles.
   - `r'\b\d+(\.\d+)?\b'` para números enteros o decimales.

4. Patrón combinado (`COMBINED_PATTERN`):
   - Genera un patrón que combina todos los patrones en `PATTERNS`.
   - Utiliza `(?P<type>pattern)` para capturar cada tipo de token, lo que facilita la identificación
     de tipos durante el análisis.
   - Excluye líneas en blanco y caracteres desconocidos no definidos en `TOKEN_TYPES`.
"""

import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
from collections import Counter

# Listado de palabras clave, operadores y delimitadores
KEYWORDS = ["void", "int", "if", "else", "for", "while", "return", "main", "printf", "double", "float", "char", "case", "default", "switch"]
LOGICAL_OPS = ["&&", r"\|\|", "!"]
ASIGNATION = ["="]  
COMP_OPS = [">=", "<=", "==", "!=", ">", "<"]
DELIMITERS = [r"\(", r"\)", "{", "}", ";", ",", ":"]
ARITH_OPS = [r"\+", "-", r"\*", "/", "%"]

# Diccionario de tipos de tokens
TOKEN_TYPES = {
    "kw": "PR",  # Palabra clave
    "log_op": "OL",  # Operadores lógicos
    "arith_op": "OA",  # Operadores aritméticos
    "comp_op": "OC",  # Operadores de comparación
    "delim": "DL",  # Delimitadores
    "id": "ID",  # Identificadores
    "asign": "AS",  # Asignación
    "number": "NU",  # Números
    "unknown": "UK",  # Tokens desconocidos
    "char": "CT",  # Caracteres
    "string": "ST"  # Cadenas de texto
}

# Expresiones regulares para cada tipo de token
PATTERNS = [
    (r'\b' + r'\b|\b'.join(KEYWORDS) + r'\b', "kw"),  # Palabras clave
    (r'|'.join(LOGICAL_OPS), "log_op"),  # Operadores lógicos
    (r'|'.join(ARITH_OPS), "arith_op"),  # Operadores aritméticos
    (r'|'.join(COMP_OPS), "comp_op"),  # Operadores de comparación
    (r'|'.join(DELIMITERS), "delim"),  # Delimitadores
    (r'|'.join(ASIGNATION), "asign"),  # Asignación
    (r'"(.*?)"', "string"),  # Cadenas entre comillas dobles
    (r'\'(.*?)\'', "char"),  # Caracteres entre comillas simples
    (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', "id"),  # Identificadores (letras, números, guiones bajos)
    (r'\b\d+(\.\d+)?\b', "number"),  # Números enteros y decimales
    (r'//.*?$|/\*.*?\*/', "comment"),  # Comentarios de una línea y bloque
    (r'^\s*$', None),  # Ignorar líneas en blanco
    (r'[^a-zA-Z0-9\s]+', "unknown")  # Caracteres desconocidos
]

# Patrón combinado que abarca todos los tipos de tokens
COMBINED_PATTERN = "|".join(f"(?P<{type}>{pattern})" for pattern, type in PATTERNS if type is not None)
