import json
import re 
import statistics 

## Rescatar los datos de un archivo JSON
def leer_datos_json(json_path= 'resultados.json'):
    try:
        with open(json_path, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            return datos
            
    except FileNotFoundError:
        print(f"El archivo {json_path} no se encontró.")
        return None
    except json.JSONDecodeError:
        print(f"Error al decodificar el archivo {json_path}.")
        return None

## Rescatar los datos de un archivo CSV
def leer_datos_csv(csv_path= 'resultados.csv'):
    try:
        with open(csv_path, "r", encoding="utf-8") as atributo:
            datos = atributo.readlines()
            datos_limpios = [linea.strip().split(",") for linea in datos]
            resultado = []
            for i, linea in enumerate(datos_limpios[1:]):
                libro = {
                    "número": i + 1,
                    "título": linea[1],
                    "autores": linea[2],
                    "año de publicación": linea[3],
                    "ISBN": linea[4]
                }
                resultado.append(libro)
            return resultado
    except FileNotFoundError:
        print(f"El archivo {csv_path} no se encontró.")
        return None

def analizar_datos(datos):
    años = []
    autores = []
    for libro in datos:
        año = libro.get("año de publicación")
        if año and str(año).isdigit():
            años.append(int(año))
        autores.extend(libro.get("autores", "").split(","))
    media_años = statistics.mean(años) if años else None
    mediana_años = statistics.median(años) if años else None
    moda_años = statistics.mode(años) if años else None
    minimo_años = min(años) if años else None
    maximo_años = max(años) if años else None
    autores_frec = statistics.multimode(autores)
    return {
        "Media de años": (f"{media_años:.2f}"),
        "Mediana de años": (f"{mediana_años:.2f}"),
        "Moda de años": (f"{moda_años:.2f}"),
        "Minimo de años": minimo_años,
        "Maximo de años": maximo_años,
        "Autores más frecuentes": autores_frec
    }    

def mostrar_resultados(analisis):

    print("\nAnálisis de datos:")
    print(f"Media de años: {analisis['Media de años']}")
    print(f"Mediana de años: {analisis['Mediana de años']}")
    print(f"Moda de años: {analisis['Moda de años']}")
    print(f"Minimo de años: {analisis['Minimo de años']}")
    print(f"Maximo de años: {analisis['Maximo de años']}")
    print(f"Autores más frecuentes: {', '.join(analisis['Autores más frecuentes'])}")

def main():
    # Leer datos de JSON
    datos_json = leer_datos_json()
    if datos_json:
        analisis_json = analizar_datos(datos_json)
        mostrar_resultados(analisis_json)

    # Leer datos de CSV
    datos_csv = leer_datos_csv()
    if datos_csv:
        analisis_csv = analizar_datos(datos_csv)
        mostrar_resultados(analisis_csv)  

if __name__ == "__main__":
    main()  
