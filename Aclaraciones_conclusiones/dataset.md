# Descripción del dataset: Vuelos EEUU 2024

Nuestro proyecto usa un conjunto de datos que nace de la combinación de varios datasets, usando comandos tales como _merge_ para unificarlos.
El dataset está formado por los principales datasets:

- **Flight Delay Dataset EEUU 2024 (CSV)**. El principal y la base del resto. Conjunto de datos publicado en Kaggle que contiene infomración de vuelos de Estados Unidos durante el año 2024. Dicho dataset contiene variables tales como aeropuerto de origen , aeropuerto de salida, mes, hora, tiempo de retraso... Variables muy útiles para nuestro trabajo, por ello forma el corazón del dataset de este proyecto. Se puede encontrar en:
  `https://www.kaggle.com/datasets/hrishitpatil/flight-data-2024``

- **Información aeropuertos US (Excel)**. Un excel que contiene infomración sobre los aeropuertos de Estados Unidos. Contiene infomración como la puntuación que éste posee, las coordenadas del aeropuerto, los distintos códigos que posee dicho aeropuerto.

- **JSON con más infomración relevante de los aeropuertos**. Contiene infomración tal como el número de pasajeros medios que suele haber en el aeropuerto, el código de estos...

Como todos los datasets contienen los códigos de aeropuertos, mediante un _merge_ se enlazan dichos datasets suando los códigos de los aeropuertos de salida y completar el dataset de nuestro trabajo.

Nota: el archivo incluido en el repositorio (flight_data_2024_sample.csv) es una muestra representativa del dataset original para facilitar la reproducción del proyecto.

## Código para la unión y obtención del dataset del proyecto:

```python
vuelos_final = vuelos.merge(json1df, left_on='origin', right_on='Code', how='left') \
    .merge(df_airports, left_on='origin', right_on='local_code', how='left')
```

Importante mencionar que utilizamos un join a la izquierda puesto que nuestros datos de base es el del archivo csv y a él vamos a unirle el resto de datasets, pudiéndose dar el caso que haya filas de aeropuertos que no se encuentre en el resto de datasets.
