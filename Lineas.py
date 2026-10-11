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
    for i, Linea in Lineas.iterrows():
        Tipo=Linea['CONDUCTOR']
        Tipo_Linea=Folder_Tipos.GetContents(str(Tipo) + '.TypLne')[0]
        Nueva_Linea= red.CreateObject('ElmLne', Linea['NOMBRE'])
        Nueva_Linea.dline=Linea['LONGITUD']/1000
        Nueva_Linea.typ_id=Tipo_Linea
        Nombre_Bus1=Linea['NODO1']
        Nombre_Bus2=Linea['NODO2']
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
        Cub1_Linea=Bus1.CreateObject('StaCubic',texto1)
        Cub2_Linea=Bus2.CreateObject('StaCubic',texto2)
        Nueva_Linea.bus1=Cub1_Linea
        Nueva_Linea.bus2=Cub2_Linea
        app.PrintPlain(Nueva_Linea)
        app.PrintPlain(i)
    app.PrintPlain('Lineas Creadas')

