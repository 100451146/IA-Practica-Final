# Script para convertir una imagen a escala de grises

# Importar librerías
import os
import cv2
import numpy as np

# Seleccionamos la carpeta con las imágenes a cambiar
pokemon = 'MrMime' # Cambiar para cada nombre de pokemon
path = 'pokemon/'+pokemon

# Recorremos las imágenes de la carpeta y vamos aplicando el filtro
i = 0
for filename in os.listdir(path):
    # Normalizar
    img = cv2.imread(path+'/'+filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(path+'/'+pokemon+'_'+str(i)+'.png',gray)
    i += 1
    
print('Imágenes en escala de grises')