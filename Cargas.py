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

    for i, Carga in Cargas.iterrows():
        Tipo_Activa=Carga['Circuito_Activa']
        Tipo_Reactiva=Carga['Circuito_Reactiva']
        Pmax_Circuito=Diccionario_Caracteristicas[Tipo_Activa]
        Qmax_Circuito=Diccionario_Caracteristicas[Tipo_Reactiva]
        Cha_Activa=Folder_Caracteristicas.GetContents(Tipo_Activa + '.ChaTime')[0]
        Cha_Reactiva=Folder_Caracteristicas.GetContents(Tipo_Reactiva + '.ChaTime')[0]
        P_Max=Pmax_Circuito*Carga['%_Activa']
        Q_Max=Qmax_Circuito*Carga['%_Reactiva'] 
        Nueva_Carga= red.CreateObject('ElmLod', Carga['NOMBRE'])
        Nueva_Carga.plini=P_Max
        Nueva_Carga.qlini=Q_Max
        Nombre_Bus_Carga=Carga['Nodo']
        try:
            Bus_Carga=app.GetCalcRelevantObjects(Carga['Nodo'] + '.ElmTerm')[0]
        except:
            Bus_Carga='NaN'
        if Bus_Carga!='NaN':    
            Cubs_Carga=Bus_Carga.GetContents()
            N_Cubs_Carga=len(Cubs_Carga)
            texto_Cub_Carga = "Cub_" + str(N_Cubs_Carga+1)
            Cub_Carga=Bus_Carga.CreateObject('StaCubic',texto_Cub_Carga)
            Nueva_Carga.bus1=Cub_Carga 
            refObj = Nueva_Carga.CreateObject('ChaRef','plini')
            refObj.typ_id = Cha_Activa
            refObj = Nueva_Carga.CreateObject('ChaRef','qlini')
            app.PrintPlain(Nueva_Carga)
            refObj.typ_id = Cha_Reactiva    
            

            
            
        

