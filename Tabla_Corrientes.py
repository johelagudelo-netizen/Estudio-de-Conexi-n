def Funcion(df_Cabecera,df_PGF,Nodos_Corto,df_PGF_Tensiones):

    import pandas as pd
    import numpy as np
    import math
    # ruta_excel = r'F:\1. Camilo\1. Aplicación Estudios\Res Cordinación'
    # df_Cabecera = pd.read_excel(ruta_excel +'\Corto.xlsx', sheet_name='Cabecera')
    # Nodos_Corto=['F2', 'MT PGF', 'BT PGF']
    # df_PGF = pd.read_excel(ruta_excel +'\Corto.xlsx', sheet_name='PGF')
    
    def Ordenar_Tablas(df_PGF_F,df_Cabecera_F):
        Diccionario={'Nodo Bajo Falla':[],\
                    'Resistencia (Ohm)':[],\
                    'Corriente Falla Relé Parque Solar(A)':[],\
                    'Corriente Falla Relé Cabecera(A)':[]}
        for i, j in df_PGF_F.iterrows():
            lista_indices = j.index.tolist()
            k= lista_indices.index('Resistencia')
            Nodos=lista_indices[k + 1:]
            Corrientes=j[Nodos].tolist()
            Diccionario['Nodo Bajo Falla'].extend(Nodos)
            Diccionario['Corriente Falla Relé Parque Solar(A)'].extend(Corrientes)
            for m in range(len(Nodos)):
                Diccionario['Resistencia (Ohm)'].append(j['Resistencia'])
        for i, j in df_Cabecera_F.iterrows():
            lista_indices = j.index.tolist()
            k= lista_indices.index('Resistencia')
            Nodos=lista_indices[k + 1:]
            Corrientes=j[Nodos].tolist()
            Diccionario['Corriente Falla Relé Cabecera(A)'].extend(Corrientes)
        
        Frame=pd.DataFrame(Diccionario)    
        return(Frame)
    
    def Ordenar_Tablas_Tension(df,Nodos_Corto):
        Diccionario={'Nodo Bajo Falla':[],\
                    'Resistencia (Ohm)':[],\
                    'Tensión sensada Rele Parque Solar (pu) - Fase A':[],\
                    'Tensión sensada Rele Parque Solar (pu) - Fase B':[],\
                        'Tensión sensada Rele Parque Solar (pu) - Fase C':[],\
                        'Tensión sensada Rele Parque Solar (pu) - Residual':[]}
        Resistencias=df['Resistencia']
        for i in Resistencias:
            for j in Nodos_Corto:
                Diccionario['Nodo Bajo Falla'].append(j)
                Diccionario['Resistencia (Ohm)'].append(i)
                Indice=df[df['Resistencia'] == i].index.values[0]
                Tension_A=df.at[Indice , j + '_Tension_A']
                Tension_B=df.at[Indice , j + '_Tension_B']
                Tension_C=df.at[Indice , j + '_Tension_C']
                Tension_N=df.at[Indice , j + '_Tension_N']
                Diccionario['Tensión sensada Rele Parque Solar (pu) - Fase A'].append(Tension_A)
                Diccionario['Tensión sensada Rele Parque Solar (pu) - Fase B'].append(Tension_B)
                Diccionario['Tensión sensada Rele Parque Solar (pu) - Fase C'].append(Tension_C)
                Diccionario['Tensión sensada Rele Parque Solar (pu) - Residual'].append(Tension_N)
        Frame=pd.DataFrame(Diccionario)
        return(Frame)    

    
    
    for i in Nodos_Corto:
        df_Cabecera[i + '_RAD_A'] = df_Cabecera[i + '_DEG_A'].apply(lambda x: math.radians(x))
        df_Cabecera[i + '_RAD_B'] = df_Cabecera[i + '_DEG_B'].apply(lambda x: math.radians(x))
        df_Cabecera[i + '_RAD_C'] = df_Cabecera[i + '_DEG_C'].apply(lambda x: math.radians(x))
        df_PGF[i + '_RAD_A'] = df_PGF[i + '_DEG_A'].apply(lambda x: math.radians(x))
        df_PGF[i + '_RAD_B'] = df_PGF[i + '_DEG_B'].apply(lambda x: math.radians(x))
        df_PGF[i + '_RAD_C'] = df_PGF[i + '_DEG_C'].apply(lambda x: math.radians(x))
        
    for i in Nodos_Corto:
        df_Cabecera[ i + '_COM_A'] = df_Cabecera[ i + '_MAG_A'] *\
            (df_Cabecera[i + '_RAD_A'].apply(lambda x: math.cos(x))\
             + 1j * df_Cabecera[i + '_RAD_A'].apply(lambda x: math.sin(x)))
        
        df_Cabecera[ i + '_COM_B'] = df_Cabecera[ i + '_MAG_B'] *\
            (df_Cabecera[i + '_RAD_B'].apply(lambda x: math.cos(x))\
             + 1j * df_Cabecera[i + '_RAD_B'].apply(lambda x: math.sin(x)))
        
        df_Cabecera[ i + '_COM_C'] = df_Cabecera[ i + '_MAG_C'] *\
            (df_Cabecera[i + '_RAD_C'].apply(lambda x: math.cos(x))\
             + 1j * df_Cabecera[i + '_RAD_C'].apply(lambda x: math.sin(x)))
                
        df_PGF[ i + '_COM_A'] = df_PGF[ i + '_MAG_A'] *\
            (df_PGF[i + '_RAD_A'].apply(lambda x: math.cos(x))\
             + 1j * df_PGF[i + '_RAD_A'].apply(lambda x: math.sin(x)))
        
        df_PGF[ i + '_COM_B'] = df_PGF[ i + '_MAG_B'] *\
            (df_PGF[i + '_RAD_B'].apply(lambda x: math.cos(x))\
             + 1j * df_PGF[i + '_RAD_B'].apply(lambda x: math.sin(x)))
        
        df_PGF[ i + '_COM_C'] = df_PGF[ i + '_MAG_C'] *\
            (df_PGF[i + '_RAD_C'].apply(lambda x: math.cos(x))\
             + 1j * df_PGF[i + '_RAD_C'].apply(lambda x: math.sin(x)))
    
    
    
    
    df_Cabecera_3psc_G = df_Cabecera[df_Cabecera['Tipo'] == '3psc']
    df_Cabecera_2psc_G = df_Cabecera[df_Cabecera['Tipo'] == '2psc']
    df_Cabecera_spgf_G = df_Cabecera[df_Cabecera['Tipo'] == 'spgf']
    
    
    df_PGF_3psc_G = df_PGF[df_PGF['Tipo'] == '3psc']
    df_PGF_2psc_G = df_PGF[df_PGF['Tipo'] == '2psc']
    df_PGF_spgf_G = df_PGF[df_PGF['Tipo'] == 'spgf']


    df_PGF_Tensiones_3psc=df_PGF_Tensiones[df_PGF_Tensiones['Tipo'] == '3psc']
    df_PGF_Tensiones_2psc=df_PGF_Tensiones[df_PGF_Tensiones['Tipo'] == '2psc']
    df_PGF_Tensiones_spgf=df_PGF_Tensiones[df_PGF_Tensiones['Tipo'] == 'spgf']

    Lista_Frames_Tensiones=[df_PGF_Tensiones_3psc,df_PGF_Tensiones_2psc,df_PGF_Tensiones_spgf]

    
    df_Cabecera_Fase=df_Cabecera.copy()
    df_PGF_Fase=df_PGF.copy()
    Lista_Columnas=['Tipo','Resistencia']
    
    
    for i in Nodos_Corto:
        df_Cabecera_Fase[i] = df_Cabecera_Fase.apply(lambda row:\
                                    max(row[i + '_MAG_A'],\
                                    row[i + '_MAG_B'], row[i + '_MAG_C']), axis=1)
        Lista_Columnas.append(i)
        
            
    for i in Nodos_Corto:
        df_PGF_Fase[i] = df_PGF_Fase.apply(lambda row:\
                                    max(row[i + '_MAG_A'],\
                                    row[i + '_MAG_B'], row[i + '_MAG_C']), axis=1)
    
    df_PGF_Fase = df_PGF_Fase[Lista_Columnas]
    df_Cabecera_Fase = df_Cabecera_Fase[Lista_Columnas]
    
    for i in Nodos_Corto:
        df_Cabecera_3psc_G[i]=0
        df_PGF_3psc_G[i]=0
    df_Cabecera_3psc_G=df_Cabecera_3psc_G[Lista_Columnas]
    df_PGF_3psc_G=df_PGF_3psc_G[Lista_Columnas]
    
    
    
    Lista_Columnas=['Tipo','Resistencia']
    for i in Nodos_Corto:
        df_Cabecera_2psc_G[i]=df_Cabecera_2psc_G[i + '_COM_A'] +\
                       df_Cabecera_2psc_G[i + '_COM_B'] +\
                           df_Cabecera_2psc_G[i + '_COM_C'] 
        df_Cabecera_2psc_G[i] = df_Cabecera_2psc_G[i].apply(abs)
        
        df_Cabecera_spgf_G[i]=df_Cabecera_spgf_G[i + '_COM_A'] +\
                       df_Cabecera_spgf_G[i + '_COM_B'] +\
                           df_Cabecera_spgf_G[i + '_COM_C'] 
        df_Cabecera_spgf_G[i] = df_Cabecera_spgf_G[i].apply(abs)
        
        df_PGF_2psc_G[i]=df_PGF_2psc_G[i + '_COM_A'] +\
                       df_PGF_2psc_G[i + '_COM_B'] +\
                           df_PGF_2psc_G[i + '_COM_C'] 
        df_PGF_2psc_G[i] = df_PGF_2psc_G[i].apply(abs)
        
        df_PGF_spgf_G[i]=df_PGF_spgf_G[i + '_COM_A'] +\
                       df_PGF_spgf_G[i + '_COM_B'] +\
                           df_PGF_spgf_G[i + '_COM_C'] 
        df_PGF_spgf_G[i] = df_PGF_spgf_G[i].apply(abs)
        
        Lista_Columnas.append(i)
                           
    df_Cabecera_spgf_G=df_Cabecera_spgf_G[Lista_Columnas]
    df_Cabecera_2psc_G=df_Cabecera_2psc_G[Lista_Columnas]
    
    df_PGF_spgf_G=df_PGF_spgf_G[Lista_Columnas]
    df_PGF_2psc_G=df_PGF_2psc_G[Lista_Columnas]
    
    df_Cabecera_G=pd.concat([df_Cabecera_3psc_G,\
                          df_Cabecera_2psc_G,df_Cabecera_spgf_G],\
                            ignore_index=True)
    
    df_PGF_G=pd.concat([df_PGF_3psc_G,\
                          df_PGF_2psc_G,df_PGF_spgf_G],\
                            ignore_index=True)
    
        
    df_Cabecera_3psc_F = df_Cabecera_Fase[df_Cabecera['Tipo'] == '3psc']
    df_Cabecera_2psc_F = df_Cabecera_Fase[df_Cabecera['Tipo'] == '2psc']
    df_Cabecera_spgf_F = df_Cabecera_Fase[df_Cabecera['Tipo'] == 'spgf']
    
    
    df_PGF_3psc_F = df_PGF_Fase[df_PGF['Tipo'] == '3psc']
    df_PGF_2psc_F = df_PGF_Fase[df_PGF['Tipo'] == '2psc']
    df_PGF_spgf_F = df_PGF_Fase[df_PGF['Tipo'] == 'spgf']


    
    
    F3CC_Fase=Ordenar_Tablas(df_PGF_3psc_F,df_Cabecera_3psc_F)
    F2CC_Fase=Ordenar_Tablas(df_PGF_2psc_F,df_Cabecera_2psc_F)
    F1CC_Fase=Ordenar_Tablas(df_PGF_spgf_F,df_Cabecera_spgf_F)
    F3CC_Tierra=Ordenar_Tablas(df_PGF_3psc_G,df_Cabecera_3psc_G)
    F2CC_Tierra=Ordenar_Tablas(df_PGF_2psc_G,df_Cabecera_2psc_G)
    F1CC_Tierra=Ordenar_Tablas(df_PGF_spgf_G,df_Cabecera_spgf_G)





    F3CC_Tensiones=Ordenar_Tablas_Tension(df_PGF_Tensiones_3psc,Nodos_Corto)
    F2CC_Tensiones=Ordenar_Tablas_Tension(df_PGF_Tensiones_2psc,Nodos_Corto)
    F1CC_Tensiones=Ordenar_Tablas_Tension(df_PGF_Tensiones_spgf,Nodos_Corto)


    
    Lista_Frames=[F3CC_Fase,F2CC_Fase,F1CC_Fase,F3CC_Tierra,F2CC_Tierra,F1CC_Tierra]

    Lista_Frames_Tensiones=[F3CC_Tensiones,F2CC_Tensiones,F1CC_Tensiones]
    
    return(Lista_Frames,Lista_Frames_Tensiones)
        
        

    
    
    
