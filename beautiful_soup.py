import requests
from bs4 import BeautifulSoup

url = 'https://dockerlabs.es'
res = requests.get(url)



if res.status_code == 200:
    soup = BeautifulSoup(res.text, 'html.parser')

    maquinas = soup.find_all('div', onclick=True)
    conteo_maquinas = 1
    autores = set()

    for maquina in maquinas:
        onclick_text = maquina['onclick']
        autor = onclick_text.split("'")[7]
        autores.add(autor)

        nombre_maquina = onclick_text.split("'")[1]

        print(f' {conteo_maquinas} {nombre_maquina} - {autor}')
        conteo_maquinas += 1
        print("Autores encontrados: ")
        for autor in autores:
            print(autor)
else:
    print(f'Hubo un error al hacer la petiicion {res.status_code}')