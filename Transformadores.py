# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 10:56:25 2024

@author: user
"""
def Funcion(Fichero):
    import sys
    import config_powerfactory  # ruta de PowerFactory: ver config_powerfactory.py
    import powerfactory as pf
    import pandas as pd
    app = pf.GetApplication()
    Trafos = pd.read_excel(Fichero, sheet_name='Transformadores')
    Trafos = Trafos.dropna(axis=1, how='all')
    Folder_Tipos = app.GetProjectFolder('equip')
    red= app.GetCalcRelevantObjects('*.ElmNet')[1]
    # Se consultan los tipos y nodos una sola vez (antes se buscaban en toda la base por cada transformador)
    Tipos = config_powerfactory.indexar_por_nombre(Folder_Tipos.GetContents('*.TypTr2'))
    Buses = config_powerfactory.indexar_por_nombre(app.GetCalcRelevantObjects('*.ElmTerm'))
    Contadores = {}
    for i, Trafo in Trafos.iterrows():
        Tipo=Trafo['Tipo']
        Tipo_Trafo=config_powerfactory.buscar(Tipos, Tipo, 'el tipo de transformador')
        Nuevo_Trafo= red.CreateObject('ElmTr2', Trafo['Nombre'])
        Nuevo_Trafo.typ_id=Tipo_Trafo 
        Nuevo_Trafo.ntnum=Trafo['Transformadores Paralelo']
        Bus1=config_powerfactory.buscar(Buses, str(Trafo['Nodo Alta']), 'el nodo')
        Bus2=config_powerfactory.buscar(Buses, str(Trafo['Nodo Baja']), 'el nodo')
        texto1 = config_powerfactory.siguiente_cubiculo(Bus1, Contadores)
        texto2 = config_powerfactory.siguiente_cubiculo(Bus2, Contadores)
        Cub1_Trafo=Bus1.CreateObject('StaCubic',texto1)
        Cub2_Trafo=Bus2.CreateObject('StaCubic',texto2)
        Nuevo_Trafo.bushv=Cub1_Trafo
        Nuevo_Trafo.buslv=Cub2_Trafo
