# Predictor de Retrasos en Vuelos de EE.UU.

## Descripción del proyecto

Este proyecto ha sido elaborado como trabajo final de la asignatura _Inteligencia Artificial y Estadistica_ del doble grado de Matemáticas y Estadística de la Universidad de Sevilla por **María Juliá González** y **Salvador Pérez Espíldora**.

El principal objetivo del proyecto, bautizado SALMAR, ha sido construir distintos tipos de modelos predictivos (_Random Fores_, _KNN_ , _Árboles de Decisión_, _Modelos de Regresión logística_...) para la clasificación de posibles retrasos en vuelos de Estados Unidos. El proyecto abarca tanto modelos de predicción logística para observar la probabilidad de que un vuelo se retrase debido a motivos de gestión como modelos de clasificación. A su vez, la clasificación tiene como objetivo diagnosticar cuando un vuelo se retrasa, está a tiempo o llega con antelación.

Durante el proceso se han establecido tres **objetivos** diferentes:

1. **Predicción de Incidencias con IA:** Permite clasificar la probabilidad y gravedad de los retrasos antes de que ocurran, facilitando la gestión de riesgos en conexiones críticas.
2. **Optimización de Rutas e Históricos:** Identifica patrones temporales (los mejores y peores meses, días y horas para volar) analizando dinámicamente la eficiencia de los trayectos.
3. **Auditoría Corporativa:** Evalúa de forma transparente el nivel de cumplimiento y puntualidad real de cada aerolínea comercial gracias a los datos recolectados.

## Funcionamiento del proyecto

Para este proyecto se ha utilizado principalmente Python, creando el notebook principal `codigo_trabajo_final_vuelos.ipynb` que recoge toda la parte de la creación del dataset, análisis de datos y entrenamientos de modelos. Además, se han incorporado otras herramientas al proyecto como Dagster, R, Streamlit o creación de Redes Neuronales o modelos XGBoos.

El notebook `codigo_trabajo_final_vuelos.ipynb` recoge todo el proceso de modelización:

1. Análisis exploratorio de los datos de vuelos 2024.
2. Preprocesamiento y limpieza de los datos.
3. Entrenamiento de modelos: Regresión Logística, Decision Tree, XGBoost y Red Neuronal
4. Evaluación y selección del mejor modelo.
5. Exportación de los modelos `.pkl` usados por la web

Nuestra aplicación SALMAR resuelve una serie de problemas que están a la orden del día en el ámbito de viajar en avión:

1. **Mitiga la Incertidumbre del Viaje**: En lugar de comprar un billete a ciegas, el usuario puede introducir los datos de su próximo vuelo (origen, destino, hora, mes...) y el simulador predice si el vuelo tiene una alta o baja probabilidad de retrasarse por motivos de la aerolínea. Esto resuelve el problema de la falta de previsión y ayuda a tomar decisiones informadas antes de viajar.

2. **Optimiza la Planificación del Pasajero**: Muchas veces los usuarios no saben qué día o a qué hora es más seguro volar para evitar colapsos en los aeropuertos. Nuestra aplicación resuelve esto analizando el histórico de las rutas para extraer con herramientas informáticas y estadísticas el mejor mes, el mejor día y la mejor hora para volar, permitiendo al usuario diseñar el itinerario con el menor riesgo posible de quedarse atrapado.

3. **Proporciona ayuda a la hora de elegir compañía para volar** : Las compañías aéreas no siempre muestran sus datos reales de puntualidad de forma clara. Esta aplicación resuelve ese problema permitiendo al usuario hacer una "auditoría" a cada aerolínea, calculando su tiempo de retraso medio, el porcentaje de vuelos retrasados al año y mostrando un gráfico interactivo con el detalle mensual para descubrir en qué épocas del año la compañía es menos eficiente.

## Instrucciones para crear el entorno:

uv venv --python 3.11
uv sync
streamlit run main.py

## Instalar las dependencias

Todas las depenencias usadas en el proyecto han sido recopiladas en el archivo `requirements.txt` donde vienen todas las
librerías y sus respectivas versiones.

## Ejecutar la aplicación

Nuestra aplicación se ha diseñado a través de Streamlit y un archivo .py que contiene todo lo necesario para su carga.

## Tecnologías utilizadas

Para este trabajo hemos utilizado la siguiente lista de tecnologías:

- Python 3.11
- Lenguaje R
- Streamlit
- Pandas / NumPy
- Scikit-learn
- Plotly
- Siuba
- Dask
- Joblib
- XGBoost Distributed
- Dagster
