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
    for i, Trafo in Trafos.iterrows():
        Tipo=Trafo['Tipo']
        Tipo_Trafo=Folder_Tipos.GetContents(Tipo + '.TypTr2')[0]
        Nuevo_Trafo= red.CreateObject('ElmTr2', Trafo['Nombre'])
        Nuevo_Trafo.typ_id=Tipo_Trafo 
        Nuevo_Trafo.ntnum=Trafo['Transformadores Paralelo']
        Nombre_Bus1=Trafo['Nodo Alta']
        Nombre_Bus2=Trafo['Nodo Baja']
        str_Nombre_Bus1= str(Nombre_Bus1)+".ElmTerm"
        str_Nombre_Bus2= str(Nombre_Bus2)+".ElmTerm"
        Bus1=app.GetCalcRelevantObjects(str_Nombre_Bus1)[0]
        Bus2=app.GetCalcRelevantObjects(str_Nombre_Bus2)[0]
        Cubs_b1=Bus1.GetContents()
        Cubs_b2=Bus2.GetContents()
        N_Cubs_b1=len(Cubs_b1)
        N_Cubs_b2=len(Cubs_b2)
        texto1 = "Cub_" + str(N_Cubs_b1+1)
        texto2 = "Cub_" + str(N_Cubs_b2+1)
        Cub1_Trafo=Bus1.CreateObject('StaCubic',texto1)
        Cub2_Trafo=Bus2.CreateObject('StaCubic',texto2)
        Nuevo_Trafo.bushv=Cub1_Trafo
        Nuevo_Trafo.buslv=Cub2_Trafo
        app.PrintPlain(Nuevo_Trafo)
