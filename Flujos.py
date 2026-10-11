# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 16:28:31 2024

@author: user
"""
def Funcion(Fichero,Lista_Variaciones,Escenarios,Años,Hora,Impresion,Ruta_Pdfs,Ruta_Excel):
    import sys
    import config_powerfactory  # ruta de PowerFactory: ver config_powerfactory.py
    import powerfactory as pf
    import pandas as pd
    from datetime import datetime

    app = pf.GetApplication()
    red= app.GetCalcRelevantObjects('*.ElmNet')[1]
    Caso_Estudio=app.GetActiveStudyCase()

    Proyecciones=pd.read_excel(Fichero, sheet_name='Proyecciones_Demanda')
    Proyecciones = Proyecciones.dropna(axis=1, how='all')
    Alimentador=pd.read_excel(Fichero, sheet_name='Alimentador')
    Alimentador = Alimentador.dropna(axis=1, how='all')
    Escenarios_Demanda_Hora=pd.read_excel(Fichero, sheet_name='Escenarios')
    Escenarios_Demanda_Hora = Escenarios_Demanda_Hora.dropna(axis=1, how='all')
    Nodo_Alimentador_0=Alimentador['Nombre'][0]
    Nodo_Alimentador=app.GetCalcRelevantObjects(str(Nodo_Alimentador_0) + '.ElmTerm')[0]
    app.PrintPlain(Nodo_Alimentador)
    Zona=Nodo_Alimentador.GetAttribute('cpZone')
    #Zona=Folder_Zona.GetContents(Nombre_Zona + '.ElmZone')[0]
    app.PrintPlain(Zona)
    Variaciones=['Sin Variaciones']
    Contingencias=['Sin Contingencias']


    Contingencias_General=Caso_Estudio.GetContents('Contingencias.SetSelect')[0]
    Contingencias.extend(Contingencias_General.All())
    app.PrintPlain(Contingencias)
    Cargabilidades_General=Caso_Estudio.GetContents('Cargabilidades.SetSelect')[0]
    Cargabilidades = Cargabilidades_General.All()
    Nodos_Tensiones=Caso_Estudio.GetContents('Nodos.SetSelect')[0]
    Nodos = Nodos_Tensiones.All()
    #Generar Lista de Variaciones 
    Folder_Variaciones=app.GetProjectFolder('scheme')
    for i in Lista_Variaciones:
        Variaciones.extend(Folder_Variaciones.GetContents(i + '.IntScheme'))

   

    """
    Condiciones Iniciales Eliminar Escenarios de Operación

    """
    Folder_Escenarios = app.GetProjectFolder('scen')
    Contenido_Escenarios=Folder_Escenarios.GetContents()
    j=0
    for i in Contenido_Escenarios:
        Contenido_Escenarios[j].Delete()
        j=j+1
    A=app.GetActiveScenarioScheduler()
    if A!= None:
        A.Deactivate()

    Inicio=[]
    Fin=[]

    for Contingencia in Contingencias:
        if Contingencia!='Sin Contingencias':
            Contingencia.outserv=0


    for i in Años:
        Año_Inicio = i
        Fecha1 = datetime(int(Año_Inicio), 5, 6,13,0,0)
        Fecha_Ref=datetime(1969,12,31,19,0,0)
        Fecha2= Fecha1.replace(month=7)
        Inicio.append(int((Fecha1-Fecha_Ref).total_seconds()))
        Fin.append(int((Fecha2-Fecha_Ref).total_seconds()))
        
    Folder_Escenarios = app.GetProjectFolder('scen')
    Diccionario={}
    for i in Escenarios: 
        Diccionario[i]=[]


    """
    **************************************************
    Crear Escenarios de Operación

    """
    for i in Años:
        Año=str(i)
        Nombre='AÑO' + " " + Año
        Sub_Folder=Folder_Escenarios.CreateObject('IntFolder', Nombre)
        Factores_Año=Proyecciones.loc[Proyecciones['AÑO']==int(i)]
        k=0
        for j in Escenarios:
            k=k+1        
            Nombre_Escenario= Año + " " + j
            Escenario_Operacion=Sub_Folder.CreateObject('IntScenario', \
                                                            Nombre_Escenario)
            Escenario_Operacion.Activate()
            
            Zona.curscale=1+(Factores_Año[j].tolist()[0])
            Diccionario[j].append(Escenario_Operacion)

    for i in Escenarios: 
        Reloj=Folder_Escenarios.CreateObject('IntScensched', 'Escenarios' + ' ' + i)
        Reloj.tStartTime=Inicio  
        Reloj.tEndTime=Fin
        Reloj.pScenario=Diccionario[i]



    """
    *******************************************************************************
    Exportar Pdfs

    """

    def Exportar_Imagenes (Texto,Impresion,Hora,Año,Contingencia,\
                           Variacion, Nombre_Escenario):
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
            Conf_Titulo.anex='Flujo'
            #Conf_Titulo.sub1z='Hora ' + Hora[:-4]
            Conf_Titulo.sub2z='Año: ' + Año + ' - ' + Nombre_Escenario
            if Contingencia==0:
                Texto_Contingencia='Sin Contingencia'
            else:
                Texto_Contingencia= 'Contingencia' + str(Contingencia)
            if Variacion==0:
                Texto_Proyecto='Sin Proyecto'
            else:
                Texto_Proyecto='Con Proyecto'
            Conf_Titulo.sub3z= Texto_Contingencia + ' - ' + Texto_Proyecto
            app.PrintPlain(Conf_Titulo)
            ComWr = app.GetFromStudyCase('ComWr')
            ComWr.iopt_rd='pdf'
            ComWr.iopt_savas=0
            ComWr.f= Ruta_Pdfs +'\ '  + Texto + str(k) +'.pdf'
            ComWr.Execute()
            k=k+1

    """
    **********************************************************************************
    Guardar Resultado de Tensiones en los Nodos

    """

    def Tensiones_Nodos(Nodos):
        Lista_Tensiones_pu=[]
        Lista_Tensiones_V=[]
        for Nodo in Nodos:
            try:
                Val_u=Nodo.GetAttribute('m:u')
                Val_U=Nodo.GetAttribute('m:Ul')
            except:    
                Val_u=0
                Val_U=0
            Lista_Tensiones_pu.append(Val_u)
            Lista_Tensiones_V.append(Val_U)
        return(Lista_Tensiones_pu,Lista_Tensiones_V)  
    
    def Definir_Cargabilidades(Cargabilidades):
        Lista_Cargabilidades=[]
        for Cargabilidad in Cargabilidades:
            if Cargabilidad.GetAttribute('outserv')==0:           
                try: 
                    Val_loading=Cargabilidad.GetAttribute('c:loading')
                except:
                    Val_loading='-'
                Lista_Cargabilidades.append(Val_loading)
            else:
                Lista_Cargabilidades.append(0)
        return(Lista_Cargabilidades) 

    Elementos_Perdidas=[]   # se llena en el primer caso y se reutiliza (los elementos no cambian)

    def Definir_Perdidas(red):
        Lista_Nombres_Perdidas=[]
        Lista_Perdidas_2=[]
        Lista_Potencia_Perdidas=[]
        Total_Perdidas=0 
        if not Elementos_Perdidas:
            Elementos_Perdidas.extend([app.GetCalcRelevantObjects('*.ElmTr2'),
                                       app.GetCalcRelevantObjects('*.ElmTr3'),
                                       app.GetCalcRelevantObjects('*.ElmLne')])
        Tr2_Calculo, Tr3_Calculo, Lineas_Calculo = Elementos_Perdidas
        for i in Tr3_Calculo:
            if i.GetAttribute('outserv')==0:
                try:  
                    Perdida=abs(i.GetAttribute('c:Ploss'))
                    Nombre=i.GetAttribute('loc_name')
                    Potencia_Activa=i.GetAttribute('m:P:bushv')
                except:
                    Perdida='-'
                    Nombre='-'
                    Potencia_Activa='-'
            else:
                Perdida=0
                Nombre=0
                Potencia_Activa=0
            Lista_Nombres_Perdidas.append(Nombre)
            Lista_Perdidas_2.append(Perdida)
            Lista_Potencia_Perdidas.append(Potencia_Activa)
            Total_Perdidas=Total_Perdidas+ Perdida
        for i in Tr2_Calculo:
            if i.GetAttribute('outserv')==0:
                try:  
                    Perdida=abs(i.GetAttribute('c:Ploss'))
                    Nombre=i.GetAttribute('loc_name')
                    Potencia_Activa=i.GetAttribute('m:P:bushv')
                except:
                    Perdida='-'
                    Nombre='-'
                    Potencia_Activa='-'
            else:
                Perdida=0
                Nombre=0
                Potencia_Activa=0
            Lista_Nombres_Perdidas.append(Nombre)
            Lista_Perdidas_2.append(Perdida)
            Lista_Potencia_Perdidas.append(Potencia_Activa)
            Total_Perdidas=Total_Perdidas+ Perdida
        for i in Lineas_Calculo :  
            if i.GetAttribute('outserv')==0: 
                try:
                    Perdida=abs(i.GetAttribute('c:Losses'))
                    Nombre=i.GetAttribute('loc_name')
                    Potencia_Activa=i.GetAttribute('m:P:bus1')
                except:
                    Perdida='-'
                    Nombre='-'
                    Potencia_Activa='-'
            else:
                Perdida=0
                Nombre=0
                Potencia_Activa=0
            Lista_Nombres_Perdidas.append(Nombre)
            Lista_Perdidas_2.append(Perdida)
            Lista_Potencia_Perdidas.append(Potencia_Activa)
            try:
                Total_Perdidas=Total_Perdidas+ Perdida
            except:
                print('Hola Mundo')
        app.PrintPlain('###############============Perdidas============##################')   
        app.PrintPlain(Total_Perdidas)
        app.PrintPlain('###############========================##################')
        return([Total_Perdidas],Lista_Nombres_Perdidas,Lista_Perdidas_2,Lista_Potencia_Perdidas) 

    Diccionario_Tensiones={}
    Diccionario_Tensiones_2={}
    Diccionario_Cargabilidades={}
    Diccionario_Cargabilidades_2={}
    Diccionario_Perdidas={}
    Diccionario_Perdidas_2={}

    """
    Definir los Nombres de los elementos en cada uno de los diccionarios
    """
    Lista_Nombre_Tensiones=[]
    Lista_Nombre_Cargabilidades=[]
    for Nodo in Nodos:
            Lista_Nombre_Tensiones.append(Nodo.GetAttribute('loc_name'))
    Diccionario_Tensiones['Nombre']=Lista_Nombre_Tensiones
    Diccionario_Tensiones_2['Nombre']=Lista_Nombre_Tensiones

    for Cargabilidad in Cargabilidades:
        Lista_Nombre_Cargabilidades.append(Cargabilidad.GetAttribute('loc_name'))
    Diccionario_Cargabilidades['Nombre']=Lista_Nombre_Cargabilidades
    Diccionario_Cargabilidades_2['Nombre']=Lista_Nombre_Cargabilidades

    def Ejecutar_Flujo(Escenarios,Diccionario_Tensiones,Diccionario_Cargabilidades,\
                    Folder_Escenarios,Proyecciones,Tiempo,Nodos,Hora,f,m,Contingencia,\
                        Impresion,Escenarios_Demanda_Hora):  
        for k in Escenarios:
            Reloj=Folder_Escenarios.GetContents('Escenarios' + ' ' + k+'.IntScensched')[0]
            Reloj.Activate()
            for Fecha in Años:
                Año=str(int(Fecha))
                Tiempo.cDate= Año + '0601'
                if Contingencia!='Sin Contingencias':
                    Contingencia.outserv=1
                for i in Hora:  
                    Nombre_Escenario = Escenarios_Demanda_Hora['Nombre Escenario'][int(i[:-4])]
                    Texto= Año + i[:-4] + k + 'C' +  str(f) + 'V' + str(m)
                    app.PrintPlain('Estamos corriendo el caso:')
                    app.PrintPlain(Texto)            
                    Tiempo.cTime=i
                    Flujo_Carga=app.GetFromStudyCase('ComLdf')
                    Flujo_Carga.Execute()
                    Exportar_Imagenes(Texto,Impresion,i,Año,f,\
                                      m,Nombre_Escenario)
                    Lista_Tensiones_pu,Lista_Tensiones_V=Tensiones_Nodos(Nodos)
                    Diccionario_Tensiones[Texto]=Lista_Tensiones_pu
                    Lista_Cargabilidades=Definir_Cargabilidades(Cargabilidades)
                    Diccionario_Cargabilidades[Texto]=Lista_Cargabilidades
                    if f==0:
                        Lista_Perdidas,Lista_Nombres_Perdidas,Lista_Perdidas_2,\
                                    Lista_Potencia_Perdidas=Definir_Perdidas(red)
                        Diccionario_Perdidas[Texto]=Lista_Perdidas
                        Diccionario_Perdidas_2[Texto + '_Nombre']=Lista_Nombres_Perdidas
                        Diccionario_Perdidas_2[Texto + '_Loss']=Lista_Perdidas_2
                        Diccionario_Perdidas_2[Texto + '_P']=Lista_Potencia_Perdidas
                        Diccionario_Tensiones_2[Texto+ '_pu']=Lista_Tensiones_pu
                        Diccionario_Tensiones_2[Texto+ '_kV']=Lista_Tensiones_V
                        Diccionario_Cargabilidades_2[Texto]=Lista_Cargabilidades
                if Contingencia!='Sin Contingencias':
                    Contingencia.outserv=0 
        return(Diccionario_Tensiones,Diccionario_Cargabilidades,Diccionario_Perdidas,\
            Diccionario_Tensiones_2,Diccionario_Cargabilidades_2,Diccionario_Perdidas_2)

    Hora_Copia=Hora.copy()
    Hora= [x + "0000" for x in Hora]
    app.PrintPlain(Hora)

    Tiempo= app.GetFromStudyCase('SetTime')

    for Variacion in Variaciones:
        if Variacion!='Sin Variaciones':
            Variacion.Deactivate()

    m=0
    for Variacion in Variaciones:
        f=0
        if Variacion != 'Sin Variaciones':
            Variacion.Activate()
        for Contingencia in Contingencias:
            Caso_Estudio=app.GetActiveStudyCase()
            Caso_Estudio.Deactivate()
            Caso_Estudio.Activate()
            Diccionario_Tensiones,Diccionario_Cargabilidades,Diccionario_Perdidas,\
            Diccionario_Tensiones_2,Diccionario_Cargabilidades_2,Diccionario_Perdidas_2 \
                = Ejecutar_Flujo (Escenarios,Diccionario_Tensiones,Diccionario_Cargabilidades,\
                    Folder_Escenarios,Proyecciones,Tiempo,Nodos,Hora,f,m,Contingencia,Impresion,\
                        Escenarios_Demanda_Hora)    
            app.PrintPlain('#############========La Linea actual en contingencia es===========##################')
            app.PrintPlain(Contingencia)
            f=f+1
        if Variacion != 'Sin Variaciones':
            Variacion.Deactivate()
        m=m+1

    """"
    =========================================================================================
    """    



    Hora=Hora_Copia.copy()

    Resultados_Cargabilidades = pd.DataFrame(Diccionario_Cargabilidades)         
    Resultados_Tensiones = pd.DataFrame(Diccionario_Tensiones)
    Resultados_Perdidas= pd.DataFrame(Diccionario_Perdidas)
    Resultados_Cargabilidades_2 = pd.DataFrame(Diccionario_Cargabilidades_2)   

    Resultados_Tensiones_2=[]
    Titulos_Tensiones=[]
    df = pd.DataFrame(Diccionario_Tensiones_2)      
    for Fecha in Años:
        Año=str(int(Fecha))
        for j in Hora:
            for k in Escenarios:
                DataFrame=df.copy()
                Texto0='Nombre'
                Texto1= Año + str(j) + str(k) + 'C0V0_pu'
                Texto2= Año + str(j) + str(k) + 'C0V1_pu'
                Texto3= Año + str(j) + str(k) + 'C0V0_kV'
                Texto4= Año + str(j) + str(k) + 'C0V1_kV'
                DataFrame=DataFrame[[Texto0,Texto1,Texto2,Texto3,Texto4]]
                DataFrame['Diferencia porcentual pu']=(DataFrame[Texto2]-\
                    DataFrame[Texto1])/DataFrame[Texto1]
                Resultados_Tensiones_2.append(DataFrame)
                Titulos_Tensiones.append(Año + str(j) + str(k))
                

    tamaño_maximo = max(len(valores) for valores in Diccionario_Perdidas_2.values())
    for Llave, Valor in Diccionario_Perdidas_2.items():
        Diccionario_Perdidas_2[Llave] += [None] * (tamaño_maximo - len(Valor))
    df = pd.DataFrame(Diccionario_Perdidas_2)
    Resultados_Perdidas_2 = []
    Titulos_Perdidas=[]
    for Fecha in Años:
        Año=str(int(Fecha))
        for j in Hora:
            for k in Escenarios:
                Texto4=Año + str(j) + str(k) + 'C0V0_Nombre'
                Texto5=Año + str(j) + str(k) + 'C0V0_Loss'
                Texto6=Año + str(j) + str(k) + 'C0V0_P'
                Texto7=Año + str(j) + str(k) + 'C0V1_Nombre'
                Texto8=Año + str(j) + str(k) + 'C0V1_Loss'
                Texto9=Año + str(j) + str(k) + 'C0V1_P'
                merged_df = pd.merge(df[[Texto7, Texto8, Texto9]], 
                                    df[[Texto4, Texto5, Texto6]], 
                                    left_on=[Texto7], 
                                    right_on=[Texto4], 
                                    how='left')
                merged_df.drop(Texto4, axis=1, inplace=True)
                merged_df['Diferencia_Pérdidas']=merged_df[Texto8]-merged_df[Texto5]
                merged_df['Diferencia_Potencia']=merged_df[Texto9]-merged_df[Texto6]
                merged_df.rename(columns={Texto7: 'Nombre'}, inplace=True)
                Resultados_Perdidas_2.append(merged_df)
                Titulos_Perdidas.append(Año + str(j) + str(k))
                                

    app.PrintPlain('Exportando datos a Excel')

    with pd.ExcelWriter(Ruta_Excel +'\Flujo Carga.xlsx') as writer:
        Resultados_Cargabilidades.to_excel(writer, index=False, sheet_name='Cargabilidades')
        Resultados_Tensiones.to_excel(writer, index=False, sheet_name='Tensiones')
        Resultados_Cargabilidades_2.to_excel(writer, index=False, sheet_name='Cargabilidades_2')
        k=0
        for i in Resultados_Tensiones_2:
            Titulo=Titulos_Tensiones[k]
            i.to_excel(writer, index=False, sheet_name='Tensiones_' + Titulo)
            k=k+1
        
        Resultados_Perdidas.to_excel(writer, index=False, sheet_name='Perdidas')
        k=0
        for i in Resultados_Perdidas_2:
            Titulo=Titulos_Perdidas[k]
            i.to_excel(writer, index=False, sheet_name='Perdidas_' + Titulo)
            k=k+1

    app.PrintPlain('Resultados Exportados')   

