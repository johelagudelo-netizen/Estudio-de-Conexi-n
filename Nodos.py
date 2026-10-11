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

    from pyproj import Transformer

    # Origen: Magna-Sirgas Origen Nacional (EPSG:3116) -> destino: lat/long WGS84 (EPSG:4326)
    # always_xy=True entrega (longitud, latitud); se convierten todas las filas en una sola llamada.
    conversor = Transformer.from_crs('EPSG:3116', 'EPSG:4326', always_xy=True)
    Longitudes, Latitudes = conversor.transform(Nodos['Cordenada X'].tolist(), Nodos['Cordenada Y'].tolist())




    for posicion, (i, Nodo) in enumerate(Nodos.iterrows()):
        Nombre=Nodo['Nombre']
        Nuevo_Nodo= red.CreateObject('ElmTerm', Nombre)
        Nuevo_Nodo.uknom=Nodo['Tensión']
        Nuevo_Nodo.GPSlon=Longitudes[posicion]
        Nuevo_Nodo.GPSlat=Latitudes[posicion]