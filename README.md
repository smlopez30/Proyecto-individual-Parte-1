[<p align=center><img src=imagenes/portada.jpg><p>](https://desarrollo-api-tm9i.onrender.com/docs)

<h1 align=center>**Proyecto Individual: Sistema de Recomendación de Películas**</h1>

Este repositorio es un proyecto individual cuyo objetivo es el desarrollo y despliegue de una API de recomendación de películas diseñada para proporcionar información diversa sobre películas, actores y directores. Ha sido construida utilizando el marco FastAPI y un conjunto de datos de películas estructurado y procesado con librerías de lenguaje Python. La API permite consultar información sobre películas, actores y directores a través de varias rutas y funcionalidades. Este proyecto fue desarrollado durante la etapa de Labs de Henry. A continuación, se describen cada una de las etapas en las que se organizó el proyecto.

**ETL**

Se realizaron algunas transformaciones a los datasets originales tales como:

+ Se eliminaron las filas integralmente duplicadas en ambos datasets y se identificaron los registros con datos inconsistentes.
+ Los valores nulos del campo **`budget`** fueron imputados con el número **`0`**. Se eliminaron los registros con valores nulos en las variables **`id`** y **`release_date`**.
+ Algunos campos tienen datos anidados por lo que se desanidaron y se extrajeron los datos necesarios. En el caso de la variable **`crew`** se extrajeron los nombres de todos los actores y para **`cast`**, se hizo lo propio con el nombre del director, creándose las variables **`actor`** y **`director`**, respectivamente.
+ Se realizó el cambio de formato en el campo **`release_date`** a **`AAAA-mm-dd`** y, posteriormente, se crearon los campos **`release_year`** y **`release_month`**, que corresponden al año y mes de estreno de cada película.
+ Se creó la columna con el retorno de inversión, llamada **`return`** como resultado de la relación entre con los campos **`revenue`** y **`budget`**. En los casos que la división no fue posible, se asignó el valor **`0`**.
+ Las columnas que no se utilizaron para en esta primera versión de la API, fueron eliminadas; a saber: **`video`**,**`imdb_id`**,**`adult`**,**`original_title`**,**`poster_path`** y **`homepage`**.
+ Los datasets fueron combinados a partir del campo **`id`**.
+ Se creó la variable **`recs`**, la cual contiene una lista de películas similares y que es utilizada por la API para el sistema de recomendación. La similaridad entre películas fue calculada a partir de una matriz de similaridad coseno utilizando la frecuencia de términos-frecuencia inversa del documento (**`tf-idf`**) en los campos **`title`** y **`overview`**.
+ Con la intención de volver más eficientes las consultas, se crearon datasets particulares para cada función de la API.

Estas tareas se realizaron en una [Jupyter Notebook](https://github.com/smlopez30/Proyecto-individual-Parte-1) con VSS Code y se subieron a GitHub. Se utilizaron librerías como Pandas, Numpy, Json, Matplotlib.pyplot y Scikit-learn.

por problemas de tamaño para subir el archivo credits.csv el mismo esta en el siguiente [link](https://mega.nz/file/gQ01DJQI#eUGE9q59kS4C5aiGj98xOrLPU0Jw_-D1hk-5RwkGgyg), ya que el mismo no se encuentra en Github

**`Análisis exploratorio de los datos`**: _(Exploratory Data Analysis-EDA)_

Descripción breve de algunas de las columnas:

* franquicia: La franquicia a la que pertenece la película (si aplica).
* budget: El presupuesto de la película.
* genres: Una lista de géneros asociados con la película.
* id: El ID de la película.
* idioma: El idioma principal de la película.
* overview: Una breve descripción de la trama de la película.
* popularity: Un valor que representa la popularidad de la película.
* productora: Una lista de las compañías productoras.
* pais: Una lista de los países donde se produjo la película.
* release_date: La fecha de lanzamiento de la película.
* runtime: La duración de la película en minutos.
* status: El estado de lanzamiento de la película (por ejemplo, "Released").
* eslogan: El eslogan de la película.
* title: El título de la película.
* vote_average: La calificación promedio de la película.
* vote_count: La cantidad de votos recibidos.
* return: Retorno financiero.
* release_year: El año de lanzamiento.
* cast: Una lista del elenco principal.
* director: El director de la película.

Algunas observaciones clave:

* franquicia: Solo 4485 de las 45345 filas tienen una franquicia definida. El resto tiene valores nulos (NaN).
* budget, genres, id, popularity, productora, pais, release_date, revenue, title, vote_average, vote_count, return, release_year, y cast: Estas columnas tienen 45345 valores no nulos, lo que significa que no faltan datos en estas columnas.
* idioma: Hay 45334 valores no nulos, lo que significa que hay algunos valores faltantes.
* overview: 44404 valores no nulos, lo que indica que hay algunas descripciones faltantes.
* runtime: 45099 valores no nulos, lo que sugiere que la duración de algunas películas no está disponible.
* status: 45265 valores no nulos, por lo que el estado de algunas películas puede estar faltando.
* eslogan: Solo 20387 de las 45345 filas tienen un eslogan definido.
* director: 44510 valores no nulos, lo que significa que algunos directores están faltando en los datos.

Resumen estadístico con medidas de tendencia central. 

budget: La mayoría de las películas tienen un presupuesto de 0, lo que sugiere que para muchas películas el presupuesto puede no estar disponible o no se ha introducido en la base de datos. La película con el mayor presupuesto tiene un presupuesto de 380 millones de dólares.

id: El campo de identificación varía de 2 a 469172, pero la media está alrededor de 108036.

popularity: La popularidad varía considerablemente, desde 0 hasta aproximadamente 547.49, con una media de 2.93.

revenue: Al igual que el presupuesto, la mayoría de las películas tienen unos ingresos de 0, lo que indica que puede que no se disponga de información sobre los ingresos para muchas películas. La película con los ingresos más altos ha recaudado aproximadamente 2.788 mil millones de dólares.

vote_average: La puntuación media de las votaciones es de 5.62 en una escala de 0 a 10, y la mediana es 6. Esto sugiere que la mayoría de las películas reciben calificaciones bastante positivas.

vote_count: El número de votos recibidos por las películas varía enormemente, desde 0 hasta 14075. Sin embargo, la media de votos es de 110, y la mediana es de 10, lo que indica que la mayoría de las películas reciben un número relativamente pequeño de votos.

return: Los retornos varían desde 0 hasta alrededor de 12.396 millones, con una media de 660. Pero dada la desviación estándar y el percentil 75 igual a 0, podemos deducir que muchos valores son 0 o cercanos a 0.

release_year: Las películas de la base de datos fueron lanzadas entre 1874 y 2020, con una media en 1991. Más del 75% de las películas fueron lanzadas después de 1978.

Los muchos valores de 0 en budget, revenue y return podrían indicar que falta mucha información en estos campos.

En las distribucion de peliculas por idioma vemos que la gran mayoria se hacen en idioma ingles con muy pocas en otros idomas (Esto es en base al dataset que se nos dio)

También se analizaron las nubes de palabras de **`title`**.

Análisis de las correlaciones:
budget vs revenue: Con una correlación de 0.768811, hay una fuerte correlación positiva. Esto significa que, en general, a medida que el presupuesto de una película aumenta, los ingresos que genera también lo hacen.

budget vs vote_count: Con una correlación de 0.676668, hay una correlación positiva. Esto puede interpretarse como que las películas con mayores presupuestos tienden a recibir más votos.

popularity vs revenue: Con una correlación de 0.506203, hay una correlación positiva moderada. Esto indica que las películas más populares tienden a generar más ingresos.

popularity vs vote_count: 0.559973 indica una correlación positiva moderada, lo que significa que las películas más populares tienden a recibir más votos.

revenue vs vote_count: 0.812019 muestra una fuerte correlación positiva, lo que indica que las películas que generan más ingresos también tienden a recibir más votos.

id vs budget, id vs revenue, id vs vote_count, etc.: Las correlaciones con la variable "id" son bastante bajas, lo que sugiere que el ID no tiene una fuerte relación lineal con las demás variables.

return: La columna "return" parece no tener una fuerte correlación con ninguna otra variable, ya que todos sus valores están muy cerca de 0.

release_year: Aunque hay algunas correlaciones menores, no parecen ser especialmente significativas, lo que indica que el año de lanzamiento, por sí solo, no tiene una fuerte relación lineal con las demás variables presentes.

Observaciones finales:
Las películas con mayores presupuestos tienden a generar más ingresos y a recibir más votos.
Las películas más populares tienden a generar más ingresos y a recibir más votos.
El ID de una película y su "retorno" no parecen ser buenos indicadores de ninguna de las otras variables.
Si bien el "año de lanzamiento" tiene algunas correlaciones menores, no parece ser un factor crítico en relación con las otras variables.
 

Este EDA se puede consultar en la [Jupyter Notebook](https://github.com/smlopez30/Proyecto-individual-Parte-1/blob/master/DataEingenier.ipynb). Se utilizaron librerías como Pandas, Numpy, Json, Seaborn, Matplotlib.pyplot y Wordcloud.
#API

**`Desarrollo de la API y despliegue`**

La API fue desarrollada con el entorno de trabajo [FastAPI](https://fastapi.tiangolo.com/) en lenguaje Python. Se optó por este _(web framework)_ por su buena performance y la facilidad de poder ser construido en un lenguaje sumamente difundido con Python. El [código principal](https://github.com/smlopez30/Proyecto-individual-Parte-1/blob/master/main.py) cuenta con las funciones para cada uno de los _(endpoints)_. Además, se pueden consultar las [librerías](https://github.com/smlopez30/Proyecto-individual-Parte-1/blob/master/requirements.txt) necesarias para su funcionamiento.
Para el sistema de recomendacion el sistema principal se encuentra en la [Jupyter Notebook](https://github.com/smlopez30/Proyecto-individual-Parte-1/blob/master/DataEingenier.ipynb) en la seccion "Sistema de recomendacion de peliculkas" en el cual se itera la columna peliculas y se crea una nueva columna en el dataset que guarda en forma de lista los 5 titulos sugeridos. El sistema se divide principalmente en dos parte en la primera solo toma la franquicia (si la tiene) y agrega en la columna recomendacion las demas peliculas de la franquicia. la segunda parte es la que por medio de la matriz del coseno se buscan similituddes en el titulo, el genero y la productora. encontrando los titulos con mayor similitud a esas variables y agregandolas en forma de lista en la columna recomendacion. Finalmente en el endpoint solo se pone el codigo para que levante los datos de la columna recomendacion correspondiente al tiutlo ingresado 

El despliegue (_(deployment)_) lo realicé como un _(web service)_ en la nube de [Render](https://render.com/). La configuración utilizada se puede consultar [aquí](https://github.com/HX-FNegrete/render-fastapi-tutorial.git). Esta opción resultó sumamente ágil para los fines del presente proyecto, además de contar con un plan gratuito. La documentación sobre el servicio se encuentra disponible [aquí](https://desarrollo-api-tm9i.onrender.com/docs).

Consultas disponibles de la [API](https://desarrollo-api-tm9i.onrender.com/)

+ Ingresas el idioma (en formato ISO 639-1 ), retornando la cantidad de peliculas producidas en el mismo. [link directo a la seccion idioma con el idioma "en"](https://desarrollo-api-tm9i.onrender.com/peliculas_idioma/en)

+ Ingresas el titulo pelicula (en ingles), retornando la duracion y el año de todas las películas que coinciden con el nombre. [link directo a la seccion titulo de una pelicula el nombre de "Toy Story"](https://desarrollo-api-tm9i.onrender.com/peliculas_duracion/Toy%20Story)

+ Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio. [link directo a la seccion franquicia con una la coleccion de "Toy Story" de ejemplo"](https://desarrollo-api-tm9i.onrender.com/franquicia/Toy%20Story)

+ Se ingresa un país (como están escritos en el dataset, no hay que traducirlos!), retornando la cantidad de peliculas producidas en el mismo. [link directo a la seccion pais con el nombre de "Argentina" de ejemplo](https://desarrollo-api-tm9i.onrender.com/peliculas_pais/Argentina)

+ Se ingresa la productora, entregandote el revenue total y la cantidad de peliculas que realizo. [link directo a la seccion productora con el nombre "Pixar Animation Studios" de ejemplo](https://desarrollo-api-tm9i.onrender.com/productoras_exitosas/Pixar%20Animation%20Studios)

+ Se ingresa el nombre del director, entregandote el retorno individual y las peliculas que realizo con su retorno, el budget y el renue. [link directo a la seccion director con el nombre "John Lasseter" de ejemplo](https://desarrollo-api-tm9i.onrender.com/get_director/John%20Lasseter)

+ Se ingresa el titulo de la una pelicula (en ingles), entregandote 5 titulos recomendados. Las recomendaciones se basan en el criterio detallado en la sección de **[Sistema de recomendacion de peliculas](https://github.com/smlopez30/Proyecto-individual-Parte-1/blob/master/DataEingenier.ipynb)**. /
[link directo a la seccion recomendacion con "Toy Story" de ejemplo](https://desarrollo-api-tm9i.onrender.com/recomendacion/Toy%20Story)

**`Funcionamiento`**

[Fastapi desarrolla una documentacion del deploy en la que se puden probar todos los items del proyecto](https://desarrollo-api-tm9i.onrender.com/docs)

Ademas, se encuentra disponible un [video](https://youtu.be/WY-HvTvJGx8) sobre el funcionamiento de la API mediante ejemplos de consultas.

**`Mantenimiento`**
Este proyecto está mantenido por Sergio Miguel Lopez. Si tienes alguna pregunta o encuentras algún problema, por favor, [contactame](https://www.linkedin.com/in/sergio-lopez-1149731a/).
