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
import sys
import controller 
import csv
from ADT import list as lt
from ADT import map as map

from DataStructures import listiterator as it

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones  y  por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def printMenu():
    print("Bienvenido al Reto 2")
    print("1- Cargar información")
    print("2- Buscar buenas películas por director")
    print("3- Buscar película por título (Req. 2)")
    print("4- Buscar información por director (Req. 3)")
    print("5- Buscar información por actor (Req. 4)")
    print("6- Buscar información por genero (Req. 5) ")
    print("0- Salir")


def initCatalog ():
    """
    Inicializa el catalogo de peliculas
    """
    return controller.initCatalog()


def loadData (catalog):
    """
    Carga las peliculas en la estructura de datos
    """
    controller.loadData(catalog)


def printBestMoviesDirector (movies, criteria):
    size = lt.size(movies)

    if size:
        print ('El director tiene  '+str(size)+' películas con puntaje promedio igual o mayor a  '+str(criteria)+": ")
        iterator = it.newIterator(movies)
        while  it.hasNext(iterator):
            movie = it.next(iterator)
            print ('Titulo: ' + movie['title'] +  ' Rating: ' + movie['vote_average'] + ' (' + movie['vote_count'] + ' votos)')
    else:
        print ('No se encontraron peliculas')
    print ('\n')

def printTitlesDirector (movies):
    size = lt.size(movies)

    if size:
        print ('El director tiene las siguientes películas: ')
        iterator = it.newIterator(movies)
        while  it.hasNext(iterator):
            movie = it.next(iterator)
            print ('Titulo: ' + movie['title'] +  ' Rating: ' + movie['vote_average'] + ' (' + movie['vote_count'] + ' votos)')
    else:
        print ('No se encontraron peliculas')
    print ('\n')
"""
Menu principal
"""
while True:
    
    printMenu()
    inputs =input('Seleccione una opción para continuar\n')
    if int(inputs[0])==1:
        print("Cargando información de los archivos ....")
        catalog = initCatalog ()
        loadData (catalog)
        print ('Mapa Peliculas cargadas: ' + str(map.size(catalog['moviesMap'])))
        #print ('Lista Peliculas cargadas: ' + str(lt.size(catalog['moviesList'])))
        print ('Directores cargados: ' + str(map.size(catalog['directors'])))
        print ('Actores cargados: '+str(map.size(catalog['actors'])))
        print ('Generos cargados: '+str(map.size(catalog['genres'])))
        print ('Mapa Titulos: ' + str(map.size(catalog['titlesMap'])))
        print ('Mapa Ids Directores: ' +  str(map.size(catalog['id_directorMap']))+"\n")

    elif int(inputs[0])==2:
        
        try:
            catalog
            name = input("Nombre del director a buscar: ")
            director = controller.getDirectorInfo (catalog, name)
            if director:
                print("Director  encontrado:",director['name'])
                movies = controller.getMoviesByDirector(catalog, director['name'], 6)
                printBestMoviesDirector (movies, 6)
            else:
                print("Director No encontrado") 
            
        except:
            print("\n **ERROR: Cargue primero un archivo**\n")
       

    elif int(inputs[0])==3:
        try: 
            catalog
            title = input("Titulo de la pelicula: ")
            data = controller.getDataTitle(catalog, title)
            if data:
                print("Voto promedio: ",data['vote_average']," Votos totales: ", data['vote_count'], "Director: ", data['director'],"\n")
            else:
                print('Titulo no encontrado\n')           
           
        except:
            print("\n **ERROR: Cargue primero un archivo**\n")


    elif int(inputs[0])==4:
        try:
            catalog
            name = input('Ingrese el nombre del director a buscar: ')
            data = controller.getDataByDirector(catalog,name)
            if data: 
                print("Director  encontrado: ",name)
                count = lt.getElement(data,1)
                avg = lt.getElement(data,2)
                movies = lt.getElement(data,3)
                print ("Número de películas dirigidas: ",str(count)," Promedio de votos en sus películas: ",str(avg),"\n")
                printTitlesDirector(movies)
            else:
                print("Director no encontrado\n")
        except:
            print("\n **ERROR: Cargue primero un archivo**\n")

    elif int(inputs[0])==5:
        try:
            catalog
            name= input('Ingresa el nombre del actor a buscar: ')
            data = controller.getMoviesByActor(catalog, name)
            if data:
                print("Actor  encontrado: ",name)
                count = lt.getElement(data,1)
                avg = lt.getElement(data,2)
                mayor = lt.getElement(data, 3)
                movies = lt.getElement(data, 4)
                print("\nTotal de películas en las que ha participado: ",str(count)," Promedio de votos en sus películas: ",str(round(avg,2))," Director que más lo ha dirigido: ",mayor,"\n")
                printTitlesDirector(movies)
            else:
                print("Actor no encontrado\n")
        except:
            print("\n **ERROR: Cargue primero un archivo**\n")

    elif int(inputs[0])==6:
        try:
            catalog
            genre = input("Genero de peliculas : ")
            data = controller.getMoviesbyGenre(catalog,genre)
            if data:
                avg = lt.getElement(data,1)
                count = lt.getElement(data,2)
                print("Voto promedio: ",str(avg)," Peliculas totales: ", str(count),"\n")
            else:
                print('Genero no encontrado\n') 
        except:
            print("\n **ERROR: Cargue primero un archivo**\n")

          

    else:
        sys.exit(0)
sys.exit(0)