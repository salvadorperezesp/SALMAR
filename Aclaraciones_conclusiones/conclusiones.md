# Conclusiones del proyecto

## Conclusión del análisis de datos

El análisis de datos ha ido tal y como se esperaba. Utilizando herramientas adquiridas en el curso de _Inteligencia Artificial y Estadística_ hemos hecho un análisis en profundidad de los datos que hemos construido.

Hemos concluido que:

- La gran mayoría de los vuelos llegan a tiempo o adelantados: Aunque la media general de retraso en las llegadas (arr_delay) es de 7.5 minutos, la mediana (el percentil 50%) es de -6 minutos. Esto significa que más de la mitad de los vuelos llega antes de lo programado. Incluso en el percentil 75%, el retraso es de apenas 10 minutos.
- Presencia de valores atípicos extremos (Outliers): El retraso máximo registrado es: 2014 minutos (más de 33 horas). Estos casos extremos son los que terminan inflando el promedio general.
- La principal causa de retraso es el Avión previo (40.6%), seguido muy de cerca por problemas imputables a la propia Aerolínea (32.2%)
- La correlación entre retraso de salida y el retraso de llegada es casi perfectaSi tu vuelo sale tarde, es prácticamente seguro que llegará tarde; el tiempo en el aire casi nunca compensa la tardanza inicial.
- La distancia no influye en el retraso: Las correlaciones entre la distancia o el tiempo de vuelo con los retrasos son prácticamente 0 (0.01 y 0.02). Un vuelo transcontinental de costa a costa no tiene más probabilidades de retrasarse que un vuelo corto regional
- Volumen de pasajeros y satisfacción: Existe una correlación alta (0.80) entre el número de pasajeros y la variable score (puntuación), lo cual suele indicar que las rutas más masivas o los aviones más grandes coinciden con mercados con dinámicas de valoración particulares, aunque no afectan al retraso directamente.
- Las peores y mejores aerolíneas: American Airlines (AA) y Frontier Airlines (F9) lideran el ranking de impuntualidad, con retrasos medios que rondan los 16 minutos.
- Julio es, de lejos, el peor mes del año tanto en retraso medio (superando los 20 minutos) como en el porcentaje de vuelos retrasados (rozando el 30%). Esto coincide con las vacaciones de verano. Diciembre y Junio también muestran picos altos. Por el contrario, Octubre y Febrero son los meses más estables y con menores retrasos.
- Los vuelos a primera hora de la mañana (5:00 AM a 8:00 AM) son los más puntuales (incluso con promedios negativos). A partir de ahí, el retraso acumulado va creciendo paulatinamente a lo largo del día hasta alcanzar su punto máximo alrededor de las 8:00 PM (20:00h).

Con esto hemos podido entender bien el corazón de nuestro dataset y de los posteriores resultados.
Una vez hemos estudio los datos, hemos podido pasar a la construcción de funciones que devuelven información relevante para el cliente como el mejor moemnto del día para volar una determinada ruta, el mejor mes... Se ha procedido a definir funciones de este tipo para proporcionar información relevante al cliente utilizando las herramientas utilizadas en la asignatura.

### Herramientas utilizadas

- Python
- R
- Matplotlib
- Seaborn
- Plotly
- Pandas
- Numpy
- Dask

## Conclusión de la parte de modelización

Aunque se han implantado numerosos modelos (KNN, RandomForest, Árboles de decisión, XGBoost, redes neuronales...) en todos se ha visto el gran problema del sesgo hacia la categoría de 'Adelantado' debido a la enorme cantidad de vuelos que caen en esa categoría. Por ello, aunque se ha implantado muchos modelos y en todos se han optimizado los parámetros con RandomGrich, en ninguno se ha conseguido llegar a los parámetros deseados ni a un accuracy apto para ser considerado un buen modelo. Debido a que, el retraso de un vuelo puede depender en gran medida a la escaleta de vuelos ese día y un efecto dominó en los retrasos y a los efectos metorólogicos, feautures que no cubren nuestro datset da lugar a que las features elegidas, aunque sean las más apropiadas para la relación cliente-web y en el contexto de nuestro proyecto no sean lo suficientemente reveladoras como para producir un buen modelo de predicción.

### Herramientas utilizadas

- KNN
- Árbol de decisión
- Random Forest
- Logistic model
- XGBoost
- Tensorflow
- Dask
