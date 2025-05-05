import json
import requests

def buscar_libro(cons):
    url = f"https://openlibrary.org/search.json?q={cons}"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            datos = json.loads(response.text)
            with open("libreria.json", 'w') as archivo:
                json.dump(datos, archivo, indent=4)
                
            if datos["docs"]:
                for libro in datos["docs"]:
                    print("\n\tTítulo:", libro.get("title"))
                    print("Autor:", libro.get("author_name"))
                    print("Año de publicación:", libro.get("first_publish_year"))
                    print("ISBN:", libro.get("isbn"))
                    olid = libro.get("key")
                    if olid:
                      url_d = f"https://openlibrary.org{olid}.json"
                      response_d = requests.get(url_d)
                      response_d.raise_for_status()
                      datos_d = response_d.json()
                      print("Descripcion:", datos_d.get("description"))
                    print("-" * 20)
            else:
                print("No se encontraron libros.")
        except json.JSONDecodeError as e:
            print("Error al decodificar JSON:", e)
    else:
        print("Error al obtener los datos.")
x = True
while x:
    cons = input("Ingrese el título o autor del libro: ")
    resp = buscar_libro(cons)
    x = input("¿Desea buscar otro libro? si/no: ")=="si"
