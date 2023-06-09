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

    return {'mes':Mes, 'cantidad':cantidad}


#Segundo endpoint: dia

@app.get("/dia/{Dia}")
async def cantidad_filmaciones_dia(Dia):
    
    dias= ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
    dia_elegido= ((dias.index(Dia)))
    
    cantidad= 0

    for i in df_total['release_date']:
        if i.weekday() == dia_elegido:
            cantidad+=1

    return {'dia':Dia, 'cantidad':cantidad}


#Tercer endpoint: popularidad

@app.get("/popularidad/{titulo}")
async def score_titulo(titulo_de_la_filmacion):
    
    titulo= titulo_de_la_filmacion
    datos= df_total[df_total['title'] == titulo]
    anio= datos['release_year'][0]
    score= datos['popularity'][0]
            
    return {'titulo':titulo, 'anio':anio, 'popularidad': round(score,2)}


#Cuarto endpoint: votos

@app.get("/votos/{titulo}")
async def votos_titulo(titulo_de_la_filmacion):

    titulo= titulo_de_la_filmacion
    datos= df_total[df_total['title'] == titulo]
    votos= datos['vote_count'][0]
    promedio= datos['vote_average'][0]
    anio= datos['release_year'][0]

    if votos < 2000:
        
        return f"La pelicula {titulo} no cuenta con valoraciones suficientes para evaluar"
    
    else:
        
        return {'titulo':titulo, 'anio':anio, 'voto_total':votos, 'voto_promedio':promedio}


#Quinto endpoint: actor

@app.get("/actor/{nombre_actor}")
async def get_actor(nombre_actor):

    actor= nombre_actor
    datos = df_total[df_total['actors_names'].str.contains(nombre_actor)]
    cantidad= datos.shape[0]
    retorno_total= datos['return'].sum()
    promedio= retorno_total / cantidad

    return {'actor':actor, 'cantidad_filmaciones':cantidad, 
            'retorno_total': round(retorno_total,2), 
            'retorno_promedio': round(promedio,2)}


#Sexto endpoint: director

@app.get("/director/{nombre_director}")

async def get_director(nombre_director):
    
    director= nombre_director
    datos= df_total[df_total['directors_names'].str.contains(nombre_director)].reset_index(drop=True)
    retorno_total= datos['return'].sum()
    #peliculas= datos[['title', 'release_date', 'return', 'budget', 'revenue']].to_numpy().tolist()

    return {'director':director, 'retorno_total_director':retorno_total, 
            'peliculas':datos['title'][0], 'anio':datos['release_year'][0], 
            'retorno_pelicula':datos['return'][0], 'budget_pelicula':
            datos['budget'][0], 'revenue_pelicula':datos['revenue'][0]}