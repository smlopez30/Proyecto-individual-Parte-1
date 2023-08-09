import pandas as pd
from fastapi import FastAPI, Query
from typing import List, Union
import ast

description = """
Este sistema permite realizar diversas consultas sobre películas, actores y directores, y, además, es posible
solicitar recomendaciones a partir de una película en particular. 🚀
El trabajo completo los pueden encontrar en Github: https://github.com/smlopez30/Proyecto-individual-Parte-1
"""

app = FastAPI(title="Sistema de Recomendación de Películas",
    description=description,
    version="0.0.1",
    contact={
        "nombre": "Sergio Miguel Lopez",
        "GitHub": "https://github.com/smlopez30",
        "email": "smlopez@gmail.com",
    }
)

peliculas = pd.read_csv('datasets/peliculas.csv')

peliculas['recomendacion'] = peliculas['recomendacion'].apply(ast.literal_eval)

@app.get('/peliculas_idioma/{idioma}')
def peliculas_idioma(idioma: str):
    '''Ingresas el idioma, retornando la cantidad de peliculas producidas en el mismo'''
    
    if idioma not in peliculas['idioma'].unique():
        return {'error': 'Idioma no encontrado en el conjunto de datos.'}
    
    peliculas_filtradas = peliculas[peliculas['idioma'] == idioma]

    cantidad_peliculas = len(peliculas_filtradas)

    return {'idioma': idioma, 'cantidad': cantidad_peliculas}


@app.get('/peliculas_duracion/{pelicula}')
def peliculas_duracion(pelicula: str):
    '''Ingresas la pelicula, retornando la duracion y el año de todas las películas que coinciden con el nombre'''

    pelicula = pelicula.lower()

    peliculas['title_lower'] = peliculas['title'].str.lower()

    peliculas_filtradas = peliculas[peliculas['title_lower'] == pelicula]

    peliculas.drop(columns=['title_lower'], inplace=True)

    if peliculas_filtradas.empty:
        return {'pelicula': pelicula, 'peliculas_coincidentes': []}

    peliculas_coincidentes = peliculas_filtradas[['title', 'runtime', 'release_year']].to_dict(orient='recomendacionords')

    return {'pelicula': peliculas_coincidentes}

@app.get('/franquicia/{franquicia}')
def franquicia(franquicia: str):
    '''Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio'''

    franquicia = franquicia.lower()

    peliculas_franquicia = peliculas[peliculas['franquicia'].str.lower() == franquicia]

    if peliculas_franquicia.empty:
        return {'franquicia': franquicia, 'mensaje': 'Franquicia no encontrada'}

    cantidad_peliculas = len(peliculas_franquicia)

    ganancia_total = peliculas_franquicia['revenue'].sum()

    ganancia_promedio = peliculas_franquicia['revenue'].mean()

    return {'franquicia': franquicia, 'cantidad': cantidad_peliculas, 'ganancia_total': ganancia_total, 'ganancia_promedio': ganancia_promedio}

@app.get('/peliculas_pais/{pais}')
def peliculas_pais(pais: str):
    '''Se ingresa un país (como están escritos en el dataset, no hay que traducirlos!), retornando la cantidad de peliculas producidas en el mismo.'''
   
    # Verificar si el país está en la columna 'pais'
    if not any(pais.lower() in str(x).lower() for x in peliculas['pais']):
        return f'No se encontraron datos para el país solicitado: {pais}'

    peliculas_pais = peliculas[peliculas['pais'].str.contains(pais, case=False)]

    cantidad_peliculas = len(peliculas_pais)

    return f'Se produjeron {cantidad_peliculas} películas en el país {pais}'


@app.get('/productoras_exitosas/{productora}')
def productoras_exitosas(productora: str):
    # Convierte la productora a minúsculas para la búsqueda
    productora_lower = productora.lower()
    
    # Verificar si la productora está en la columna 'productora', convirtiendo las productoras en la lista a minúsculas
    if not any(productora_lower in map(str.lower, x) for x in peliculas['productora'].apply(lambda x: x if isinstance(x, list) else [])):
        return f'No se encontraron datos para la productora solicitada: {productora}'

    peliculas_productora = peliculas[peliculas['productora'].apply(lambda x: productora_lower in map(str.lower, x) if isinstance(x, list) else False)]
    cantidad_peliculas = len(peliculas_productora)
    revenue_total = peliculas_productora['revenue'].sum()
    return f'La productora {productora} ha tenido un revenue de {revenue_total} y ha realizado {cantidad_peliculas} películas.'



@app.get('/get_director/{nombre_director}')
def get_director(nombre_director: str):
    '''Se ingresa el nombre del director, entregandote el retorno individual y las peliculas que realizo con su retorno, el budget y el renue.'''
    try:
        director_movies = peliculas[peliculas['director'].str.strip() == nombre_director.strip()]
        
        if director_movies.empty:
            return {'error': 'Director no encontrado', 'director': nombre_director}

        total_revenue = director_movies['revenue'].sum()
        total_budget = director_movies['budget'].sum()
        
        if total_budget == 0:
            director_success = None
        else:
            director_success = total_revenue / total_budget

        peliculas_info = []
        for _, pelicula in director_movies.iterrows():
            if pelicula['budget'] != 0:
                retorno_individual = pelicula['return']
            else:
                retorno_individual = None

            pelicula_info = {
                'nombre': pelicula.get('title', 'Desconocido'),
                'fecha_lanzamiento': pelicula.get('release_date', 'Desconocido'),
                'retorno_individual': retorno_individual,
                'costo_pelicula': pelicula['budget'],
                'ganancia_pelicula': pelicula['revenue']
            }
            peliculas_info.append(pelicula_info)

        return {
            'director': nombre_director,
            'retorno_total_director': director_success,
            'peliculas': peliculas_info
        }
    except Exception as e:
        return {'error': str(e), 'director': nombre_director}


    
@app.get('/recomendacion/{titulo}', response_model=List[str])
def recomendacion(titulo: str):
    '''Se ingresa el titulo de la una pelicula (en ingles), entregandote 5 titulos recomendados.'''
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


