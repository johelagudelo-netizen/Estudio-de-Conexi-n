# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 16:51:19 2024

@author: user
"""
def Funcion(Fichero):
    import sys
    import config_powerfactory  # ruta de PowerFactory: ver config_powerfactory.py
    import powerfactory as pf
    import pandas as pd
    app = pf.GetApplication()
    red= app.GetCalcRelevantObjects('*.ElmNet')[1]
    Nodos= pd.read_excel(Fichero, sheet_name='Nodos')
    Nodos = Nodos.dropna(axis=1, how='all')

    from pyproj import Proj, transform

    # Definir la proyección de origen y destino
    proyeccion_origen = Proj(init='epsg:3116')  # Mangas-Sirgas Origen Nacional
    proyeccion_destino = Proj(init='epsg:4326')  # Latitud y Longitud (WGS84)




    for i, Nodo in Nodos.iterrows():
        Nombre=Nodo['Nombre']
        Nuevo_Nodo= red.CreateObject('ElmTerm', Nombre)
        Nuevo_Nodo.uknom=Nodo['Tensión']
        # Coordenadas (X, Y) en Mangas-Sirgas Origen Nacional
        x_origen = Nodo['Cordenada X']
        y_origen = Nodo['Cordenada Y'] 

        # Convertir las coordenadas
        longitud, latitud = transform(proyeccion_origen, proyeccion_destino, x_origen, y_origen)
        Nuevo_Nodo.GPSlon=longitud
        Nuevo_Nodo.GPSlat=latitud
        app.PrintPlain(Nuevo_Nodo)
        app.PrintPlain(i)