
from bs4 import BeautifulSoup
import requests
import re # expresiones regulares elimina los caracteres especiales de los titulos 

def descargar_pagina(url):
    req = requests.get(url)
    if req.status_code == 200:
        return BeautifulSoup(req.text, "html.parser")
    else:
        print("Error de conexión: ", req.status_code)
        return None

def limpiar_titulos(titulo): # voy a usar sub que es una funcion de 're' que busca en un texto todos los caracteres y los subtituye en este caso por espacio.
    titulo_limp = re.sub(r'[^A-Za-z0-9\s]', '', titulo) # r'[^A-Za-z0-9\s]' es para decir que es cualquier carácter que no sea letra,may,min,número y ni espacio.
    return titulo_limp.strip() # el metodo stirp elimina los espacios en blanco

pagina = descargar_pagina("https://books.toscrape.com/")

if pagina:
    libros = pagina.find_all("article", class_="product_pod")
    for i in libros:
        titulo_pagina = i.find("h3").find("a")["title"]
        titulo_limp = limpiar_titulos(titulo_pagina)
        print(titulo_limp)
else:
    print("Error de conexión: No se pudo cargar la página.")
