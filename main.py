import pandas as pd
from fastapi import FastAPI, Query
from typing import List, Union
import ast



# Cargar el dataset "peliculas"
peliculas = pd.read_csv('datasets/peliculas.csv')

# Convertir el contenido de la columna 'recomendacion' en listas
peliculas['recomendacion'] = peliculas['recomendacion'].apply(ast.literal_eval)


# Crear la instancia de FastAPI
app = FastAPI()

@app.get('/peliculas_idioma/{ej. es}')
def peliculas_idioma(idioma:str):
    '''Ingresas el idioma, retornando la cantidad de peliculas producidas en el mismo'''
    
    peliculas_filtradas = peliculas[peliculas['idioma'] == idioma]

    # Contar la cantidad de películas en el idioma especificado
    cantidad_peliculas = len(peliculas_filtradas)

    return {'idioma': idioma, 'cantidad': cantidad_peliculas}

@app.get('/peliculas_duracion/{pelicula}')
def peliculas_duracion(pelicula: str):
    '''Ingresas la pelicula, retornando la duracion y el año de todas las películas que coinciden con el nombre'''

    # Convertir la cadena de búsqueda a minúsculas
    pelicula = pelicula.lower()

    # Convertir los títulos de las películas en el DataFrame a minúsculas
    peliculas['title_lower'] = peliculas['title'].str.lower()

    # Filtrar el DataFrame para obtener las películas que contienen la cadena ingresada
    peliculas_filtradas = peliculas[peliculas['title_lower'] == pelicula]

    # Eliminar la columna temporal 'title_lower'
    peliculas.drop(columns=['title_lower'], inplace=True)

    # Verificar si se encontraron películas
    if peliculas_filtradas.empty:
        return {'pelicula': pelicula, 'peliculas_coincidentes': []}

    # Seleccionar solo las columnas de interés (nombre, duración y año)
    peliculas_coincidentes = peliculas_filtradas[['title', 'runtime', 'release_year']].to_dict(orient='recomendacionords')

    return {'pelicula': peliculas_coincidentes}

@app.get('/franquicia/{franquicia}')
def franquicia(franquicia: str):
    '''Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio'''

    franquicia = franquicia.lower()

    # Filtrar el DataFrame para obtener las películas que pertenecen a la franquicia ingresada
    peliculas_franquicia = peliculas[peliculas['franquicia'].str.lower() == franquicia]

    # Verificar si se encontraron películas de la franquicia
    if peliculas_franquicia.empty:
        return {'franquicia': franquicia, 'mensaje': 'Franquicia no encontrada'}

    # Calcular la cantidad de películas de la franquicia
    cantidad_peliculas = len(peliculas_franquicia)

    # Calcular la ganancia total de la franquicia
    ganancia_total = peliculas_franquicia['revenue'].sum()

    # Calcular el promedio de ganancias de la franquicia
    ganancia_promedio = peliculas_franquicia['revenue'].mean()

    return {'franquicia': franquicia, 'cantidad': cantidad_peliculas, 'ganancia_total': ganancia_total, 'ganancia_promedio': ganancia_promedio}

@app.get('/peliculas_pais/{pais}')
def peliculas_pais(pais: str):
    '''Se ingresa un país (como están escritos en el dataset, no hay que traducirlos!), retornando la cantidad de peliculas producidas en el mismo.'''
    # Verificar si el país ingresado está presente en la columna 'pais' de cada celda
    peliculas_pais = peliculas[peliculas['pais'].str.contains(pais, case=False)]

    # Calcular la cantidad de películas en el país especificado
    cantidad_peliculas = len(peliculas_pais)

    return f'Se produjeron {cantidad_peliculas} películas en el país {pais}'

# Nueva función para obtener el revenue total y la cantidad de películas producidas por una productora específica
@app.get('/productoras_exitosas/{productora}')
def productoras_exitosas(productora: str):
    '''Se ingresa la productora, entregandote el revenue total y la cantidad de peliculas que realizo.'''
    peliculas_productora = peliculas[peliculas['productora'] == productora]
    cantidad_peliculas = len(peliculas_productora)
    revenue_total = peliculas_productora['revenue'].sum()
    return f'La productora {productora} ha tenido un revenue de {revenue_total} y ha realizado {cantidad_peliculas} películas.'


@app.get('/get_director/{director}')
def get_director(director: str):
    # Filtrar el dataset peliculas para obtener solo las películas del director dado
    director_movies = peliculas[peliculas['director'] == director]
    
    # Calcular el éxito general del director basado en la suma de revenues / suma de budgets
    total_revenue = director_movies['revenue'].sum()
    total_budget = director_movies['budget'].sum()
    
    if total_budget == 0:
        director_success = None  # O podrías manejarlo de otra manera si el total del budget es cero
    else:
        director_success = total_revenue / total_budget

    # Crear una lista de información de cada película del director
    peliculas_info = []
    for _, pelicula in director_movies.iterrows():
        # Verificar si el costo de la película es cero para evitar la división por cero
        if pelicula['budget'] != 0:
            retorno_individual = pelicula['return']
        else:
            retorno_individual = 0  # O podrías asignar otro valor predeterminado

        pelicula_info = {
            'nombre': pelicula['title'],
            'fecha_lanzamiento': pelicula['release_date'],
            'retorno_individual': retorno_individual,
            'costo_pelicula': pelicula['budget'],
            'ganancia_pelicula': pelicula['revenue']
        }
        peliculas_info.append(pelicula_info)

    return {
        'director': director,
        'retorno_total_director': director_success,
        'peliculas': peliculas_info
    }

    
@app.get('/recomendacion/{titulo}', response_model=List[str])
def recomendacion(titulo: str):
    try:
        print(f'Título ingresado: {titulo}')
        pelicula = peliculas[peliculas['title'].str.contains(titulo, case=False)]
        if not pelicula.empty:
            recomendaciones = pelicula['recomendacion'].iloc[0]
            print(f'Recomendaciones encontradas: {recomendaciones}')
            return list(recomendaciones)
        else:
            return ['Título no encontrado']
    except IndexError:
        return ['Título no encontrado']


