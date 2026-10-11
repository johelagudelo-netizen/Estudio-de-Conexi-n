# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 21:45:55 2024

@author: user
"""
def Funcion(Fichero):
    import sys
    import config_powerfactory  # ruta de PowerFactory: ver config_powerfactory.py
    import powerfactory as pf
    import pandas as pd
    app = pf.GetApplication()
    red= app.GetCalcRelevantObjects('*.ElmNet')[1]
    Folder_Caracteristicas = app.GetProjectFolder('chars')
    Cargas= pd.read_excel(Fichero, sheet_name='Cargas')
    Cargas = Cargas.dropna(axis=1, how='all')
    Circuitos=pd.read_excel(Fichero, sheet_name='Char_Tiempo')
    Circuitos = Circuitos.dropna(axis=1, how='all')
    numero_de_columnas = Circuitos.shape[1]
    Diccionario_Caracteristicas={}
    for i in range(1,numero_de_columnas):
        nombre_columna = Circuitos.columns[i]
        Diccionario_Caracteristicas[nombre_columna]=abs(Circuitos[nombre_columna]).max()

    # Se consultan las características y nodos una sola vez (antes, una búsqueda en toda la base por carga)
    Caracteristicas = config_powerfactory.indexar_por_nombre(Folder_Caracteristicas.GetContents('*.ChaTime'))
    Buses = config_powerfactory.indexar_por_nombre(app.GetCalcRelevantObjects('*.ElmTerm'))
    Contadores = {}
    for i, Carga in Cargas.iterrows():
        Tipo_Activa=Carga['Circuito_Activa']
        Tipo_Reactiva=Carga['Circuito_Reactiva']
        Pmax_Circuito=Diccionario_Caracteristicas[Tipo_Activa]
        Qmax_Circuito=Diccionario_Caracteristicas[Tipo_Reactiva]
        Cha_Activa=config_powerfactory.buscar(Caracteristicas, Tipo_Activa, 'la característica de tiempo')
        Cha_Reactiva=config_powerfactory.buscar(Caracteristicas, Tipo_Reactiva, 'la característica de tiempo')
        P_Max=Pmax_Circuito*Carga['%_Activa']
        Q_Max=Qmax_Circuito*Carga['%_Reactiva'] 
        Nueva_Carga= red.CreateObject('ElmLod', Carga['NOMBRE'])
        Nueva_Carga.plini=P_Max
        Nueva_Carga.qlini=Q_Max
        Nombre_Bus_Carga=Carga['Nodo']
        Bus_Carga=Buses.get(Nombre_Bus_Carga) if isinstance(Nombre_Bus_Carga, str) else None
        if Bus_Carga is not None:
            texto_Cub_Carga = config_powerfactory.siguiente_cubiculo(Bus_Carga, Contadores)
            Cub_Carga=Bus_Carga.CreateObject('StaCubic',texto_Cub_Carga)
            Nueva_Carga.bus1=Cub_Carga 
            refObj = Nueva_Carga.CreateObject('ChaRef','plini')
            refObj.typ_id = Cha_Activa
            refObj = Nueva_Carga.CreateObject('ChaRef','qlini')
            refObj.typ_id = Cha_Reactiva    
            

            
            
        

