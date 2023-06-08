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
    
    cantidad_total= 0

    for i in df_total['release_date']:
        if type(i) == str:
            continue
        if i.month == mes_elegido:
            cantidad_total+=1

    return "{cantidad} peliculas fueron estrenadas en el mes de {mes}"\
            .format(cantidad = cantidad_total, mes = Mes)


#Segundo endpoint: dia

@app.get("/dia/{Dia}")
async def cantidad_filmaciones_dia(Dia):
    
    dias= ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
    dia_elegido= ((dias.index(Dia)))
    
    cantidad_total= 0

    for i in df_total['release_date']:
        if type(i) == str:
            continue
        if i.weekday() == dia_elegido:
            cantidad_total+=1

    return "{cantidad} peliculas fueron estrenadas los dias {dia}"\
            .format(cantidad = cantidad_total, dia = Dia)


#Tercer endpoint: popularidad

@app.get("/popularidad/{titulo}")
def score_titulo(titulo_de_la_filmacion):
    
    titulo= titulo_de_la_filmacion

    for i in range(len(df_total)):

        if df_total.iloc[i]['title'] == titulo:
            
            año= df_total.iloc[i]['release_year']
            score = df_total.iloc[i]['popularity']
            
            return "La pelicula {titulo} fue estrenada en el año {año} "\
                   "con un score/popularidad de {score}"\
                    .format(titulo = titulo, año = año, score = score)


#Cuarto endpoint: votos

@app.get("/votos/{titulo}")
def votos_titulo(titulo_de_la_filmacion):
    titulo= titulo_de_la_filmacion

    for i in range(len(df_total)):

        año= df_total.iloc[i]['release_year']
        votos = df_total.iloc[i]['vote_count']
        promedio = df_total.iloc[i]['vote_average']

        if df_total.iloc[i]['title'] == titulo:
            
            if df_total.iloc[i]['vote_count'] < 2000:

                return "La pelicula {titulo} fue estrenada en el año {año} "\
                        "y no cuenta con valoraciones suficientes para evaluar"\
                        .format(titulo = titulo, año = año)

            else:
                
                return "La pelicula {titulo} fue estrenada en el año {año}. "\
                        "La misma cuenta con un total de {votos} valoraciones "\
                        "y con un promedio de {promedio}".format(titulo = titulo, año = 
                        año, votos= votos, promedio= promedio)


#Quinto endpoint: actor

@app.get("/actor/{nombre_actor}")
def get_actor(nombre_actor):
    
    actor= nombre_actor
    cantidad_peliculas= 0
    retorno_total= 0

    for i in range(len(df_total)):

        if actor in (df_total.iloc[i]['actors_names']):
            
            cantidad_peliculas +=1
            retorno_total+= df_total.iloc[i]['return']
        
    promedio_retorno= (retorno_total/cantidad_peliculas)

    return "El actor {actor} ha participado de {cantidad_peliculas} "\
            "filmaciones, el mismo ha conseguido un retorno "\
            "de {retorno_total} con un promedio de {promedio} por filmacion."\
            .format(actor = actor, cantidad_peliculas = cantidad_peliculas, 
                    retorno_total= round(retorno_total, 2), promedio= round(promedio_retorno,2))


#Sexto endpoint: director

@app.get("/director/{nombre_director}")

def get_director(nombre_director):
    
    director= nombre_director
    datos= df_total[df_total['directors_names'].str.contains('John Lasseter')].reset_index(drop=True)
    retorno_total= datos['return'].sum()
    peliculas= datos[['title', 'release_date', 'return', 'budget', 'revenue']].to_numpy().tolist()

    return f"El éxito del director {director} se pude medir por su retorno de {retorno_total:.2f}.\
 Dirigió las siguientes películas (título, fecha, retorno, presupuesto, recaudacion):", peliculas