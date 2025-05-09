import json
import re 

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
d= leer_datos()
print(d)
