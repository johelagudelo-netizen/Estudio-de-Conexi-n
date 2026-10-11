# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 15:58:48 2024

@author: user
"""
def Funcion(Fichero):
    import sys
    import pandas as pd
    import config_powerfactory  # ruta de PowerFactory: ver config_powerfactory.py
    import powerfactory as pf
    app = pf.GetApplication()
    Tipo_Lineas = pd.read_excel(Fichero, sheet_name='Tipo_Líneas')
    Tipo_Lineas = Tipo_Lineas.dropna(axis=1, how='all')
    Folder_Tipos = app.GetProjectFolder('equip')
    for i, Tipo in Tipo_Lineas.iterrows():
        Nuevo_Tipo_Linea = Folder_Tipos.CreateObject\
                                    ('TypLne',Tipo['Nombre'])
        Nuevo_Tipo_Linea.uline=Tipo['Voltaje Nominal']
        Nuevo_Tipo_Linea.sline=Tipo['Corriente Nominal']
        Nuevo_Tipo_Linea.cohl_=Tipo['Tipo']
        Nuevo_Tipo_Linea.frnom=60
        Nuevo_Tipo_Linea.rline=Tipo['R1']
        Nuevo_Tipo_Linea.xline=Tipo['X1']
        Nuevo_Tipo_Linea.rline0=Tipo['R0']
        Nuevo_Tipo_Linea.xline0=Tipo['X0']
        Nuevo_Tipo_Linea.nlnph=Tipo['Fases']
