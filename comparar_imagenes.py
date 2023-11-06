from PIL import Image
import os

# Ruta de la carpeta con las imágenes
carpeta = 'pokemon/Pikachu'

# Diccionario para almacenar las imágenes idénticas
imagenes_ident = {}

# Recorriendo la carpeta y comparando cada imagen con las demás
for nombre_imagen1 in os.listdir(carpeta):
    ruta_imagen1 = os.path.join(carpeta, nombre_imagen1)
    if os.path.isfile(ruta_imagen1):
        imagen1 = Image.open(ruta_imagen1)
        for nombre_imagen2 in os.listdir(carpeta):
            ruta_imagen2 = os.path.join(carpeta, nombre_imagen2)
            if os.path.isfile(ruta_imagen2) and ruta_imagen1 != ruta_imagen2:
                imagen2 = Image.open(ruta_imagen2)
                if imagen1.size == imagen2.size and list(imagen1.getdata()) == list(imagen2.getdata()):
                    if nombre_imagen1 not in imagenes_ident:
                        imagenes_ident[nombre_imagen1] = [nombre_imagen2]
                    else:
                        imagenes_ident[nombre_imagen1].append(nombre_imagen2)

# Mostrar las imágenes idénticas encontradas
for imagen, imagenes_iguales in imagenes_ident.items():
    print(f"La imagen {imagen} es idéntica a: {', '.join(imagenes_iguales)}")
    
# Sacamos la imagen duplicada de la carpeta y la movemos a otra carpeta, dejando solamente una copia de la imagen
for imagen, imagenes_iguales in imagenes_ident.items():
    # si no existe la carpeta la creamos
    if not os.path.exists('pokemon/duplicadas'):
        os.makedirs('pokemon/duplicadas')
    # movemos la imagen a la carpeta duplicadas
    os.rename(carpeta + '/' + imagen, 'pokemon/duplicadas/' + imagen)
    # borramos las imagenes duplicadas
    for imagen_duplicada in imagenes_iguales:
        os.remove(carpeta + '/' + imagen_duplicada)
     
    
# Si no hay imágenes idénticas, mostrar un mensaje
if len(imagenes_ident) == 0:
    print("No hay imágenes idénticas.")

