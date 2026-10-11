def Funcion(Lista_Frame,Pt_Cabecera,Pt_Curva_PGF,Delta_Fase,Delta_Tierra):
    import pandas as pd
    import sys
    sys.path.append(r'C:\Program Files\DIgSILENT\PowerFactory 2021 SP2\Python\3.9')
    import powerfactory as pf
    app = pf.GetApplication()
    Folder_Variaciones=app.GetProjectFolder('scheme')
    Variacion=Folder_Variaciones.GetContents(Pt_Curva_PGF.Variacion + '.IntScheme')[0]
    #Variacion=app.GetActiveNetworkVariations()[0]
    Expansion=Variacion.GetContents('*.IntSstage')[0]
    try:    
        Generador=Expansion.GetContents('*.ElmGenstat')[0]
        Potencia=Generador.sgn
    except:
        print('No es un Generador Estatico')
    try:
        Generador=Expansion.GetContents('*.ElmSym')[0]
        Tipo_Generador=Generador.typ_id
        Potencia=Tipo_Generador.sgn
    except:
        print('No es una maquina sincrona')

    Nodo_Mt_OR=app.GetCalcRelevantObjects(Pt_Curva_PGF.Barra_MT_OR + '.ElmTerm')[0]
    Tension=Nodo_Mt_OR.uknom

    F3CC_Fase= Lista_Frame[0]
    F2CC_Fase= Lista_Frame[1]
    F1CC_Fase= Lista_Frame[2]
    F3CC_Tierra= Lista_Frame[3]
    F2CC_Tierra= Lista_Frame[4]
    F1CC_Tierra= Lista_Frame[5]
    Lista_Frames_Fase=[F3CC_Fase,F2CC_Fase,F1CC_Fase]
    Lista_Frames_Tierra=[F3CC_Tierra,F2CC_Tierra,F1CC_Tierra]
    Curva51F=Pt_Cabecera.Curva51F
    Curva51N=Pt_Cabecera.Curva51N
    Dial51F=Pt_Cabecera.Dial51F
    Dial51N=Pt_Cabecera.Dial51N
    Pick_up51F=Pt_Cabecera.Pick_up51F
    Pick_up51N=Pt_Cabecera.Pick_up51N
    Pick_up50F=Pt_Cabecera.Pick_up50F
    Pick_up50N=Pt_Cabecera.Pick_up50N
    Delay_Instantanea_Fase=Pt_Cabecera.Delay_Instantanea_Fase
    Delay_Instantanea_Tierra=Pt_Cabecera.Delay_Instantanea_Tierra

    Dial51F=float(Dial51F)
    Dial51N=float(Dial51N)
    Pick_up51F=float(Pick_up51F)
    Pick_up51N=float(Pick_up51N)
    Pick_up50F=float(Pick_up50F)
    Pick_up50N=float(Pick_up50N)
    Delay_Instantanea_Fase=float(Delay_Instantanea_Fase)
    Delay_Instantanea_Tierra=float(Delay_Instantanea_Tierra)
    
    Pick_up51F_PGF=1e6*Potencia/((3**0.5)*Tension*1e3)*1.1
    Pick_up51N_PGF=Pick_up51F_PGF*0.2
    Pick_up51F_PGF = round(Pick_up51F_PGF, 2)
    Pick_up51N_PGF = round(Pick_up51N_PGF, 3)

    Estandar={'VI_IEC':'IEC Muy Inversa',
                    'NI_IEC':'IEC Normalmente Inversa',
                    'EI_IEC':'IEC Extremadamente Inversa',
                    'NI_IEEE':'IEEE Normalmente Inversa',
                    'EI_IEEE':'IEEE Extremadamente Inversa',
                    'VI_IEEE':'IEEE Muy Inversa',
                    'EI_ANSI':'ANSI Extremadamente Inversa',
                    'VI_ANSI': 'ANSI Muy Inversa',
                    'NI_ANSI': 'ANSI Normalmente Inversa',
                    'TLI_ANSI': 'ANSI Tiempo Largo Inversa',
                    'TLVI_ANSI': 'ANSI Tiempo Largo Muy Inversa',
                    'TLEI_ANSI': 'ANSI Tiempo Largo Extremadamente Inversa',
                    'ITC_ANSI': 'ANSI Inversa Tiempo Corto',
                    'EITC_ANSI': 'ANSI Extremadametbte Inversa Tiempo Corto' }

    Diccionario_Curvas={
                'VI_IEC':[13.5,1,0],\
                'NI_IEC':[0.14,0.02,0],\
                'EI_IEC':[80,2,0],\
                'VI_IEEE':[19.61,2,0.491],\
                'NI_IEEE':[0.0515,0.02,0.114],\
                'EI_IEEE':[28.2,2,0.1217],\
                'EI_ANSI':[6.407, 2, 0.025],\
                'VI_ANSI': [2.855, 2,0.0712],\
                'NI_ANSI': [0.0086, 0.02,0.00185],\
                'TLI_ANSI': [0.086, 0.02, 0.185],\
                'TLVI_ANSI': [28.55,2,0.712],\
                'TLEI_ANSI': [64.07,2,0.25],\
                'ITC_ANSI': [0.00172,0.02,0.0037],
                'EITC_ANSI': [1.281,2,0.005]}   
    Tipo51F=Curva51F
    a = Diccionario_Curvas[Tipo51F][0]
    n = Diccionario_Curvas[Tipo51F][1]
    b = Diccionario_Curvas[Tipo51F][2]
    Tiempos_Cordinacion_Fase_OR=[]
    for i in Lista_Frames_Fase:
        Tiempo=[]
        for indice, j in i.iterrows():
            Corriente=j['Corriente Falla Relé Cabecera(A)']
            if Corriente<Pick_up51F:
                Tiempo.append('No Opera')
            elif Corriente>Pick_up50F:
                Tiempo.append(Delay_Instantanea_Fase)
                Tiempos_Cordinacion_Fase_OR.append(Delay_Instantanea_Fase)
            else:
                Val=  ((a*Dial51F)  / (((Corriente / Pick_up51F) ** n) - 1))+b
                Tiempos_Cordinacion_Fase_OR.append(Val)
                Tiempo.append(Val)
                print('Hola Mundo')
        i['Tiempo Actuación Rele Cabecera (S)']=Tiempo
    try:
        Tiempo_Minimo_Fase_OR=min(Tiempos_Cordinacion_Fase_OR)
    except:
        Tiempo_Minimo_Fase_OR=2
        
    Tipo51N=Curva51N
    a = Diccionario_Curvas[Tipo51N][0]
    n = Diccionario_Curvas[Tipo51N][1]
    b = Diccionario_Curvas[Tipo51N][2]
    Tiempos_Cordinacion_Tierra_OR=[]
    for i in Lista_Frames_Tierra:
        Tiempo=[]
        for indice, j in i.iterrows():
            Corriente=j['Corriente Falla Relé Cabecera(A)']
            if Corriente<Pick_up51N:
                Tiempo.append('No Opera')
            elif Corriente>Pick_up50N:
                Tiempo.append(Delay_Instantanea_Tierra)
                Tiempos_Cordinacion_Tierra_OR.append(Delay_Instantanea_Tierra)
            else:
                Val=  ((a*Dial51N)   / (((Corriente / Pick_up51N) ** n) - 1))+b
                Tiempos_Cordinacion_Tierra_OR.append(Val)
                Tiempo.append(Val)
                print('Hola Mundo')
        i['Tiempo Actuación Rele Cabecera (S)']=Tiempo
    try:
        Tiempo_Minimo_Tierra_OR=min(Tiempos_Cordinacion_Tierra_OR)
    except:
        Tiempo_Minimo_Tierra_OR=2

    # Establecer parámetros cordinación PGF Fase
    Tipo51F=Curva51F
    a = Diccionario_Curvas[Tipo51F][0]
    n = Diccionario_Curvas[Tipo51F][1]
    b = Diccionario_Curvas[Tipo51F][2]
    


    Tiempo_Cordinacion_Fase=Tiempo_Minimo_Fase_OR- float(Delta_Fase)

    Maximos=[]
    for i in Lista_Frames_Fase:
        Maximos.append(i['Corriente Falla Relé Parque Solar(A)'].max())
    Max_Corriente_Fase=max(Maximos)
    Dial51F_PGF=(Tiempo_Cordinacion_Fase-b)*(((Max_Corriente_Fase/Pick_up51F_PGF)**n)-1)/a

    for i in Lista_Frames_Fase:
        Tiempo=[]
        for indice, j in i.iterrows():
            Corriente=j['Corriente Falla Relé Parque Solar(A)']
            if Corriente<Pick_up51F_PGF:
                Tiempo.append('No Opera')
            else:
                Tiempo.append( ((a * Dial51F_PGF) / (((Corriente / Pick_up51F_PGF) ** n) - 1))+b)
        i['Tiempo Actuación Rele Parque Solar(S)']=Tiempo
        

    # Establecer parámetros cordinación PGF Tierra
    Tipo51N=Curva51N
    a = Diccionario_Curvas[Tipo51N][0]
    n = Diccionario_Curvas[Tipo51N][1]
    b = Diccionario_Curvas[Tipo51N][2]
    Tiempo_Cordinacion_Tierra=Tiempo_Minimo_Tierra_OR- float(Delta_Tierra)

    Maximos=[]
    for i in Lista_Frames_Tierra:
        Maximos.append(i['Corriente Falla Relé Parque Solar(A)'].max())
    Max_Corriente_Tierra=max(Maximos)
    Dial51N_PGF=(Tiempo_Cordinacion_Tierra-b)*(((Max_Corriente_Tierra/Pick_up51N_PGF)**n)-1)/a

    for i in Lista_Frames_Tierra:
        Tiempo=[]
        for indice, j in i.iterrows():
            Corriente=j['Corriente Falla Relé Parque Solar(A)']
            if Corriente<Pick_up51N_PGF:
                Tiempo.append('No Opera')
            else:
                Tiempo.append( ((a * Dial51N_PGF) / (((Corriente / Pick_up51N_PGF) ** n) - 1))+b)
                print('Hola Mundo')
        i['Tiempo Actuación Rele Parque Solar(S)']=Tiempo
    
    Diccionario_Curvas_PGF={'Dial51F_PGF':Dial51F_PGF,'Dial51N_PGF':Dial51N_PGF,\
                            'Pick_up51F_PGF':Pick_up51F_PGF,'Pick_up51N_PGF':Pick_up51N_PGF}
    return(Lista_Frames_Fase,Lista_Frames_Tierra,Diccionario_Curvas_PGF)



