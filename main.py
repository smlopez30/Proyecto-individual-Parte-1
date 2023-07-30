import pandas as pd
import json
from fastapi import FastAPI
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from surprise import Reader, Dataset, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from typing import List
from typing import Union

# Cargar el dataset "peliculas"
peliculas = pd.read_csv('datasets/peliculas.csv')

# Crear la instancia de FastAPI
app = FastAPI()


@app.get('/peliculas_idioma/{idioma}')
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
    peliculas_filtradas.drop(columns=['title_lower'], inplace=True)

    # Verificar si se encontraron películas
    if peliculas_filtradas.empty:
        return {'pelicula': pelicula, 'peliculas_coincidentes': []}

    # Seleccionar solo las columnas de interés (nombre, duración y año)
    peliculas_coincidentes = peliculas_filtradas[['title', 'runtime', 'release_year']].to_dict(orient='records')

    return {'pelicula': peliculas_coincidentes}



@app.get('/peliculas_nombre/{pelicula}')
def peliculas_nombre(pelicula: str):
    '''Ingresas la película, retornando las películas que coinciden con el nombre'''
    # Convertir la cadena de búsqueda a minúsculas
    pelicula = pelicula.lower()

    # Convertir los títulos de las películas en el DataFrame a minúsculas
    peliculas['title_lower'] = peliculas['title'].str.lower()

    # Filtrar el DataFrame para obtener las películas que contienen la cadena ingresada
    peliculas_filtradas = peliculas[peliculas['title_lower'].str.contains(pelicula, case=False)]

    # Eliminar la columna temporal 'title_lower'
    peliculas.drop(columns=['title_lower'], inplace=True)

    # Verificar si se encontraron películas
    if peliculas_filtradas.empty:
        return {'pelicula': pelicula, 'peliculas_coincidentes': []}

    # Obtener la lista de nombres de películas que coinciden con las letras ingresadas
    peliculas_coincidentes = peliculas_filtradas['title'].tolist()

    return {'pelicula': pelicula, 'peliculas_coincidentes': peliculas_coincidentes}

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

@app.get('/get_director/{nombre_director}')
def get_director(nombre_director: str):
    ''' Se ingresa el nombre de un director que se encuentre dentro de un dataset deviendo devolver el éxito del mismo medido a través del retorno. 
    Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma. En formato lista'''

    # Convertir la cadena de búsqueda a minúsculas
    nombre_director = nombre_director.lower()

    # Filtrar el DataFrame para obtener las películas dirigidas por el director ingresado
    peliculas_director = peliculas[peliculas['director'].str.lower() == nombre_director]

    # Verificar si se encontraron películas del director
    if peliculas_director.empty:
        return {'director': nombre_director, 'mensaje': 'Director no encontrado'}

    # Calcular el éxito del director medido a través del retorno (promedio de ganancias de sus películas)
    retorno_total_director = peliculas_director['revenue'].mean()

    # Crear una lista para almacenar la información de cada película del director
    peliculas_info = []

    # Iterar sobre las películas del director y obtener la información requerida
    for _, pelicula in peliculas_director.iterrows():
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
        'director': nombre_director,
        'retorno_total_director': retorno_total_director,
        'peliculas': peliculas_info
    }

# Reemplazar valores NaN por cadenas vacías en las columnas relevantes
peliculas['franquicia'].fillna('', inplace=True)
peliculas['genres'].fillna('', inplace=True)
peliculas['idioma'].fillna('', inplace=True)
peliculas['eslogan'].fillna('', inplace=True)

# Concatenamos las características relevantes en un solo campo para el análisis TF-IDF
peliculas['combined_features'] = peliculas['franquicia'] + ' ' + peliculas['genres']

# Creamos una matriz TF-IDF con las características de todas las películas
tfidf = TfidfVectorizer(stop_words='english')
features_matrix = tfidf.fit_transform(peliculas['combined_features'].fillna(''))

# Calcular la similitud de coseno entre las características de todas las películas
cosine_sim = linear_kernel(features_matrix, features_matrix)

indices = pd.Series(peliculas.index, index=peliculas['title']).drop_duplicates()

# Definir endpoint para obtener recomendaciones de películas por características
@app.get('/recomendacion/caracteristicas/{titulo}', response_model=Union[List[str], dict])
def recommend_movies_by_features(titulo: str):
    try:
        idx = indices[indices.index == titulo].iloc[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:6]
        movie_indices = [i[0] for i in sim_scores]
        movie_titles = peliculas.iloc[movie_indices]['title'].tolist()
        return movie_titles
    except KeyError:
        return {'message': f'No se encuentra la película "{titulo}" en el conjunto de datos'}
    except IndexError:
        return {'message': f'No se pudo obtener la recomendación para la película "{titulo}"'}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
