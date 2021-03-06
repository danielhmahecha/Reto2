"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """


import config as cf
from ADT import list as lt
from ADT import map as map
from DataStructures import listiterator as it


"""
Se define la estructura de un catálogo de libros.
El catálogo tendrá tres listas, una para libros, otra para autores 
y otra para géneros
"""

# Construccion de modelos

def newCatalog():
    """
    Inicializa el catálogo de peliculas. Retorna el catalogo inicializado.
    """
   
    catalog = {'moviesList':None, 'directors':None, 'moviesMap': None}
    #catalog['moviesList'] = lt.newList("ARRAY_LIST")
    
    #MAPAS PARA ARCHIVOS GRANDES:
    catalog['moviesMap'] = map.newMap (164531, maptype='CHAINING')#329044 movies-bigfile
    catalog['directors'] = map.newMap (171863, maptype='PROBING') #85929 directors-bigfile
    catalog['actors'] = map.newMap (130439, maptype='CHAINING') #260862 actors big-file
    catalog['titlesMap'] = map.newMap (164531, maptype='CHAINING') #329044 titles big-file
    catalog['id_directorMap'] = map.newMap (164531, maptype= 'CHAINING') #329044 ids big-file
    

    #MAPAS PARA ARCHIVOS PEQUEÑOS:
    #catalog['moviesMap'] = map.newMap (1009, maptype='CHAINING')#2000 movies-smallfile
    #catalog['directors'] = map.newMap (4001, maptype='PROBING') #2000 directors-smallfile
    #catalog['actors'] = map.newMap (2417, maptype='CHAINING') #4833 actors small-file
    #catalog['titlesMap'] = map.newMap (4001, maptype='PROBING') #2000 titles small-file
    #catalog['id_directorMap'] = map.newMap (4001, maptype= 'PROBING') #2000 ids small-file

    #MAPA GENER0S (IGUAL PARA ARCHIVOS GRANDES Y PEQUEÑOS):
    catalog['genres'] = map.newMap(41, maptype='PROBING') #20 genres
    return catalog

def addGenre (catalog, row):
    genres = catalog['genres']
    gen = ['Adventure','Crime','Animation','History','Action','TV Movie','War','Fantasy','Romance','Thriller','Music','Horror','Documentary','Science Fiction','Family','Comedy','Drama','Western','Mystery','Foreign']
    for g in gen:
        
        if g in row['genres']:
            genre = map.get(genres,g,compareByKey)
            if genre:
                lt.addLast(genre['genreMovies'],row['id'])
            else:
                newgenre = newGenre (g,row)
                map.put(genres,newgenre['genre'],newgenre,compareByKey)

def newGenre(g,row):
    newgenre = {'genre':"", 'genreMovies':None}
    newgenre['genre']=g
    newgenre['genreMovies']=lt.newList()
    lt.addLast(newgenre['genreMovies'],row['id'])
    return newgenre
    

def newMovie(row):

    movie = {"id": row['id'], "genres": row['genres'], "title": row['title'], "vote_average": row['vote_average'], "vote_count": row['vote_count']}
    return movie

def addMovieList (catalog, row):
    """
    Adiciona la pelicula a una lista
    """
    movies = catalog['moviesList']
    movie = newMovie(row)
    lt.addLast (movies, movie)

def addMovieMap(catalog, row):
    """
    Adicion la pelicula al map con key=id
    """
    movies = catalog['moviesMap']
    movie = newMovie(row)
    map.put(movies, movie['id'], movie, compareByKey)

def addTitlesMap(catalog, row):
    titles = catalog['titlesMap']
    title = newMovie(row)
    map.put(titles, title['title'], title, compareByKey)

def addId_Director(catalog, row):
    ids = catalog['id_directorMap']
    id_director = newIdDirector(row)
    map.put(ids, id_director['id'], id_director['name'], compareByKey )

def newIdDirector (row):
    id_director = {'id':"",'name':""}
    id_director['name'] = row['director_name']
    id_director['id'] = row['id']
    return id_director

def newDirector (row):
    """
    Crea una nueva estructura para modelar un director y sus películas
    """
    director = {'name':"", "directorMovies":None}
    director ['name'] = row['director_name']
    director ['directorMovies'] = lt.newList('SINGLE_LINKED')
    lt.addLast(director['directorMovies'],row['id'])
    return director

def newActor (row, actnumber):
    
    actor = {'name': "", "actorMovies":None}
    actor ['name'] = row[actnumber]
    actor['actorMovies'] = lt.newList()
    lt.addLast(actor['actorMovies'],row['id'])

    return actor

def addActor (catalog,row):
    actors = catalog['actors']

    actor1=map.get(actors, row['actor1_name'], compareByKey)
    if actor1:
        lt.addLast(actor1['actorMovies'],row['id'])

    else:
        actor1 = newActor(row,'actor1_name')
        map.put(actors,actor1['name'],actor1,compareByKey)

    actor2=map.get(actors, row['actor2_name'], compareByKey)
    if actor2:
        lt.addLast(actor2['actorMovies'],row['id'])
    else:
        actor2 = newActor(row,'actor2_name')
        map.put(actors,actor2['name'],actor2,compareByKey)
    
    actor3=map.get(actors, row['actor3_name'], compareByKey)
    if actor3:
        lt.addLast(actor3['actorMovies'],row['id'])
    else:
        actor3 = newActor(row,'actor3_name')
        map.put(actors,actor3['name'],actor3,compareByKey)

    actor4=map.get(actors, row['actor4_name'], compareByKey)
    if actor4:
        lt.addLast(actor4['actorMovies'],row['id'])
    else:
        actor4 = newActor(row,'actor4_name')
        map.put(actors,actor4['name'],actor4,compareByKey)

    actor5=map.get(actors, row['actor5_name'], compareByKey)
    if actor5:
        lt.addLast(actor5['actorMovies'],row['id'])
    else:
        actor5 = newActor(row,'actor5_name')
        map.put(actors,actor5['name'],actor5,compareByKey)


def addDirector (catalog, row):
    """
    Adiciona un director al map y sus peliculas
    """
    #if name:
    directors = catalog['directors']
    director=map.get(directors, row['director_name'], compareByKey)
    if director:
        lt.addLast(director['directorMovies'],row['id'])
    else:
        director = newDirector(row)
        map.put(directors, director['name'], director, compareByKey)


# Funciones de consulta


def getDirectorInMap (catalog, name):
    """
    Retorna el director  desde el mapa de directores a partir del nombre (key)
    """
    return map.get(catalog['directors'], name, compareByKey)

def getActorInMap(catalog,name):
    return map.get(catalog['actors'],name,compareByKey)
    

def getMovieInMap (catalog, id):
    """
    Retorna la pelicula desde el mapa de peliculas a partir del id
    """
    return map.get(catalog['moviesMap'], id, compareByKey)

def getMovieByTitle (catalog, title):
    return map.get(catalog['titlesMap'], title, compareByKey)

def getIdDirector (catalog, id):
    return map.get(catalog['id_directorMap'], id, compareByKey)

def getGenreInMap (catalog, genre):
    return map.get(catalog['genres'],genre,compareByKey)

# Funciones de comparacion

def compareByKey (key, element):
    return  (key == element['key'] )  

def compareByName(name, element):
    return (name == element['name'])

