# Este archivo contiene la implementacion del backend:
# - Recibe la imagen de entrada
# - Pasa la imagen por el modelo
# - Devuelve la categoria de la imagen

# Para las peticiones HTTP
from flask import Flask, request, render_template

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
        return render_template('result.html', prediccion=pokemon_predicho)

    if request.method == 'GET':
        print(request)
        # Mostramos el formulario HTML de subida de imagen
        return render_template('main.html')

    return render_template('main.html')


if __name__ == '__main__':
    app.run(debug=True)
