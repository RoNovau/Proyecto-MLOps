from fastapi import FastAPI
import pandas as pd
import numpy as np
import datetime


#Transformamos el csv limpio con todos los datos a dataframe.
df_total= pd.read_csv('proyecto1.csv', sep= ',', encoding= 'utf-8')

#Parseamos la columna release date a datetime.
df_total['release_date']= pd.to_datetime(df_total['release_date'], yearfirst=True)

#Cambie algunos valores Nan de la columna actores y directores.
df_total['directors_names'][42827] = '[]'
df_total['actors_names'][42827] = '[]'

#Instanciamos la API
app = FastAPI()

#Creamos el primer endpoint "mes"
@app.get("/mes/{Mes}")
async def cantidad_filmaciones_mes(Mes):
    
    meses= ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', \
            'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    
    mes_elegido= ((meses.index(Mes))+1)
    
    cantidad= 0

    for i in df_total['release_date']:
        if i.month == mes_elegido:
            cantidad+=1

    return f"{cantidad} peliculas fueron estrenadas en el mes de {Mes}"


#Segundo endpoint: dia

@app.get("/dia/{Dia}")
async def cantidad_filmaciones_dia(Dia):
    
    dias= ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
    dia_elegido= ((dias.index(Dia)))
    
    cantidad= 0

    for i in df_total['release_date']:
        if i.weekday() == dia_elegido:
            cantidad+=1

    return f"{cantidad} peliculas fueron estrenadas los dias {Dia}"


#Tercer endpoint: popularidad

@app.get("/popularidad/{titulo}")
async def score_titulo(titulo_de_la_filmacion):
    
    titulo= titulo_de_la_filmacion
    datos= df_total[df_total['title'] == titulo]
            
    return f"La pelicula {titulo} fue estrenada en el año {datos['release_year'][0]}\
 con un score/popularidad de {round(datos['popularity'][0],1)}"


#Cuarto endpoint: votos

@app.get("/votos/{titulo}")
async def votos_titulo(titulo_de_la_filmacion):

    titulo= titulo_de_la_filmacion
    datos= df_total[df_total['title'] == titulo]
    votos= datos['vote_count'][0]
    promedio= datos['vote_average'][0]

    if votos < 2000:
        
        return f"La pelicula {titulo} fue estrenada en el año {datos['release_year'][0]} "\
"y no cuenta con valoraciones suficientes para evaluar"
    
    else:
        
        return f"La pelicula {titulo} fue estrenada en el año \
{datos['release_year'][0]}. La misma cuenta con un total de \
{datos['vote_count'][0]} valoraciones, con un promedio de {datos['vote_average'][0]}."


#Quinto endpoint: actor

@app.get("/actor/{nombre_actor}")
async def get_actor(nombre_actor):

    actor= nombre_actor
    datos = df_total[df_total['actors_names'].str.contains(nombre_actor)]
    cantidad= datos.shape[0]
    retorno_total= datos['return'].sum()
    promedio= retorno_total / cantidad

    return f"El/la actor/actriz {actor} ha participado en {cantidad} filmaciones y ha conseguido\
un retorno de {retorno_total:.2f}, con un promedio de {round(promedio, 2)} por filmacion."


#Sexto endpoint: director

@app.get("/director/{nombre_director}")

async def get_director(nombre_director):
    
    director= nombre_director
    datos= df_total[df_total['directors_names'].str.contains(nombre_director)].reset_index(drop=True)
    retorno_total= datos['return'].sum()
    peliculas= datos[['title', 'release_date', 'return', 'budget', 'revenue']].to_numpy().tolist()

    return f"El éxito del/la director/a {director} se pude medir por su retorno de {retorno_total:.2f}.\
 Dirigió las siguientes películas (título, fecha, retorno, presupuesto, recaudacion):", peliculas