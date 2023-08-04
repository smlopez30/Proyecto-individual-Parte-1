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


@app.get('/get_direcomendaciontor/{nombre_direcomendaciontor}')
def get_direcomendaciontor(nombre_direcomendaciontor: str):
    ''' Se ingresa el nombre de un direcomendaciontor que se encuentre dentro de un dataset deviendo devolver el éxito del mismo medido a través del retorno.
    Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma. En formato lista'''

    # Convertir la cadena de búsqueda a minúsculas
    nombre_direcomendaciontor = nombre_direcomendaciontor.lower()

    # Filtrar el DataFrame para obtener las películas dirigidas por el direcomendaciontor ingresado
    peliculas_direcomendaciontor = peliculas[peliculas['direcomendaciontor'].str.lower() == nombre_direcomendaciontor]

    # Verificar si se encontraron películas del direcomendaciontor
    if peliculas_direcomendaciontor.empty:
        return {'direcomendaciontor': nombre_direcomendaciontor, 'mensaje': 'Direcomendaciontor no encontrado'}

    # Calcular el éxito del direcomendaciontor medido a través del retorno (promedio de ganancias de sus películas)
    retorno_total_direcomendaciontor = peliculas_direcomendaciontor['revenue'].mean()

    # Crear una lista de información de cada película del direcomendaciontor
    peliculas_info = []
    for _, pelicula in peliculas_direcomendaciontor.iterrows():
        # Verificar si el costo de la película es cero para evitar la división por cero
        if pelicula['budget'] != 0:
            retorno_individual = pelicula['revenue'] / pelicula['budget']
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
        'direcomendaciontor': nombre_direcomendaciontor,
        'retorno_total_direcomendaciontor': retorno_total_direcomendaciontor,
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


