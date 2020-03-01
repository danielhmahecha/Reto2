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
import model
import csv
from ADT import list as lt
from ADT import map as map

from DataStructures import listiterator as it
from Sorting import mergesort as sort
from time import process_time 


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


# Funcionaes utilitarias

def printList (lst):
    iterator = it.newIterator(lst)
    while  it.hasNext(iterator):
        element = it.next(iterator)
        result = "".join(str(key) + ": " + str(value) + ",  " for key, value in element.items())
        print (result)



def compareratings (movie1, movie2):
    return ( float(movie1['vote_average']) > float(movie2['vote_average']))


# Funciones para la carga de datos 

def loadMovies (catalog, sep=';'):
    """
    Carga las películas del archivo. 
    """
    t1_start = process_time() #tiempo inicial
    moviesfile = cf.data_dir + 'themoviesdb/SmallMoviesDetailsCleaned.csv'
    #moviesfile = cf.data_dir + 'themoviesdb/AllMoviesDetailsCleaned.csv'
    dialect = csv.excel()
    dialect.delimiter=sep
    with open(moviesfile, encoding="utf-8-sig") as csvfile:
        spamreader = csv.DictReader(csvfile, dialect=dialect)
        for row in spamreader: 
            # Se adiciona la pelicula a la lista de peliculas
            #model.addMovieList(catalog, row)
            # Se adiciona la pelicula al mapa de peliculas (key=title)
            model.addMovieMap(catalog, row)
            model.addTitlesMap(catalog, row)
            model.addGenre(catalog,row)
    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución carga películas y géneros:",t1_stop-t1_start," segundos")   

def loadDirectors (catalog, sep=';'):
    """
    Carga los libros del archivo.  Por cada libro se toman sus autores y por 
    cada uno de ellos, se crea en la lista de autores, a dicho autor y una
    referencia al libro que se esta procesando.
    """
    t1_start = process_time() #tiempo inicial
    castingfile = cf.data_dir + 'themoviesdb/MoviesCastingRaw-small.csv'
    #castingfile = cf.data_dir + 'themoviesdb/AllMoviesCastingRaw.csv'
    dialect = csv.excel()
    dialect.delimiter=sep
    with open(castingfile, encoding="utf-8-sig") as csvfile:
        spamreader = csv.DictReader(csvfile, dialect=dialect)
        for row in spamreader: 
            # Se adiciona el director al mapa  de directores
            model.addDirector(catalog, row)
            model.addId_Director(catalog, row)
            model.addActor(catalog, row)
    

    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución carga directores y actores:",t1_stop-t1_start," segundos")   


def initCatalog ():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog



def loadData (catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    loadMovies(catalog)
    loadDirectors(catalog)

# Funciones llamadas desde la vista y enviadas al modelo

def getDataTitle (catalog, title):

    dataTitle = None
    movie = model.getMovieByTitle(catalog, title)
    if movie:
        vote_average = movie['vote_average']
        vote_count = movie['vote_count']
        id = movie['id']
        director = model.getIdDirector(catalog, id)
        dataTitle = {'vote_average': vote_average, 'vote_count': vote_count, 'director': director}

    return dataTitle

def getDirectorInfo (catalog, name):
    t1_start = process_time() 
    director = model.getDirectorInMap(catalog, name)
    t1_stop = process_time()
   # print("\nTiempo de ejecución buscar Director:",t1_stop-t1_start," segundos\n")   
    if director:
        return director
    else:
        return None   

def getMoviesByDirector(catalog, name, minavg):
    t1_start = process_time() #tiempo inicial 
    director = getDirectorInfo (catalog, name)
    movies = None

    if director: 
        ids = director['directorMovies']
        movies = lt.newList('ARRAY_LIST')
        iterator = it.newIterator(ids)
        while  it.hasNext(iterator):
            id = it.next(iterator)
            movie = getMovieInfo (catalog, id)
            if float(movie['vote_average']) >= minavg:
                lt.addLast(movies,movie)
            
 
    
    t1_stop = process_time() #tiempo final
    if (minavg>0):
        print("\nTiempo de ejecución buscar buenas peliculas por Director:",t1_stop-t1_start," segundos\n")

    return movies

def getDataByDirector(catalog, name):
    t1_start = process_time() #tiempo inicial 
    movies = getMoviesByDirector(catalog,name,0)
    data = None

    if movies:
        iterator = it.newIterator(movies)
        count = lt.size(movies)
        sum=0
        avg=0
        while it.hasNext(iterator):
            movie = it.next(iterator)
            sum += float(movie['vote_average'])
        
        if (sum > 0):
            avg = round(sum/count,2)
    
        data = lt.newList()
        lt.addLast(data,count)
        lt.addLast(data,avg)
        lt.addLast(data,movies)

    t1_stop = process_time() #tiempo final
    print("\nTiempo de ejecución buscar peliculas del Director:",t1_stop-t1_start," segundos\n")
    
    return data

def getMoviesByActor(catalog,name):
    t1_start = process_time()
    data = None
    actor = model.getActorInMap(catalog,name)
    if actor:
        ids = actor ['actorMovies']
        movies = lt.newList()
        count = lt.size(ids)
        iterator = it.newIterator(ids)
        sum=0
        avg=0
        while it.hasNext(iterator):
            id = it.next(iterator)
            movie = getMovieInfo(catalog, id)
            lt.addLast(movies,movie)
            sum += float(movie['vote_average'])

        if sum>0:
            avg = sum/count
        
        mayorDirector = principalDirector ( catalog, ids )

        data = lt.newList()
        lt.addLast(data, count)
        lt.addLast(data, avg)
        lt.addLast(data, mayorDirector)
        lt.addLast(data, movies)
    t1_stop = process_time()
    print("Tiempo ejecución búsqueda por actor: ",str(t1_stop-t1_start)," segundos")
    return data
    
def principalDirector (catalog, ids):
    iterator = it.newIterator(ids)
    dicc = {}
    while it.hasNext(iterator):
        id=it.next(iterator)  
        director = model.getIdDirector(catalog, id)
        if director in dicc:
            dicc[director] += 1
        else:
            dicc[director] = 1
   
    count = 0
    mayor = None
    
    for director in dicc:
        if (dicc[director] > count):
            count = dicc[director]
            mayor = director

    return mayor
        
def getMovieInfo(catalog, id):
    t1_start = process_time() #tiempo inicial
    #book=model.getBookInList(catalog, bookTitle)
    movie=model.getMovieInMap(catalog, id)
    t1_stop = process_time() #tiempo final
    #print("Tiempo de ejecución buscar pelicula:",t1_stop-t1_start," segundos")   
    if movie:
        return movie
    else:
        return None   

def getMoviesbyGenre(catalog,genre):
    genre_ids = model.getGenreInMap(catalog,genre)
    count = 0
    sum = 0
    iterator = it.newIterator(genre_ids)
    while it.hasNext(iterator):
        ID = it.next(iterator)
        movie = getMovieInfo(catalog, ID)
        count += 1
        sum += float(movie['vote_average'])
    data = lt.newList()
    average = round((sum/count),2)
    lt.addLast(data,average)
    lt.addLast(data,count)

    return data 




