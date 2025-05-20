from bs4 import BeautifulSoup
import requests
import csv

def descargar_pagina(url):
    req = requests.get(url)
    if req.status_code == 200:
        return BeautifulSoup(req.text, "html.parser")
    else:
        print("Error de conexión: ", req.status_code)
        return None

def libro_disponible(texto):
    return "si" if "In stock" in texto else "no"

url_pagina = "https://books.toscrape.com/catalogue/page-1.html"
pagina = descargar_pagina(url_pagina)

with open("disponibilidad_libros.csv", "w", newline="", encoding="utf-8") as archivo_csv:
    escribir = csv.writer(archivo_csv)
    escribir.writerow(["Título", "Disponible"])  

    if pagina:
        libros = pagina.find_all("article", class_="product_pod")
        for libro in libros:
            titulo = libro.find("h3").find("a")["title"]
            href = libro.find("h3").find("a")["href"]
            catalogo = "https://books.toscrape.com/catalogue/"  + href
            detalle = descargar_pagina(catalogo)
            if detalle:
                disponibilidad = detalle.find("p", class_="instock availability")
                disponibilidad_texto = disponibilidad.get_text(strip=True)
                esta_disponible = libro_disponible(disponibilidad_texto)
                
                escribir.writerow([titulo, esta_disponible])
    else:
        print("Error de conexión: No se pudo cargar la página.")
