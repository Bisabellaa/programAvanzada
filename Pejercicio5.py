from bs4 import BeautifulSoup
import requests
from collections import defaultdict # es una libreria que cuenta los libros tuve que buscar como hacerlo porque no tenia idea.

def descargar_pagina(url):
    req = requests.get(url)
    if req.status_code == 200:
        return BeautifulSoup(req.text, "html.parser")
    else:
        print("Error al cargar:", url)
        return None

def libro_disponible(texto):
    return "si" if "In stock" in texto else "no"

disponibilidad_categoria = defaultdict(int) # creo un diccionario para contar disponibilidad por categoría. los va a contar automaticamente
url_pagina = "https://books.toscrape.com/catalogue/page-{}.html"

for num_pagina in range(1, 4): 
    url = url_pagina.format(num_pagina)
    pagina = descargar_pagina(url)
    
    if pagina:
        libros = pagina.find_all("article", class_="product_pod")
        for libro in libros:
            titulo = libro.find("h3").find("a")["title"]
            href = libro.find("h3").find("a")["href"]
            catalogo = "https://books.toscrape.com/catalogue/" + href
            detalle = descargar_pagina(catalogo)
            if detalle:
                # Extraer categoría (segundo <li> del breadcrumb)
                breadcrumb = detalle.find("ul", class_="breadcrumb")
                categoria = breadcrumb.find_all("li")[2].text.strip()
                
                # Extraer disponibilidad
                disponibilidad = detalle.find("p", class_="instock availability")
                disponible = libro_disponible(disponibilidad.get_text(strip=True))
                
                # Si está disponible, contamos 1 en su categoría
                if disponible == "si":
                    disponibilidad_categoria[categoria] += 1

print("Disponibilidad por categoría:")
for categoria, cantidad in disponibilidad_categoria.items():
    print(categoria ,":", cantidad)
