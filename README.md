# (NOMBRE DE LA APP)
## Aplicación de CNN para reconocimiento de Pokémon y generación de una interfaz explicativa

### 1. Generar el modelo
El modelo se genera con el cuadernillo de python
...

### 2. Ejecutar la aplicación web
- Prerrequisistos
    ```
    pip install Flask BeautifulSoup requests
    ```

    Para que la aplicación funcione, el modelo debe estar en la ruta ```modelo/modelo.hdf5```

- Ejecutar

  Desde el directorio ```interface/``` ejecutar la aplicación con:
  ```
  python3 app.py
  ```

  La aplicación se ejecutará en ```localhost:5000```
