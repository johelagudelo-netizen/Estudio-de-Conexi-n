# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 10:23:59 2024

@author: user
"""
def Funcion(Fichero):
    import sys
    import config_powerfactory  # ruta de PowerFactory: ver config_powerfactory.py
    import powerfactory as pf
    import pandas as pd
    app = pf.GetApplication()
    red= app.GetCalcRelevantObjects('*.ElmNet')[1]
    Tipo_Trafos = pd.read_excel(Fichero, sheet_name='Tipo_Transformadores')
    Tipo_Trafos = Tipo_Trafos.dropna(axis=1, how='all')
    Folder_Tipos = app.GetProjectFolder('equip')
    for i, Tipo in Tipo_Trafos.iterrows():
        Nuevo_Tipo_Trafo = Folder_Tipos.CreateObject\
                                    ('TypTr2',Tipo['Nombre'])
        Nuevo_Tipo_Trafo.nt2ph=Tipo['Tecnología']
        Nuevo_Tipo_Trafo.strn=Tipo['Tecnología']
        Nuevo_Tipo_Trafo.frnom=60  
        Nuevo_Tipo_Trafo.utrn_h=Tipo['Tensión Alta']       
        Nuevo_Tipo_Trafo.utrn_l=Tipo['Tensión Baja']                        
        Nuevo_Tipo_Trafo.uktr=Tipo['Vcc']    
        Nuevo_Tipo_Trafo.pcutr=Tipo['Pérdidas Cobre']  
        Nuevo_Tipo_Trafo.uk0tr=Tipo['Vcc0'] 
        Nuevo_Tipo_Trafo.pcutr=Tipo['Pérdidas Cobre']   
        Nuevo_Tipo_Trafo.tr2cn_h=Tipo['Conexión Alta']  
        Nuevo_Tipo_Trafo.tr2cn_l=Tipo['Conexión Baja']  
        Nuevo_Tipo_Trafo.nt2ag=Tipo['Desfase Horario']  

                        
