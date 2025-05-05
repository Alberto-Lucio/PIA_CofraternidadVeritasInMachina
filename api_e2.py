##Version 1.2.3
import re
import requests
import json

# Construir URL para la API de Open Library según el criterio de búsqueda
def construir_url(criterio, consulta):
    criterios_api = {
        "titulo": "title",
        "autor": "author",
        "tema": "subject",
        "isbn": "isbn"
    }
    clave_api = criterios_api.get(criterio.lower())
    if clave_api:
        consulta_f = consulta.strip().replace(' ', '+')
        return f"https://openlibrary.org/search.json?{clave_api}={consulta_f}"
    return None

# Validar la entrada del usuario según el criterio de búsqueda
def validar_input(criterio, valor):
    patrones = {
        'autor': r"^([\w\s.\-']){2,100}$",
        'titulo': r"^([\w\s\-:'.,!?]){2,100}$",
        'tema': r"^([\w\s\-]){2,50}$",
        'isbn': r"^\d{10}(\d{3})?$"
    }
    # Se usan expresiones regulares para validar la entrada y se eliminan espacios al inicio y al final del valor
    return re.fullmatch(patrones.get(criterio, ""), valor.strip()) is not None

## Limpiar espacios extra y saltos de línea de los datos
def limpiar_dato(texto):
    """Limpiar espacios extra y saltos de línea de los datos."""
    if isinstance(texto, str):
        return texto.strip().replace('\n', ' ')
    return texto

## Limpiar los resultados obtenidos de la API para obtener solo datos relevantes
def limpiar_resultados(libros):
    resultados_limpios = []
    for libro in libros:
        # Solo conservamos los datos relevantes
        titulo = limpiar_dato(libro.get('title', 'Título desconocido'))
        autores_lista = libro.get('author_name', ['Autor desconocido'])
        autores = ', '.join([limpiar_dato(nombre) for nombre in autores_lista])
        fecha = libro.get('first_publish_year', 'Año desconocido')
        isbn_lista = libro.get('isbn', [])
        isbn = isbn_lista[0] if isbn_lista else 'ISBN desconocido'
        
        # Crear un diccionario limpio para cada libro
        libro_limpio = {
            "número": len(resultados_limpios)+1,  
            "título": titulo,
            "autores": autores,
            "año de publicación": fecha,
            "ISBN": isbn
        }
        # Agregar el libro limpio a la nueva estructura de datos
        resultados_limpios.append(libro_limpio)

    return resultados_limpios

## Función principal para buscar libros
def buscar_libros():
    while True:
        print("\n=== MENÚ DE BÚSQUEDA DE LIBROS ===")
        print("1. Buscar por autor")
        print("2. Buscar por título")
        print("3. Buscar por tema")
        print("4. Buscar por ISBN")
        print("5. Salir")

        opcion = input("Seleccione una opción (1-5): ").strip()

        criterios = {
            '1': 'autor',
            '2': 'titulo',
            '3': 'tema',
            '4': 'isbn'
        }

        if opcion == '5':
            print("Saliendo del buscador")
            break
        elif opcion in criterios:
            criterio = criterios[opcion]
            valor = input(f"Ingrese la búsqueda para '{criterio}': ").strip()
            
            if not validar_input(criterio, valor):
                print(f"Entrada inválida para '{criterio}'. Inténtelo nuevamente.")
                continue

            url = construir_url(criterio, valor)
            if not url:
                print("Error al construir la URL.")
                continue
            ## Verificar la disponibilidad de la API de Open Library
            try:
                test_response = requests.get("https://openlibrary.org")
                if test_response.status_code != 200:
                    print("La API de Open Library no está disponible.")
                    continue
            except requests.exceptions.RequestException:
                print("No se pudo establecer conexión con la API.")
                continue

            print(f"\n Consultando: {url}")
            try:
                respuesta = requests.get(url)
                respuesta.raise_for_status()
                datos = respuesta.json()
                libros = datos.get('docs', [])

                if not libros:
                    print("No se encontraron resultados.")
                else:
                    # Limpiar los resultados obtenidos
                    resultados = limpiar_resultados(libros[:10])

                    # Mostrar los primeros 10 resultados
                    for libro in resultados:
                        print(f"\n{libro['título']} \nAutor(es): {libro['autores']} \nAño de publicación: {libro['año de publicación']} \nISBN: {libro['ISBN']}")
                    
                    # Guardar los resultados limpios en un archivo JSON
                    with open('resultados.json', 'w', encoding='utf-8') as resultados_json:
                        json.dump(resultados, resultados_json, indent=4)
                    print("\n Resultados guardados en 'resultados_json.json'.")
                    
                    # Guardar los resultados limpios en un archivo CSV
                    with open('resultados.csv', 'w', encoding='utf-8') as resultados_csv:
                        resultados_csv.write("Número,Título,Autores,Año de publicación,ISBN\n")
                        for libro in resultados:
                            resultados_csv.write(f"{libro['número']},{libro['título']},{libro['autores']},{libro['año de publicación']},{libro['ISBN']}\n")
            
            # Manejar errores de conexión y respuesta
            except requests.exceptions.RequestException as e:
                print(f"Error al conectar con la API: {e}")
        else:
            print("Opción inválida. Por favor, elija un número entre 1 y 5.")
if __name__ == "__main__":
    buscar_libros()
