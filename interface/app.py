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

app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')
modelo = load_model('../modelo/modelo.hdf5')


@app.route('/', methods=['GET', 'POST'])
def subir_imagen():
    if request.method == 'POST':
        imagen = request.files['imagen']
        # Guardamos la imagen en el directorio de imagenes
        imagen.save('./imagen.jpg')
        imagen = image.load_img('./imagen.jpg', target_size=(128, 128))
        imagen_array = image.img_to_array(imagen)
        imagen_array = np.expand_dims(imagen_array, axis=0)
        prediccion = modelo.predict(imagen_array)
        prediccion = np.argmax(prediccion)
        clases = {0: 'Bulbasaur', 1: 'Caterpie', 2: 'Charizard', 3: 'Charmander', 4: 'Dragonite',
                  5: 'Eevee', 6: 'Gengar', 7: 'Geodude', 8: 'Greninja', 9: 'Jigglypuff', 10: 'Lapras',
                  11: 'Machop', 12: 'Magikarp', 13: 'Meowth', 14: "MrMime", 15: 'Pikachu', 16: 'Rattata',
                  17: 'Rayquaza', 18: 'Snorlax', 19: 'Squirtle'}
        pokemon_predicho = clases[prediccion]

        return redirect(url_for('stats_pokemon', pokemon_name=pokemon_predicho))

    if request.method == 'GET':
        print(request)
        # Mostramos el formulario HTML de subida de imagen
        return render_template('main.html')

    return render_template('main.html')


@app.route('/result/<pokemon_name>')
def stats_pokemon(pokemon_name):
    # Voy a usar wikidex porque megadexter me ha bloqueado la IP :(
    # Cogemos de la página web
    url = 'https://wikidex.net/wiki/' + pokemon_name
    # url = 'https://megadexter.com/dex/pokemon/' + pokemon_name
    pagina = requests.get(url)
    soup = BeautifulSoup(pagina.content, 'html.parser')
    print('#' * 50)
    print('Pokemon\t\t', pokemon_name)

    # TIPO y HABILIDADES
    # El tipo y las habilidades están en la tabla con clase "datos"
    tabla = soup.find('table', class_='datos')
    # El tipo está en la fila con titulo "Tipos a los que pertenece"
    # y aparece en el título de los elementos <a>, pero en el primer
    # elemento <a> solo pone "Tipo"
    tabla_tipo = tabla.find('tr', title='Tipos a los que pertenece')
    tabla_tipo = tabla_tipo.findAll('a')[1:]
    tipos = [a['title'] for a in tabla_tipo]
    print('Tipo\t\t', tipos)

    # Las habilidades están en la fila con titulo "Habilidades que puede conocer"
    # y es una lista de elementos <a> con la habilidad en el texto
    # igual saltandonos el primer elemento
    # y las habilidades ocultas están en la fila con titulo "Habilidad oculta"
    # y es un elemento <a> con la habilidad en el texto
    tabla_habilidades = tabla.find('tr', title='Habilidades que puede conocer')
    tabla_habilidades = tabla_habilidades.findAll('a')[1:]
    tabla_ocultas = tabla.find('tr', title='Habilidad oculta')
    tabla_ocultas = tabla_ocultas.findAll('a')[1:]
    habilidades = [a.text for a in tabla_habilidades]
    habilidades_ocultas = [a.text for a in tabla_ocultas]
    habilidades.extend(habilidades_ocultas)
    print('Habilidades\t', habilidades)

    # DEBILIDADES y RESISTENCIAS
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
    # Las resistencias están en las filas 4 y 5
    # y la inmunidad en la fila 6
    # En cada fila hay 3 elementos <td> y en el tercero está lo que queremos,
    # una lista de <a> con la resistencia en el titulo
    tabla_resistencias = tabla.findAll('tr')[4:6]
    tabla_resistencias = [d.findAll('td')[2] for d in tabla_resistencias]
    tabla_resistencias = [d.findAll('a') for d in tabla_resistencias]
    tabla_resistencias = [[a['title'] for a in d] for d in tabla_resistencias]
    resistencias = [s for d in tabla_resistencias for s in d]
    print('resistencias\t', resistencias)
    tabla_inmunidad = tabla.findAll('tr')[6]
    tabla_inmunidad = tabla_inmunidad.findAll('td')[2]
    tabla_inmunidad = tabla_inmunidad.findAll('a')
    tabla_inmunidad = [a['title'] for a in tabla_inmunidad]
    print('Inmunidades\t', tabla_inmunidad)

    # MOVIMIENTOS
    # La información que queremos no está en wikidex, sino en megadexter
    # pero ME HAN BLOQUEADO LA IP WTF
    print('#' * 50)
    return render_template('result.html', pokemon_name=pokemon_name,
                           types=tipos, abilities=habilidades,
                           weaknesses=debilidades, resistances=resistencias,
                           immunity=tabla_inmunidad)


if __name__ == '__main__':
    app.run(debug=True)
