# Grupo 7 - Práctica Final de Inteligencia Artificial en las Organizaciones
## Aplicación de CNN para reconocimiento de Pokémon y generación de una interfaz explicativa

### 1. Generar el modelo
El modelo se genera con el cuadernillo de Python `Desarrollo_Practica.ipynb`.  
Los pasos a seguir están explicados en el propio cuaderno.

### 2. Ejecutar la aplicación web
- Prerrequisistos  
    La aplicación requiere de ciertas librerías de Python para funcionar.
  Estas se pueden instalar con el siguiente comando:
    ```
    pip install Flask BeautifulSoup requests numpy cv2 tensorflow PIL
    ```

    Para que la aplicación funcione, el modelo que se quiera usar debe estar en la ruta ```modelo/modelo.hdf5```

- Ejecutar la aplicación web

  Desde el directorio ```interface/``` ejecutar la aplicación con:
  ```
  python3 app.py
  ```

  La aplicación se ejecutará en ```localhost:5000```
