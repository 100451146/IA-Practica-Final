# Script para normalizar, redimensionar y convertir a escala de grises una carpeta de imágenes 

# Importar librerías
import os
from PIL import Image

# Seleccionamos la carpeta con las imágenes a normalizar
pokemon = 'Pikachu' # Cambiar para cada nombre de pokemon
path = 'pokemon/'+pokemon

# Recorremos las imágenes de la carpeta y vamos cambiando el tamaño
i = 0
for filename in os.listdir(path):
    # Normalizar
    img = Image.open(path+'/'+filename)
    img = img.resize((128,128))
    img.save(path+'/'+pokemon+'_'+str(i)+'.png')
    i += 1
    
print('Imágenes normalizadas')

# eliminar todos los jpg

for filename in os.listdir(path):
    if filename.endswith(".jpg"):
        os.remove(path+'/'+filename)
        
print('Imágenes jpg eliminadas')

