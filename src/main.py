import os
from utils.file_reader import lector_archivos
from utils.comment_handler import esconder_comentarios
from utils.lexical_analyzer import analizador_lexico
from utils.pdf_writer import escribir_resultados

def main():
    """
    Función principal del programa que realiza un análisis léxico de un archivo de texto, eliminando los comentarios
    y generando un archivo PDF con los resultados. Este proceso incluye los siguientes pasos:

    1. Leer el archivo de código fuente especificado.
    2. Eliminar los comentarios del código.
    3. Realizar un análisis léxico para extraer tokens y generar una tabla de símbolos.
    4. Crear un informe en PDF que incluye la frecuencia de tokens, visualización gráfica, y una lista de tokens con sus posiciones en el código fuente.

    Módulos Importados:
    - `lector_archivos`: Lee el contenido del archivo de entrada.
    - `esconder_comentarios`: Procesa el texto para eliminar o esconder comentarios manteniendo la estructura de líneas.
    - `analizador_lexico`: Realiza el análisis léxico sobre el texto proporcionado.
    - `escribir_resultados`: Genera un archivo PDF con los resultados del análisis léxico.

    Args:
        Ninguno.

    Returns:
        Ninguno.

    Excepciones:
        - Si el archivo de entrada no puede ser leído, se imprime un mensaje de error.
        - `ValueError`: Lanzada si el análisis léxico encuentra un token desconocido, e imprime un mensaje de error.
        - Otras excepciones relacionadas con la creación del PDF y rutas de archivo se capturan y manejan para asegurar la generación correcta del informe.

    Ejemplo de uso:
        Al ejecutar este script, se procesará el archivo `testing/test_lexico_01.txt`, eliminando comentarios y generando
        un informe de resultados en PDF llamado `resultados_lexicos.pdf`.

    Notas:
        - Asegúrate de que el archivo de entrada existe y contiene un código fuente válido.
        - La carpeta de salida (`output/`) debe existir, y el usuario debe tener permisos de escritura en esta ruta.
    """


    file_path = 'testing/test_lexico_01.txt'  # Ruta del archivo de entrada
    image_path = 'output/token_frequencies.png' # Ruta del archivo de salida grafico
    output_file = 'output/resultados_lexicos.pdf'  # Ruta del archivo de salida

    # Eliminar el archivo PDF existente si existe
    if os.path.exists(output_file):
        os.remove(output_file)
        os.remove(image_path)
        
    # Intento de leer el archivo de entrada
    sample_code = lector_archivos(file_path)
    
    if sample_code is not None:
        try:
            # Intento de limpiar comentarios y generar la "tabla de símbolos"
            sample_code = esconder_comentarios(sample_code)
            symbol_table = analizador_lexico(sample_code)
            
            # Si el análisis léxico es exitoso, escribir los resultados en el archivo de salida
            escribir_resultados(symbol_table, output_file)
            print(f"Resultados guardados en '{output_file}'.")
        
        except ValueError as e:
            # Imprimir mensaje de error si hay un token desconocido
            print(f"Error en el análisis léxico: {e}")
    else:
        print("Error: No se pudo procesar el archivo. ¿Está seguro de que existe?")

if __name__ == "__main__":
    main()