def Funcion(Fichero):
    import sys
    import config_powerfactory  # ruta de PowerFactory: ver config_powerfactory.py
    import powerfactory as pf 
    import pandas as pd
    app = pf.GetApplication()
    Diccionario={}
    dataframe = pd.read_excel(Fichero, sheet_name='Char_Tiempo')
    dataframe = dataframe.dropna(axis=1, how='all')
    numero_de_columnas = dataframe.shape[1]
    Folder_Caracteristicas = app.GetProjectFolder('chars')

    horas = list(range(24))

    df = pd.DataFrame({'Hora': horas})
    Potencia_Maxima_Circuito=pd.DataFrame()

    for i in range(1,numero_de_columnas):
        nombre_columna = dataframe.columns[i]
        Caracteristicas_Tiempo=Folder_Caracteristicas.GetContents(nombre_columna + '.ChaTime')
        if  not Caracteristicas_Tiempo:
            Caracteristicas_Tiempo= Folder_Caracteristicas.CreateObject\
                                                ('ChaTime',nombre_columna)
            Caracteristicas_Tiempo.source=0
            Caracteristicas_Tiempo.repeat=0
            Caracteristicas_Tiempo.cunit=1
            Caracteristicas_Tiempo.usage=1
            df[nombre_columna]=dataframe[nombre_columna]/abs(dataframe[nombre_columna]).max()
            Lista = df[nombre_columna].values.tolist()
            try:
                Caracteristicas_Tiempo.vector=Lista
            except:
                print("Error de tiempos")


