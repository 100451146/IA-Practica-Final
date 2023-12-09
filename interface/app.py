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
clases = {0: 'Abra', 1: 'Aerodactyl', 2: 'Alakazam', 3: 'Arbok',
          4: 'Arcanine', 5: 'Articuno', 6: 'Beedrill', 7: 'Bellsprout',
          8: 'Blastoise', 9: 'Bulbasaur', 10: 'Butterfree', 11: 'Caterpie',
          12: 'Chansey', 13: 'Charizard', 14: 'Charmander', 15: 'Charmeleon',
          16: 'Clefable', 17: 'Clefairy', 18: 'Cloyster', 19: 'Cubone',
          20: 'Dewgong', 21: 'Diglett', 22: 'Ditto', 23: 'Dodrio', 24: 'Doduo',
          25: 'Dragonair', 26: 'Dragonite', 27: 'Dratini', 28: 'Drowzee',
          29: 'Dugtrio', 30: 'Eevee', 31: 'Ekans', 32: 'Electabuzz',
          33: 'Electrode', 34: 'Exeggcute', 35: 'Exeggutor', 36: 'Farfetchd',
          37: 'Fearow', 38: 'Flareon', 39: 'Gastly', 40: 'Gengar',
          41: 'Geodude', 42: 'Gloom', 43: 'Golbat', 44: 'Goldeen',
          45: 'Golduck', 46: 'Golem', 47: 'Graveler', 48: 'Greninja',
          49: 'Grimer', 50: 'Growlithe', 51: 'Gyarados', 52: 'Haunter',
          53: 'Hitmonchan', 54: 'Hitmonlee', 55: 'Horsea', 56: 'Hypno',
          57: 'Ivysaur', 58: 'Jigglypuff', 59: 'Jolteon', 60: 'Jynx',
          61: 'Kabuto', 62: 'Kabutops', 63: 'Kadabra', 64: 'Kakuna',
          65: 'Kangaskhan', 66: 'Kingler', 67: 'Koffing', 68: 'Krabby',
          69: 'Lapras', 70: 'Lickitung', 71: 'Machamp', 72: 'Machoke',
          73: 'Machop', 74: 'Magikarp', 75: 'Magmar', 76: 'Magnemite',
          77: 'Magneton', 78: 'Mankey', 79: 'Marowak', 80: 'Meowth',
          81: 'Metapod', 82: 'Mew', 83: 'Mewtwo', 84: 'Moltres', 85: 'MrMime',
          86: 'Muk', 87: 'Nidoking', 88: 'Nidoqueen', 89: 'Nidorina',
          90: 'Nidorino', 91: 'Ninetales', 92: 'Oddish', 93: 'Omanyte',
          94: 'Omastar', 95: 'Onix', 96: 'Paras', 97: 'Parasect', 98: 'Persian',
          99: 'Pidgeot', 100: 'Pidgeotto', 101: 'Pidgey', 102: 'Pikachu',
          103: 'Pinsir', 104: 'Poliwag', 105: 'Poliwhirl', 106: 'Poliwrath',
          107: 'Ponyta', 108: 'Porygon', 109: 'Primeape', 110: 'Psyduck',
          111: 'Raichu', 112: 'Rapidash', 113: 'Raticate', 114: 'Rattata',
          115: 'Rayquaza', 116: 'Rhydon', 117: 'Rhyhorn', 118: 'Sandshrew',
          119: 'Sandslash', 120: 'Scyther', 121: 'Seadra', 122: 'Seaking',
          123: 'Seel', 124: 'Shellder', 125: 'Slowbro', 126: 'Slowpoke',
          127: 'Snorlax', 128: 'Spearow', 129: 'Squirtle', 130: 'Starmie',
          131: 'Staryu', 132: 'Tangela', 133: 'Tauros', 134: 'Tentacool',
          135: 'Tentacruel', 136: 'Vaporeon', 137: 'Venomoth', 138: 'Venonat',
          139: 'Venusaur', 140: 'Victreebel', 141: 'Vileplume', 142: 'Voltorb',
          143: 'Vulpix', 144: 'Wartortle', 145: 'Weedle', 146: 'Weepinbell',
          147: 'Weezing', 148: 'Wigglytuff', 149: 'Zapdos', 150: 'Zubat'}


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

    # WIKIDEX - ANEXO: MOVIMIENTOS
    # MOVIMENTOS
    # Vamos a pedir otra página de wikidex para obtener los movimientos
    url = f'https://www.wikidex.net/wiki/Anexo:{pokemon_name}/Movimientos_por_nivel/G1'
    # url = 'https://www.smogon.com/dex/rb/pokemon/' + pokemon_name.lower()
    print('#' * 50)
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    # Seleccionamos los 4 ultimos elementos de la tabla de clase "movnivel"
    tabla_mov = soup.findAll('table', class_='movnivel')
    tabla_mov = [m.findAll('tr') for m in tabla_mov][-1][-4:]
    # En cada fila hay 3 elementos <td>, el primero es el nivel, el segundo
    # es el nombre del movimiento y el tercero es el tipo
    tabla_mov = [m.findAll('td') for m in tabla_mov]
    tabla_mov = [[m[0].text.strip(), m[1].text.strip(), m[2].find('a')['title']] for m in tabla_mov]
    tabla_mov = [f"Nivel {m[0]}: {m[1]} ({m[2]})" for m in tabla_mov]
    print('movimientos\t', tabla_mov)
    print('#' * 50)
    return render_template('result.html', pokemon_name=pokemon_name,
                           types=tipos, abilities=habilidades,
                           weaknesses=debilidades, resistances=resistencias,
                           immunity=tabla_inmunidad, moves=tabla_mov)


if __name__ == '__main__':
    app.run(debug=True)
