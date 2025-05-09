import json
import re 

## Rescatar los datos de un archivo JSON
def leer_datos(json_path= 'resultados.json'):
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

d= leer_datos()
print(d)
