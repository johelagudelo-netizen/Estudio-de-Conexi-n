# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 16:50:15 2024

@author: user
"""
def Funcion(Fichero):
    import sys
    import config_powerfactory  # ruta de PowerFactory: ver config_powerfactory.py
    import powerfactory as pf
    import pandas as pd
    app = pf.GetApplication()
    Lineas = pd.read_excel(Fichero, sheet_name='Líneas')
    Lineas= Lineas.dropna(axis=1, how='all')
    Folder_Tipos = app.GetProjectFolder('equip')
    red= app.GetCalcRelevantObjects('*.ElmNet')[1]
    # Se consultan los tipos y nodos una sola vez (antes se buscaban en toda la base por cada línea)
    Tipos = config_powerfactory.indexar_por_nombre(Folder_Tipos.GetContents('*.TypLne'))
    Buses = config_powerfactory.indexar_por_nombre(app.GetCalcRelevantObjects('*.ElmTerm'))
    Contadores = {}
    for i, Linea in Lineas.iterrows():
        Tipo=Linea['CONDUCTOR']
        Tipo_Linea=config_powerfactory.buscar(Tipos, str(Tipo), 'el tipo de línea')
        Nueva_Linea= red.CreateObject('ElmLne', Linea['NOMBRE'])
        Nueva_Linea.dline=Linea['LONGITUD']/1000
        Nueva_Linea.typ_id=Tipo_Linea
        Bus1=config_powerfactory.buscar(Buses, str(Linea['NODO1']), 'el nodo')
        Bus2=config_powerfactory.buscar(Buses, str(Linea['NODO2']), 'el nodo')
        texto1 = config_powerfactory.siguiente_cubiculo(Bus1, Contadores)
        texto2 = config_powerfactory.siguiente_cubiculo(Bus2, Contadores)
        Cub1_Linea=Bus1.CreateObject('StaCubic',texto1)
        Cub2_Linea=Bus2.CreateObject('StaCubic',texto2)
        Nueva_Linea.bus1=Cub1_Linea
        Nueva_Linea.bus2=Cub2_Linea
    app.PrintPlain('Lineas Creadas')

