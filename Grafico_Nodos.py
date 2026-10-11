# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 13:58:02 2024

@author: user
"""

import sys
import config_powerfactory  # ruta de PowerFactory: ver config_powerfactory.py
import powerfactory as pf
import pandas as pd
app = pf.GetApplication()
red= app.GetCalcRelevantObjects('*.ElmNet')[1]
Nodos= pd.read_excel('Proyecto.xlsm', sheet_name='Nodos')
Nodos = Nodos.dropna(axis=1, how='all')

diagrama = app.GetCurrentDiagram() 
app.PrintPlain(diagrama)

# Crear Nodos - Network Data
for i , Nodo in Nodos.iterrows():
    Nombre=Nodo['Nombre']
    Nodo_Evaluado=app.GetCalcRelevantObjects(Nombre + '.ElmTerm')[0]
    nuevo_nodo_grafico=diagrama.CreateObject('IntGrf',Nombre)
    nuevo_nodo_grafico.rCenterX=Nodo['Cordenada X']/100
    nuevo_nodo_grafico.rCenterY=Nodo['Cordenada Y']/100
    nuevo_nodo_grafico.rSizeX=1
    app.PrintPlain(nuevo_nodo_grafico)
    nuevo_nodo_grafico.pDataObj=Nodo_Evaluado
    nuevo_nodo_grafico.sSymNam='TermStrip'
    nuevo_nodo_grafico.iRot=0
