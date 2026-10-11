# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 18:30:58 2024

@author: user
"""

def Funcion(Años,Lista_Variaciones, Lista_Diagramas, Direccion_Pdfs, Direccion_Excel):
    import sys
    import config_powerfactory  # ruta de PowerFactory: ver config_powerfactory.py
    import powerfactory as pf
    import pandas as pd
    from datetime import datetime
    
    app = pf.GetApplication()
    red= app.GetCalcRelevantObjects('*.ElmNet')[1]
    Caso_Estudio=app.GetActiveStudyCase()
    Nodos_Corto=Caso_Estudio.GetContents('Nodos_Corto.SetSelect')[0]
    Nodos = Nodos_Corto.All()
        
    Folder_Escenarios = app.GetProjectFolder('scen')
    Contenido_Escenarios=Folder_Escenarios.GetContents()
    
    
    j=0
    for i in Contenido_Escenarios:
        Contenido_Escenarios[j].Delete()
        j=j+1
    A=app.GetActiveScenarioScheduler()
    if A!= None:
        A.Deactivate()
    
    Variaciones=['Sin Variacion']
    Folder_Variaciones=app.GetProjectFolder('scheme')
    for i in Lista_Variaciones:
        Variaciones.extend(Folder_Variaciones.GetContents(i + '.IntScheme'))
        Folder_Variaciones.GetContents(i + '.IntScheme')[0].Deactivate()
        
    def Exportar_Imagenes (Texto,Impresion,Tipo,Variacion):
        Diccionario={'3FCC': 'Trifásico','2FCC': 'Bifásico','1FCC': 'Monofásico'}
        Diccionario_Variacion={0:'Sin Proyecto',1:'Con Proyecto'}
        Carpeta_Graficas=app.GetGraphicsBoard() 
        k=1
        for i in Impresion:
            Grafica=Carpeta_Graficas.GetContents(str(i)+'.SetDeskPage')[0]
            app.PrintPlain(Grafica)
            Grafica.Show()
            Diagrama = app.GetCurrentDiagram() 
            app.PrintPlain(Diagrama)
            Layers=Diagrama.GetContents('Layers.IntFolder')[0]
            Contenido_Layers=Layers.GetContents()
            for i in Contenido_Layers:
                Tipo_Layer=i.GetAttribute('layerId')
                if Tipo_Layer==43:
                    Nombre_Titulo=i.GetAttribute('loc_name')
                    break
            Title=Layers.GetContents(Nombre_Titulo + '.IntGrflayer')[0]
            Title.iVis=1
            Configuracion=Diagrama.GetContents('Settings.IntFolder')[0]
            app.PrintPlain(Configuracion)
            Titulo=Configuracion.GetContents('*.VisTitle')[0]
            app.PrintPlain(Titulo)
            Conf_Titulo=Titulo.GetAttribute('SetTit')
            Texto_Tipo_Corto=Diccionario[Tipo]
            Conf_Titulo.sub1z='Corto ' + Texto_Tipo_Corto 
            Conf_Titulo.sub3z=Diccionario_Variacion[Variacion]
            app.PrintPlain(Conf_Titulo)
            ComWr = app.GetFromStudyCase('ComWr')
            ComWr.iopt_rd='pdf'
            ComWr.iopt_savas=0
            ComWr.f= Direccion_Pdfs +'\ '  + Texto + str(k) +'.pdf'
            ComWr.Execute()
            k=k+1    
        
    def Resultados_Corto(Nodos,Tipo):  
        if Tipo == '3psc':
            Nombre_Ik='m:Ikss'
            Nombre_Sk='m:Skss'
            Nombre_Ip='m:Ip'
        elif Tipo == 'spgf':
            Nombre_Ik='m:Ikss:A'
            Nombre_Sk='m:Skss:A'
            Nombre_Ip='m:Ip:A'
        elif Tipo == '2psc':
            Nombre_Ik='m:Ikss:B'
            Nombre_Sk='m:Skss:B'
            Nombre_Ip='m:Ip:B'  

        Lista_Ikss=[]
        Lista_Skss=[]
        Lista_Ip=[]
        for Nodo in Nodos:
            try:
                Val_Ikss=Nodo.GetAttribute(Nombre_Ik)
                Val_Skss=Nodo.GetAttribute(Nombre_Sk)
                Val_Ip=Nodo.GetAttribute(Nombre_Ip)
            except:    
                Val_Ikss=0
                Val_Skss=0
                Val_Ip=0
            Lista_Ikss.append(Val_Ikss)
            Lista_Skss.append(Val_Skss)
            Lista_Ip.append(Val_Ip)
        return(Lista_Ikss,Lista_Skss,Lista_Ip)  

    Diccionario={}
    Nombres=[]
    for Nodo in Nodos:
        Nombres.append(Nodo.GetAttribute('loc_name'))
    Diccionario['Nombre']=Nombres
    
    Tiempo= app.GetFromStudyCase('SetTime')
    Tipo_Corto=['3FCC','1FCC','2FCC']
    Tipo_Pf=['3psc','spgf','2psc']
    m=0
    for Variacion in Variaciones: 
        # try:
        #     Variacion_Activa=app.GetActiveNetworkVariations()[0]
        #     Variacion_Activa.Deactivate()
        # except:
        #     app.PrintPlain('Iniciamos sin variaciones activadas')  
        if Variacion != 'Sin Variacion':
            Variacion.Activate()
        for i in Años:
            Año=str(i)
            Tiempo.cDate= Año + '0601'
            k=0
            for j in Tipo_Corto:
                Corto=app.GetFromStudyCase('ComShc')
                Corto.iopt_mde=1
                Corto.iopt_shc=Tipo_Pf[k]
                T_Corto=Tipo_Pf[k]
                Corto.Rf=0
                app.PrintPlain(Corto.iopt_shc)
                k=k+1
                Corto.iopt_allbus=0
                Corto.shcobj=Nodos_Corto
                Caso_Estudio=app.GetActiveStudyCase()
                Caso_Estudio.Deactivate()
                Caso_Estudio.Activate()
                Corto.Execute()
                Lista_Ikss,Lista_Skss,Lista_Ip=Resultados_Corto(Nodos,T_Corto)
                Nombre= str(i) + '_' + str(j) + '_V' + str(m)
                Diccionario[Nombre + '_Ikss']=Lista_Ikss
                Diccionario[Nombre + '_Skss']=Lista_Skss
                Diccionario[Nombre + '_Ip']=Lista_Ip
                Exportar_Imagenes(Nombre,Lista_Diagramas,j,m)
        if Variacion != 'Sin Variacion':
            Variacion.Deactivate()
        m=m+1
    Resultados_Corto = pd.DataFrame(Diccionario)
    Lista_Resultados=[]
    Titulos=[]
    app.PrintPlain('Exportando datos a Excel')
    for i in Años:
        for j in Tipo_Corto:
            Texto0='Nombre'
            Texto1= str(i) + '_' + str(j) + '_V0' + '_Ikss'
            Texto2= str(i) + '_' + str(j) + '_V0' + '_Skss'
            Texto3= str(i) + '_' + str(j) + '_V0' + '_Ip'
            Texto4= str(i) + '_' + str(j) + '_V1' + '_Ikss'
            Texto5= str(i) + '_' + str(j) + '_V1' + '_Skss'
            Texto6= str(i) + '_' + str(j) + '_V1' + '_Ip'
            DataFrame=Resultados_Corto[[Texto0,Texto1,Texto2,Texto3,Texto4,\
                                        Texto5,Texto6]]
            Lista_Resultados.append(DataFrame)
            Titulos.append(str(i) + '_' + str(j))
    
    with pd.ExcelWriter(Direccion_Excel + '\CortoCircuito.xlsx') as writer:
        k=0
        for i in Lista_Resultados:
            Titulo=Titulos[k]
            k=k+1
            i.to_excel(writer, index=False, sheet_name= Titulo)
    app.PrintPlain('Resultados Exportados')          
            
    