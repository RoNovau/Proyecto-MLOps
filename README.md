![Portada](https://d500.epimg.net/cincodias/imagenes/2020/12/31/lifestyle/1609408585_467254_1609408795_noticia_normal.jpg)

<h1 align="center">  Sistema de recomendación de peliculas </h1>

## 📋 Indice
1. [Descripcion del proyecto](#descripcion)
2. [Flujo de Trabajo](#workflow)
3. [Extracción, transformación y carga de datos. (ETL)](#etl)
4. [Desarrollo de la API.](#api)
5. [Análisis Exploratorio de Datos (EDA).](#eda)
6. [Sistema de recomendacion.](#sist)
7. [Deployment](#deploy)
8. [Dependencias](#depen)


## 🧹 1. Descripcion del proyecto <a name="descripcion"></a>

En el presente sistema de recomendación, basado en procesos de Machine Learning, se filtra y predicen las posibles preferencias de los usuarios. El modo de funcionamiento es el siguiente: se ingresa el nombre de una película y te recomienda las similares en una lista de 5 valores.

El proyecto, que forma parte de las practicas de la academia SoyHenry, se encontrará con el ciclo de vida completo de los datos: contempla desde el tratamiento y recolección de los datos (Data Engineer) hasta el entrenamiento y mantenimiento del modelo de ML (Data Scientist), integrando ambos roles.

## 🧹 2. Flujo de trabajo <a name="workflow"></a>

El workflow del proyecto puede observarse en la siguiente imagen. El proceso completo cuenta con varias etapas, desde la Ingenieria de Datos (ETL), la creación de una API, el deployment y el tratamiento de Machine Learning asociado al EDA. A continuación se explican brevemente cada etapa.

![Workflow](src\DiagramaConceptualDelFlujoDeProcesos.png)

## 🧹 3. Extracción, transformación y carga de datos. (ETL) <a name="etl"></a>

En esta primera etapa nos encargamos de obtener el dataframe con el que se realizará todo el trabajo y se procede a limpiar los datos y dejarlos procesados para el tratamiento posterior. Puede verse el paso a paso en el siguiente [Link](/ETL.ipynb)

## 🧹 4. Desarrollo de la API. <a name="api"></a>

En la siguiente etapa, con la información obtenida y limpia, procedemos a crear una API a la cual se puede acceder con el siguiente [Link](https://movies-info-z1wd.onrender.com). La API cuenta con ciertas funcionalidades:

+ `/cantidad_filmaciones_mes/{mes}`: Devuelve la cantidad de películas estrenadas en el mes ingresado.
+ `/cantidad_filmaciones_dia{dia}`: Devuelve la cantidad de películas estrenadas en el día ingresado.
+ `/score_titulo/{titulo}`: Devuelve el año de estreño y el score del titulo ingresado.
+ `/votos_titulo/{titulo}`: Devuelve el año de estreño, la cantidad de votos y la puntuación promedio del titulo ingresado.
+ `/get_actor/{nombre_actor}`: Devuelve la cantidad de películas, el retorno y el promedio de retorno de las peliculas en las que participa el actor ingresado.
+ `/get_director/{nombre_director}`: Devuelve las películas dirigidas por el director ingresado, junto con el retorno, el presupuesto y la ganancia de cada película. 
+ `/recomendacion/{titulo}`: Genera una recomendacion de 5 peliculas, relacionada con el titulo de la pelicula ingresada, y basada en el genero y el overview. 

## 🧹 5. Análisis Exploratorio de Datos (EDA). <a name="eda"></a>

En este paso volvemos a hacer un análisis de los datos, buscando correlaciones de variables, outliers, existencia de nulos, variables claves. Realizamos graficos para comprender mejor algunos datos y wordclouds para conocer las palabras mas repetidas. A su vez, se realiza el preprocesamiento de la columna "overview" para obtener las palabras clave de mayor frecuencia en cada pelicula. Para dicha tarea se utilizan métodos de Procesamiento de lenguaje Natural y la biblioteca NLTK. Puede verse el paso a paso en el siguiente [Link](/EDA.ipynb)

## 🧹 6. Sistema de recomendacion. <a name="sist"></a>

En este paso del modelo se realiza un sistema de recomendacion, asociado al ultimo endpoint de la API. La recomendacion se encuentra basada en el género de la película ingresada y en la similitud con la información preprocesada de la columna "overview". Se creó una matriz de similitud y se enlistan las 5 recomendaciones a través del algoritmo de similitud coseno. Por una limitación de memoria y capacidad, el modelo no pudo realizarse sobre la totalidad del dataframe, sino que se tomó una muestra de 5000 registros. El criterio para seleccionarlos estuvo basado en la popularidad, siendo las peliculas con mayor popularidad las elegidas para la muestra. Esta decision se basa en la hipótesis de que las recomendaciones, por lo general, son sobre películas reconocidas. Puede verse el paso a paso en el siguiente [Link](/ml.ipynb)

## 🧹 7. Deployment <a name="deploy"></a>

El deployment de la API y del modelo de recomendacion fue realizado con Render gracias al siguiente tutorial [Link](https://github.com/HX-FNegrete/render-fastapi-tutorial)

## 🧹 8. Dependencias <a name="depen"></a>

Para este proyecto se utilizaron las siguientes librerias de Python:

- pandas
- numpy
- seaborn
- matplotlib
- sklearn
- FastAPI
- Uvicorn
- wordcloud
- datetime
- nltk






