# Dada una carpeta con archivos, este script cambia el nombre de los archivos de la carpeta.

# Importar librerías
import os

# Seleccionamos la carpeta con las imágenes a normalizar
pokemon = 'Snorlax'  # Cambiar para cada nombre de pokemon
path = 'pokemon/'+pokemon

# Recorremos las imágenes de la carpeta y vamos cambiando el nombre
i = 0
for filename in os.listdir(path):
    os.rename(path+'/'+filename, path+'/'+pokemon+'_'+str(i)+'.png')
    i += 1

print('Nombres cambiados')
