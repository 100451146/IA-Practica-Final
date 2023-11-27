# Este archivo contiene la implementacion del backend:
# - Recibe la imagen de entrada
# - Pasa la imagen por el modelo
# - Devuelve la categoria de la imagen

# Para las peticiones HTTP
from flask import Flask, request, render_template, redirect, url_for

# Para el web scrapping
from bs4 import BeautifulSoup
import requests

# Para el modelo
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

# Creamos la aplicación de flask
app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')

# Cargar el modelo
modelo = load_model('../modelo/modelo.hdf5')
# Copiar las clases del cuadernillo
clases = {0: 'Bulbasaur', 1: 'Caterpie', 2: 'Charizard', 3: 'Charmander',
          4: 'Dragonite', 5: 'Eevee', 6: 'Gengar', 7: 'Geodude', 8: 'Greninja',
          9: 'Jigglypuff', 10: 'Lapras', 11: 'Machop', 12: 'Magikarp',
          13: 'Meowth', 14: "MrMime", 15: 'Pikachu', 16: 'Rattata',
          17: 'Rayquaza', 18: 'Snorlax', 19: 'Squirtle'}


@app.route('/', methods=['GET', 'POST'])
def subir_imagen():
    print(request)
    if request.method == 'POST':
        # Guardamos la imagen que han subido como imagen.jpg
        imagen = request.files['imagen']
        imagen.save('./imagen.jpg')
        # Cargamos la imagen para que el modelo prediga
        imagen = image.load_img('./imagen.jpg', target_size=(128, 128))
        imagen_array = image.img_to_array(imagen)
        imagen_array = np.expand_dims(imagen_array, axis=0)
        # Predecimos con el modelo y devolvemos la prediccion
        prediccion = modelo.predict(imagen_array)
        prediccion = np.argmax(prediccion)
        pokemon_predicho = clases[prediccion]

        return redirect(url_for('stats_pokemon', pokemon_name=pokemon_predicho))

    if request.method == 'GET':
        # Mostramos el formulario HTML de subida de imagen
        return render_template('main.html')

    return render_template('main.html')


@app.route('/result/<pokemon_name>')
def stats_pokemon(pokemon_name):
    print('#' * 50)
    print('Pokemon\t\t', pokemon_name)

    # WIKIDEX
    # De wikidex vamos a sacar el las resistencias, debilidades e inmunidades
    url = 'https://wikidex.net/wiki/' + pokemon_name
    pagina = requests.get(url)
    soup = BeautifulSoup(pagina.content, 'html.parser')
    print('#' * 50)
    print('Wikidex')

    # DEBILIDADES
    # Estan en otra tabla con clase "tabpokemon", la ultima de la página
    tabla = soup.findAll('table', class_='tabpokemon')[-1]
    # print(tabla)
    # Las debilidades están en las filas 1 y 2
    # En cada fila hay 3 elementos <td> y en el tercero está lo que queremos,
    # una lista de <a> con la debilidad en el titulo
    tabla_debilidades = tabla.findAll('tr')[1:3]
    tabla_debilidades = [d.findAll('td')[2] for d in tabla_debilidades]
    tabla_debilidades = [d.findAll('a') for d in tabla_debilidades]
    tabla_debilidades = [[a['title'] for a in d] for d in tabla_debilidades]
    debilidades = [w for d in tabla_debilidades for w in d]
    print('Debilidades\t', debilidades)

    # RESISTENCIAS
    # Las resistencias están en las filas 4 y 5
    tabla_resistencias = tabla.findAll('tr')[4:6]
    tabla_resistencias = [d.findAll('td')[2] for d in tabla_resistencias]
    tabla_resistencias = [d.findAll('a') for d in tabla_resistencias]
    tabla_resistencias = [[a['title'] for a in d] for d in tabla_resistencias]
    resistencias = [s for d in tabla_resistencias for s in d]
    print('resistencias\t', resistencias)

    # INMUNIDADES
    # Las inmunidades están en la fila 6
    tabla_inmunidad = tabla.findAll('tr')[6]
    tabla_inmunidad = tabla_inmunidad.findAll('td')[2]
    tabla_inmunidad = tabla_inmunidad.findAll('a')
    tabla_inmunidad = [a['title'] for a in tabla_inmunidad]
    print('inmunidades\t', tabla_inmunidad)

    # MEGADEXTER
    # De Megadexter vamos a sacar los tipos y habilidades
    url = 'https://megadexter.com/dex/pokemon/' + pokemon_name
    pagina = requests.get(url)
    soup = BeautifulSoup(pagina.content, 'html.parser')
    print('#' * 50)
    print('Megadexter')
    # Toda la información está en divs con clase "row"
    tablas = soup.findAll('div', class_='row')

    # TIPOS
    # Los tipos están en la primera entrada
    tabla_general = tablas[0].find('div', title=f'Tipos de {pokemon_name}')
    tabla_general = tabla_general.findAll('a')
    tipos = [a['title'] for a in tabla_general]
    print('Tipos\t\t', tipos)

    # HABILIDADES
    # Las habilidades están en los divs con clase "panel-cristal"
    tabla_habilidades = tablas[1].findAll('div', class_='panel-cristal')
    # El nombre de la habildad está en el texto del elemento <a>
    habilidades_nombre = [t.findAll('a') for t in tabla_habilidades]
    habilidades_nombre = [a.text for t in habilidades_nombre for a in t]
    # La descripción de la habilidad está en el texto de un elemento
    # <div> con clase "panel-body"
    habilidades_descripcion = [t.findAll('div', class_='panel-body') for t in tabla_habilidades]
    habilidades_descripcion = [d.text for t in habilidades_descripcion for d in t]
    # print(habilidades_nombre)
    # print(habilidades_descripcion)
    habilidades = dict(zip(habilidades_nombre, habilidades_descripcion))
    print(habilidades)

    # SMOGON
    # De Smogon vamos a sacar los movimientos
    url = 'https://www.smogon.com/dex/rb/pokemon/' + pokemon_name
    print('#' * 50)
    print('Smogon')
    # MOVIMENTOS
    print('#' * 50)
    return render_template('result.html', pokemon_name=pokemon_name,
                           types=tipos, abilities=habilidades,
                           weaknesses=debilidades, resistances=resistencias,
                           immunity=tabla_inmunidad)


if __name__ == '__main__':
    app.run(debug=True)
