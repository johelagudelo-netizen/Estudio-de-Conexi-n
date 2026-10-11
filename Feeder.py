def Funcion(Fichero):
    import sys
    import config_powerfactory  # ruta de PowerFactory: ver config_powerfactory.py
    import powerfactory as pf
    import pandas as pd
    app = pf.GetApplication()
    Nodo_Alimentador= pd.read_excel(Fichero, sheet_name='Alimentador')
    Nodo_Alimentador = Nodo_Alimentador.dropna(axis=1, how='all')
    Valor=Nodo_Alimentador['Nombre'][0]
    print(Valor)


    Folder_Feeder = app.GetDataFolder('ElmFeeder')

    Nodo=app.GetCalcRelevantObjects(Valor + '.ElmTerm')[0]
    Feeder=Folder_Feeder.CreateObject('ElmFeeder', 'Feeder_Proyecto')
    Feeder.irVolt=0
    Feeder.ilVolt=0
    Feeder.operRadial=1
    Nombre_Feeder=Feeder.loc_name


    Cub=Nodo.GetContents()[0]
    Feeder.obj_id=Cub
    Herramienta_Graficos=app.GetFromStudyCase('ComSgllayout')
    Herramienta_Graficos.iAction=0
    Herramienta_Graficos.iGenType=3
    Herramienta_Graficos.pFeeders=Feeder
    Herramienta_Graficos.Execute()
    Folder_Diagramas=app.GetProjectFolder('dia')
    Grafico_Feeder=Folder_Diagramas.GetContents(Nombre_Feeder + '.IntGrfnet')[0]
    Grafico_Grid=Folder_Diagramas.GetContents('Grid.IntGrfnet')[0]
    Carpetas_Grid=Grafico_Grid.GetContents('*.IntFolder')
    Carpetas_Grid=Grafico_Grid.GetContents()
    #range(len(Carpetas_Grid))
    for i in Carpetas_Grid:
        i.Delete()
    Elementos_Graficos=Grafico_Feeder.GetContents()
    Grafico_Grid.PasteCopy(Elementos_Graficos)


    Conectados=Nodo.GetConnectedElements()
    Grafico_Nodo_AL=Grafico_Grid.GetContents(Valor + '_Graph.IntGrf')[0]
    X_Grafico_Nodo_AL=Grafico_Nodo_AL.GetAttribute('rCenterX')
    Y_Grafico_Nodo_AL=Grafico_Nodo_AL.GetAttribute('rCenterY')
    for i in Conectados:
        Tipo=i.GetClassName()
        Nombre=i.GetAttribute('loc_name')
        if Tipo == 'ElmLod':
            Nueva_Carga_grafico=Grafico_Grid.CreateObject('IntGrf',Nombre)
            Nueva_Carga_grafico.rCenterX=X_Grafico_Nodo_AL
            Nueva_Carga_grafico.rCenterY=Y_Grafico_Nodo_AL
            Nueva_Carga_grafico.pDataObj=i
            Nueva_Carga_grafico.sSymNam='d_load'
            Nueva_Carga_grafico.iRot=0




