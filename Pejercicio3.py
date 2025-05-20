from bs4 import BeautifulSoup
import requests
import re
import csv

def descargar_pagina(url):
    req = requests.get(url)
    if req.status_code == 200:
        return BeautifulSoup(req.text, "html.parser")
    else:
        print("Error de conexión: ", req.status_code)
        return None

def limpiar_titulo(titulo):
    titulo_limp = re.sub(r'[^A-Za-z0-9\s]', '', titulo)
    return titulo_limp.strip()

paginas_url = "https://books.toscrape.com/catalogue/page-{}.html"
titulos = []

for pag in range(1, 4):
    url = paginas_url.format(pag) # .format(pag) reemplaza ese {} por el número de página correspondiente ejemplo de la url: 'https://books.toscrape.com/catalogue/page-3.html'
    pagina = descargar_pagina(url)
    if pagina:
        libros = pagina.find_all("article", class_="product_pod")
        for i in libros:
            titulo_pagina = i.find("h3").find("a")["title"]
            titulos.append(limpiar_titulo(titulo_pagina)) # agrega a la lista tilulos los titulos limpios 
    else:
        print("Error de conexión: No se pudo cargar la página.")


with open("titulos.csv", "w", newline="", encoding="utf-8") as archivo:
    escribir = csv.writer(archivo)
    escribir.writerow(["Títulos"])
    for titulo in titulos:
        escribir.writerow([titulo])


