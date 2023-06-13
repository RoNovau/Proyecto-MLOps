from fastapi import FastAPI
import pandas as pd
import numpy as np
import datetime
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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
@app.get("/cantidad_filmaciones_mes/{mes}")
async def cantidad_filmaciones_mes(mes):

    '''Se ingresa el mes y la funcion retorna la cantidad de peliculas que se estrenaron ese mes historicamente'''

    meses= ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', \
            'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
    

    if mes not in meses:
        return {'error': f'El mes: {mes} no se encontro.'}
    
    else:
        mes_elegido= ((meses.index(mes.lower()))+1)
    
        cantidad= 0

        for i in df_total['release_date']:
            if i.month == mes_elegido:
                cantidad+=1

        return {'mes':mes, 'cantidad':cantidad}
    


#Segundo endpoint: dia

@app.get("/cantidad_filmaciones_dia/{dia}")
async def cantidad_filmaciones_dia(dia):
    
    '''Se ingresa el dia y la funcion retorna la cantidad de peliculas que se estrebaron ese dia historicamente'''

    dias= ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
    
    if dia not in dias:
        return {'error': f'El dia: {dia} no se encontro'}
    
    else:
        dia_elegido= (dias.index(dia.lower()))
        
        cantidad= 0

        for i in df_total['release_date']:
            if i.weekday() == dia_elegido:
                cantidad+=1

            return {'dia':dia, 'cantidad':cantidad}
        

#Tercer endpoint: popularidad

@app.get("/score_titulo/{titulo}")
async def score_titulo(titulo):
    
    '''Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score'''

    datos= df_total[df_total['title'] == titulo]
    anio= datos['release_year'].values[0]
    score= round(datos['popularity'].values[0],2)

    if datos.shape[0] > 0:    
        return {'titulo':titulo, 'anio': f'{anio}', 'popularidad': f'{score}'}

    else:
        return {'error': f'La pelicula {titulo} no se encontro'}

#Cuarto endpoint: votos

@app.get("/votos_titulo/{titulo}")
async def votos_titulo(titulo):

    '''Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos 
    y el valor promedio de las votaciones. La misma variable deberá de contar con al menos 2000 valoraciones, 
    caso contrario, debemos contar con un mensaje avisando que no cumple esta condición y que no se devuelve ningun valor.'''


    datos= df_total[df_total['title'] == titulo]
    votos= datos['vote_count'].values[0]
    promedio= datos['vote_average'].values[0]
    anio= datos['release_year'].values[0]

    if votos < 2000:
        
        return f"La pelicula {titulo} no cuenta con valoraciones suficientes para evaluar"
    
    else:
        
        return {'titulo':titulo, 'anio': f'{anio}', 'voto_total': 
                f'{votos}', 'voto_promedio':f'{promedio}'}


#Quinto endpoint: actor

@app.get("/get_actor/{nombre_actor}")
async def get_actor(nombre_actor):

    '''Se ingresa el nombre de un actor que se encuentre dentro de un dataset debiendo devolver el éxito del mismo
      medido a través del retorno. Además, la cantidad de películas que en las que ha participado y el promedio de retorno'''
    
    actor= nombre_actor
    datos = df_total[df_total['actors_name'].str.contains(actor)]
    cantidad= datos.shape[0]
    retorno_total= datos['return'].sum()
    promedio= retorno_total / cantidad


    if datos.shape[0] > 0:
        return {'actor':actor, 'cantidad_filmaciones': f'{cantidad}', 
            'retorno_total': f'{round(retorno_total,2)}', 
            'retorno_promedio': f'{round(promedio,2)}'}
    
    else:
        return {'error': f'El actor {actor} no se encontro'}


#Sexto endpoint: director

@app.get("/get_director/{nombre_director}")

async def get_director(nombre_director):
    
    ''' Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver 
    el éxito del mismo medido a través del retorno. Además, deberá devolver el nombre de cada película 
    con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.'''

    director= nombre_director
    datos= df_total[df_total['directors_names'].str.contains(director)].reset_index(drop=True)
    retorno_total= datos['return'].sum()
    titles= datos['title'].to_numpy().tolist()
    years= datos['release_year'].to_numpy().tolist()
    returns= datos['return'].to_numpy().tolist()
    budget= datos['budget'].to_numpy().tolist()
    revenue= datos['revenue'].to_numpy().tolist()

    if datos.shape[0] > 0:
        return {'director':director, 'retorno_total_director':retorno_total, 
            'peliculas': titles, 'anio':years, 'retorno_pelicula':returns, 
            'budget_pelicula':budget, 'revenue_pelicula':revenue}
    
    else:
        return {'error': f'El director {director} no se encontro'}


# lectura del csv que alimenta el modelo de machine learning
df_modelo= pd.read_csv('modelo.csv')

# creacion de la matriz 
count= CountVectorizer(analyzer= 'word', ngram_range= (1,2), min_df = 0, stop_words= 'english')
count_matrix = count.fit_transform(df_modelo['info'])

#creacion de la matriz de similitud
cosine_sim = cosine_similarity(count_matrix, count_matrix)

#creacion variables titulos e indices
titles= df_modelo['title']
indices= pd.Series(df_modelo.index, index=df_modelo['title'])


#Septimo endpoint: recomendacion

@app.get("/recomendacion/{titulo}")

def recommendacion(titulo):

    '''Ingresas un nombre de pelicula y te recomienda las similares en una lista'''

    idx= indices[titulo]
    sim_scores = list(enumerate(cosine_sim[idx][0]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores= sim_scores[1:31]
    movie_indices= [i[0] for i in sim_scores]

    if sim_scores != []:

        return {'Lista recomendada' : titles.iloc[movie_indices].head().tolist()}
    
    else:

        return {'error': f'La pelicula {titulo} no se encontro'}