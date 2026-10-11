# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 18:30:58 2024

@author: user
"""

def Funcion(Pt_Cabecera,Pt_Curva_PGF, Lista_Cortos,Delta_Fase,Delta_Tierra):
    import sys
    import config_powerfactory  # ruta de PowerFactory: ver config_powerfactory.py
    import powerfactory as pf
    import pandas as pd
    import numpy as np
    from datetime import datetime

    import sys
    import config_powerfactory  # ruta de PowerFactory: ver config_powerfactory.py
    import powerfactory as pf
    app = pf.GetApplication()

    Folder_Variaciones=app.GetProjectFolder('scheme')
    Variacion=Folder_Variaciones.GetContents(Pt_Curva_PGF.Variacion + '.IntScheme')[0]
    Variacion.Activate()   
    
    Medida_Cabecera=app.GetCalcRelevantObjects(Pt_Cabecera.Elm_Sensado)[0]
    Medida_PGF=app.GetCalcRelevantObjects(Pt_Curva_PGF.Sensado)[0]

    Nodo_MT_OR= app.GetCalcRelevantObjects(Pt_Curva_PGF.Barra_MT_OR + '.ElmTerm')[0]
    Tension_OR= Nodo_MT_OR.GetAttribute('uknom')

    Nodo_MT_PGF= app.GetCalcRelevantObjects(Pt_Curva_PGF.Barra_MT_PGF + '.ElmTerm')[0]
    Nodo_MT_Cabecera= app.GetCalcRelevantObjects(Pt_Cabecera.Nodo + '.ElmTerm')[0]

    #Nodo_MT_PGF.GetConnectedElements



    app = pf.GetApplication()
    red= app.GetCalcRelevantObjects('*.ElmNet')[1]
    Caso_Estudio=app.GetActiveStudyCase()
    Nodos_Corto=Lista_Cortos
    Nodos=[]

    for i in Nodos_Corto:
        Nodos.append(app.GetCalcRelevantObjects( i + '.ElmTerm')[0])
    
    
        
    Folder_Escenarios = app.GetProjectFolder('scen')
    Contenido_Escenarios=Folder_Escenarios.GetContents()

    Fallas=['3FCC','2FCC','1FCC']
    Tipo_Corto=['3psc','2psc','spgf']
   
    
    j=0
    for i in Contenido_Escenarios:
        Contenido_Escenarios[j].Delete()
        j=j+1
    A=app.GetActiveScenarioScheduler()
    if A!= None:
        A.Deactivate()
    
    
        
    def Resultados_Corto(Pt_Cabecera,Pt_Curva_PGF,Tipo): 
        Tipo_Cabecera=Medida_Cabecera.GetClassName()
        Lista_Ikss_Cabecera,Lista_Phii_Cabecera\
            =Obtener_Corriente(Tipo_Cabecera,Medida_Cabecera,\
                                              Pt_Cabecera,Pt_Curva_PGF)
        Tipo_PGF=Medida_PGF.GetClassName()
        Lista_Ikss_PGF,Lista_Phii_PGF\
            =Obtener_Corriente(Tipo_PGF,Medida_PGF,\
                                         Pt_Cabecera,Pt_Curva_PGF)
        Lista_Tensiones_Cabecera=Obtener_Tensiones(Nodo_MT_Cabecera,Tipo)
        Lista_Tensiones_PGF=Obtener_Tensiones(Nodo_MT_PGF,Tipo)
        return(Lista_Ikss_Cabecera,Lista_Ikss_PGF,Lista_Phii_Cabecera,\
                    Lista_Phii_PGF,Lista_Tensiones_Cabecera,Lista_Tensiones_PGF)  

    def Obtener_Corriente(Tipo,i,Pt_Cabecera,Pt_Curva_PGF):
        if Tipo=='ElmLne':
            Cub1=i.GetAttribute('bus1')
            Cub2=i.GetAttribute('bus2')
        elif Tipo=='ElmTr2':
            Cub1=i.GetAttribute('bushv')
            Cub2=i.GetAttribute('buslv')
        elif Tipo== 'ElmXnet':
            Cub1=i.GetAttribute('bus1')
            Cub2=i.GetAttribute('bus1')
        elif Tipo== 'ElmCoup':
            Cub1=i.GetAttribute('bus1')
            Cub2=i.GetAttribute('bus2')

        Nodo1=Cub1.GetAttribute('cterm')
        Nodo2=Cub2.GetAttribute('cterm')

        if Nodo1.GetAttribute('loc_name')==Pt_Cabecera.Nodo or \
            Nodo1.GetAttribute('loc_name')==Pt_Curva_PGF.Barra_MT_PGF:
            try:
                Iks_A=i.GetAttribute('m:Ikss:bus1:A')
                Iks_B=i.GetAttribute('m:Ikss:bus1:B')
                Iks_C=i.GetAttribute('m:Ikss:bus1:C')
                Phii_A=i.GetAttribute('m:phii:bus1:A')
                Phii_B=i.GetAttribute('m:phii:bus1:B')
                Phii_C=i.GetAttribute('m:phii:bus1:C')
                
            except:
                Iks_A=i.GetAttribute('m:Ikss:bushv:A')
                Iks_B=i.GetAttribute('m:Ikss:bushv:B')
                Iks_C=i.GetAttribute('m:Ikss:bushv:C')
                Phii_A=i.GetAttribute('m:phii:bushv:A')
                Phii_B=i.GetAttribute('m:phii:bushv:B')
                Phii_C=i.GetAttribute('m:phii:bushv:C')
        elif Nodo2.GetAttribute('loc_name')==Pt_Cabecera.Nodo or \
            Nodo2.GetAttribute('loc_name')==Pt_Curva_PGF.Barra_MT_PGF:
            try:
                Iks_A=i.GetAttribute('m:Ikss:bus2:A')
                Iks_B=i.GetAttribute('m:Ikss:bus2:B')
                Iks_C=i.GetAttribute('m:Ikss:bus2:C')
                Phii_A=i.GetAttribute('m:phii:bus2:A')
                Phii_B=i.GetAttribute('m:phii:bus2:B')
                Phii_C=i.GetAttribute('m:phii:bus2:C')
            except:
                Iks_A=i.GetAttribute('m:Ikss:buslv:A')
                Iks_B=i.GetAttribute('m:Ikss:buslv:B')
                Iks_C=i.GetAttribute('m:Ikss:buslv:C') 
                Phii_A=i.GetAttribute('m:phii:buslv:A')
                Phii_B=i.GetAttribute('m:phii:buslv:B')
                Phii_C=i.GetAttribute('m:phii:buslv:C') 
        else:
            Iks_A=0
            Iks_B=0
            Iks_C=0
            Phii_A=0
            Phii_B=0
            Phii_C=0
        return([Iks_A,Iks_B,Iks_C],[Phii_A,Phii_B,Phii_C])
    
    def Obtener_Tensiones(i,Tipo):
        TensionA=i.GetAttribute('m:u:A')
        TensionB=i.GetAttribute('m:u:B')
        TensionC=i.GetAttribute('m:u:C')
        if Tipo=='spgf':
            TensionN=(i.GetAttribute('m:u0'))*3
        else:
            TensionN=0
        return([TensionA,TensionB,TensionC,TensionN])

    Diccionario_Corrientes_Cabecera={}
    Diccionario_Tensiones_Cabecera={}
    Diccionario_Corrientes_PGF={}
    Diccionario_Tensiones_PGF={}
    Resistencias=[Pt_Curva_PGF.RFalla_1,Pt_Curva_PGF.RFalla_2,Pt_Curva_PGF.RFalla_3]
    Diccionario_0={}
    Diccionario_2={}
    Diccionario_3={}
    for i in Lista_Cortos:
        Diccionario_0[i +'_MAG_A'] = []
        Diccionario_0[i +'_MAG_B'] = []
        Diccionario_0[i +'_MAG_C'] = []
        Diccionario_2[i +'_MAG_A'] = []
        Diccionario_2[i +'_MAG_B'] = []
        Diccionario_2[i +'_MAG_C'] = []
        Diccionario_0[i +'_DEG_A'] = []
        Diccionario_0[i +'_DEG_B'] = []
        Diccionario_0[i +'_DEG_C'] = []
        Diccionario_2[i +'_DEG_A'] = []
        Diccionario_2[i +'_DEG_B'] = []
        Diccionario_2[i +'_DEG_C'] = []
        Diccionario_3[i + '_Tension_A']=[]
        Diccionario_3[i + '_Tension_B']=[]
        Diccionario_3[i + '_Tension_C']=[]
        Diccionario_3[i + '_Tension_N']=[]
    Diccionario_1={'Tipo':[],'Resistencia':[]}
    Diccionario_Corrientes_Cabecera= Diccionario_1 | Diccionario_0
    Diccionario_Corrientes_PGF=Diccionario_1 | Diccionario_2
    Diccionario_Tensiones_PGF=Diccionario_1 | Diccionario_3

    def Establecer_Corrientes(df,Nodos):
        for Nodo in Nodos:
            df[Nombre_Nodo + '_DEG_A']*np.pi / 180

    for Resistencia in Resistencias:
        for k in range(3):
            Falla=Fallas[k]
            Tipo=Tipo_Corto[k]
            Diccionario_Corrientes_Cabecera['Tipo'].append(Tipo)
            Diccionario_Corrientes_Cabecera['Resistencia'].append(Resistencia)
            for Nodo in Nodos:
                Tension_Nodo=Nodo.GetAttribute('uknom')
                Relacion=Tension_OR/Tension_Nodo
                R_Falla=float(Resistencia)/(Relacion**2)
                Nombre_Nodo=Nodo.GetAttribute('loc_name')  
                Clave= Nombre_Nodo + '_' + Falla + '_' + str(Resistencia)
                Corto=app.GetFromStudyCase('ComShc')
                Corto.iopt_mde=1
                Corto.iopt_cur=0
                Corto.iopt_shc=Tipo
                Corto.Rf=float(R_Falla)
                app.PrintPlain(Corto.iopt_shc)
                Corto.iopt_allbus=0
                Corto.shcobj=Nodo
                Corto.Execute()
                Lista_Ikss_Cabecera,Lista_Ikss_PGF,Lista_Phii_Cabecera,Lista_Phii_PGF,\
                Lista_Tensiones_Cabecera,Lista_Tensiones_PGF=Resultados_Corto(Pt_Cabecera,Pt_Curva_PGF,Tipo)
                Diccionario_Corrientes_Cabecera[Nombre_Nodo + '_MAG_A'].append(Lista_Ikss_Cabecera[0])
                Diccionario_Corrientes_Cabecera[Nombre_Nodo + '_MAG_B'].append(Lista_Ikss_Cabecera[1])
                Diccionario_Corrientes_Cabecera[Nombre_Nodo + '_MAG_C'].append(Lista_Ikss_Cabecera[2])
                Diccionario_Corrientes_PGF[Nombre_Nodo + '_MAG_A'].append(Lista_Ikss_PGF[0])
                Diccionario_Corrientes_PGF[Nombre_Nodo + '_MAG_B'].append(Lista_Ikss_PGF[1])
                Diccionario_Corrientes_PGF[Nombre_Nodo + '_MAG_C'].append(Lista_Ikss_PGF[2])
                Diccionario_Corrientes_Cabecera[Nombre_Nodo + '_DEG_A'].append(Lista_Phii_Cabecera[0])
                Diccionario_Corrientes_Cabecera[Nombre_Nodo + '_DEG_B'].append(Lista_Phii_Cabecera[1])
                Diccionario_Corrientes_Cabecera[Nombre_Nodo + '_DEG_C'].append(Lista_Phii_Cabecera[2])
                Diccionario_Corrientes_PGF[Nombre_Nodo + '_DEG_A'].append(Lista_Phii_PGF[0])
                Diccionario_Corrientes_PGF[Nombre_Nodo + '_DEG_B'].append(Lista_Phii_PGF[1])
                Diccionario_Corrientes_PGF[Nombre_Nodo + '_DEG_C'].append(Lista_Phii_PGF[2])
                Diccionario_Tensiones_PGF[Nombre_Nodo + '_Tension_A'].append(Lista_Tensiones_PGF[0])
                Diccionario_Tensiones_PGF[Nombre_Nodo + '_Tension_B'].append(Lista_Tensiones_PGF[1])
                Diccionario_Tensiones_PGF[Nombre_Nodo + '_Tension_C'].append(Lista_Tensiones_PGF[2])
                Diccionario_Tensiones_PGF[Nombre_Nodo + '_Tension_N'].append(Lista_Tensiones_PGF[3])
            
    df_Cabecera = pd.DataFrame(Diccionario_Corrientes_Cabecera)
    df_PGF = pd.DataFrame(Diccionario_Corrientes_PGF)
    df_PGF_Tensiones = pd.DataFrame(Diccionario_Tensiones_PGF)
    import Tabla_Corrientes
    Lista_Frame,Lista_Frames_Tensiones=Tabla_Corrientes.Funcion(df_Cabecera,df_PGF, Lista_Cortos,df_PGF_Tensiones)

    import Calculos_Coordinacion
    Lista_Frames_Fase,Lista_Frames_Tierra,\
        Diccionario_Curvas_PGF=Calculos_Coordinacion.Funcion(Lista_Frame,Pt_Cabecera,Pt_Curva_PGF,\
                                                             Delta_Fase,Delta_Tierra)


    
                
    return(Lista_Frames_Fase,Lista_Frames_Tierra,Diccionario_Curvas_PGF,Lista_Frames_Tensiones)
    