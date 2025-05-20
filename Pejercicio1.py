# 1) Crear una función pura que descargue la página y devuelva el objeto BeautifulSoup
#    Manejar posibles errores de conexión
from bs4 import BeautifulSoup
import requests # el req es para poder descargar la pagina 

def descargar_pagina(url):
    req = requests.get(url)
    if req.status_code == 200:  # status_code lo utilizo para verificar si la pag cargo ok ! 
        return BeautifulSoup(req.text, "html.parser")
    else:
        print("Error de conexión: ", req.status_code)
        return None

pagina = descargar_pagina("https://books.toscrape.com/") # instancio el objeto 

if pagina:
    print(pagina.title.text)  # imprimo por ejemplo el titulo de la pag para ver si cargo correctamente
else:
    print("Error de conexión: No se pudo cargar la página.")




