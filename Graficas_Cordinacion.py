def Funcion(Lista_Frames_Fase,Lista_Frames_Tierra,\
                                    Proteccion_Cabecera,Nombre_Directorio_Protecciones,\
                                        Diccionario_Curvas_PGF):
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd


    #------- Tipo de Curvas------
        # [a , n]
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
    #------- Párametros Fase OR-------------------
    Tipo_51F_OR=Proteccion_Cabecera.Curva51F
    a_51F_OR = Diccionario_Curvas[Tipo_51F_OR][0]
    n_51F_OR = Diccionario_Curvas[Tipo_51F_OR][1]
    b_51F_OR = Diccionario_Curvas[Tipo_51F_OR][2]
    Pick_up_51F_OR = float(Proteccion_Cabecera.Pick_up51F)
    Dial_51F_OR = float(Proteccion_Cabecera.Dial51F)
    Instantanea_50F_OR=float(Proteccion_Cabecera.Pick_up50F)
    Delay_50F_OR=float(Proteccion_Cabecera.Delay_Instantanea_Fase)


    #------- Párametros Tierra OR-------------------
    Tipo_51N_OR=Proteccion_Cabecera.Curva51N
    a_51N_OR = Diccionario_Curvas[Tipo_51N_OR][0]
    n_51N_OR = Diccionario_Curvas[Tipo_51N_OR][1]
    b_51N_OR = Diccionario_Curvas[Tipo_51N_OR][2]
    Pick_up_51N_OR = float(Proteccion_Cabecera.Pick_up51N)
    Dial_51N_OR = float(Proteccion_Cabecera.Dial51N)
    Instantanea_50N_OR=float(Proteccion_Cabecera.Pick_up50N)
    Delay_50N_OR=float(Proteccion_Cabecera.Delay_Instantanea_Tierra)


    #------- Párametros Fase PGF-------------------
    Tipo_51F_PGF=Proteccion_Cabecera.Curva51F
    a_51F_PGF = Diccionario_Curvas[Tipo_51F_PGF][0]
    n_51F_PGF = Diccionario_Curvas[Tipo_51F_PGF][1]
    b_51F_PGF = Diccionario_Curvas[Tipo_51F_PGF][2]
    Pick_up_51F_PGF = float(Diccionario_Curvas_PGF['Pick_up51F_PGF'])
    Dial_51F_PGF = float(Diccionario_Curvas_PGF['Dial51F_PGF'])

    #------- Párametros Tierra OR-------------------
    Tipo_51N_PGF=Proteccion_Cabecera.Curva51N
    a_51N_PGF = Diccionario_Curvas[Tipo_51N_PGF][0]
    n_51N_PGF = Diccionario_Curvas[Tipo_51N_PGF][1]
    b_51N_PGF = Diccionario_Curvas[Tipo_51N_PGF][2]
    Pick_up_51N_PGF = float(Diccionario_Curvas_PGF['Pick_up51N_PGF']) 
    Dial_51N_PGF= float(Diccionario_Curvas_PGF['Dial51N_PGF'])



    #--------- Funciones--------
    def Graficar(Diccionario,Titulo):
        
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

        plt.ioff() 
        fig = plt.figure(figsize=(6, 8))
        for Clave, Valor in Diccionario.items():
            t=Valor[0]
            I=Valor[1]
            x=10
            y=10
            Color=Valor[2]
            Nombre=Valor[3]
            pik_up = Valor[5]  # Pik-up
            dial = Valor[4]  # Dial
            Tipo = Valor[6]  # Tipo Curva
            
            if Tipo=='Corto':
                dial=round(dial,2)
                pik_up=round(pik_up,2)
                Etiqueta=f" ICC: {pik_up} A \n {Nombre} {dial} s"
                x=pik_up
                y=dial

            else:
                tipo_curva=Estandar[Tipo]
                Etiqueta = f"{Nombre}\n{tipo_curva}\n Pik-up: {pik_up}\n Dial: {dial}"
                x=I[10]
                y=t[10]
            plt.plot(I,t,color=Color, label=Etiqueta)
            # Etiquetas de los ejes
            plt.xlabel('Corriente (A)')
            plt.ylabel('Tiempo(s)')
            # Mostrar la gráfica
            plt.grid(True,which='both')
            plt.xscale('log')
            plt.yscale('log')
            plt.text(x, y, Etiqueta, fontdict={'size': 8, 'color': Color})
        plt.title(Titulo)  # Agregar título a la figura
        plt.close(fig) 
        return(fig)


    I_51F_OR = np.arange(Pick_up_51F_OR + 1, Instantanea_50F_OR)
    t_51F_OR =   ((Dial_51F_OR * a_51F_OR)   / (((I_51F_OR / Pick_up_51F_OR) ** n_51F_OR) - 1)) + b_51F_OR
    I_50F_OR=np.array([Instantanea_50F_OR,Instantanea_50F_OR,1E4])
    t_50F_OR=np.array([t_51F_OR[-1],Delay_50F_OR,Delay_50F_OR])
    I_F_OR=np.concatenate((I_51F_OR, I_50F_OR))
    t_F_OR=np.concatenate((t_51F_OR, t_50F_OR))
    Etiqueta_F_OR='Curva de Fase OR'
    Diccionario={'51F_OR':[t_F_OR,I_F_OR,'red',Etiqueta_F_OR,Dial_51F_OR,Pick_up_51F_OR,Tipo_51F_OR]}

    I_51N_OR = np.arange(Pick_up_51N_OR + 1, Instantanea_50N_OR)
    t_51N_OR =  ((Dial_51N_OR * a_51N_OR)   / (((I_51N_OR / Pick_up_51N_OR) ** n_51N_OR) - 1)) + b_51N_OR
    I_50N_OR=np.array([Instantanea_50N_OR,Instantanea_50N_OR,1E4])
    t_50N_OR=np.array([t_51N_OR[-1],Delay_50N_OR,Delay_50N_OR])
    I_N_OR=np.concatenate((I_51N_OR, I_50N_OR))
    t_N_OR=np.concatenate((t_51N_OR, t_50N_OR))
    Etiqueta_N_OR='Curva de Tierra OR'
    Diccionario['51N_OR']=[t_N_OR,I_N_OR,'red',Etiqueta_N_OR,Dial_51N_OR,Pick_up_51N_OR,Tipo_51N_OR]


    #I_51F_PGF = np.arange(Pick_up_51F_PGF + 1, Instantanea_50F_OR)
    I_51F_PGF = np.arange(Pick_up_51F_PGF + 1, 10000)
    t_51F_PGF =  ((Dial_51F_PGF * a_51F_PGF)  / (((I_51F_PGF / Pick_up_51F_PGF) ** n_51F_PGF) - 1)) + b_51F_PGF
    Etiqueta_F_PGF='Curva de Fase PGF'
    Diccionario['51F_PGF']=[t_51F_PGF,I_51F_PGF,'green',Etiqueta_F_PGF,Dial_51F_PGF,Pick_up_51F_PGF,Tipo_51F_PGF]


    #I_51N_PGF = np.arange(Pick_up_51N_PGF + 1, Instantanea_50N_OR)
    I_51N_PGF = np.arange(Pick_up_51N_PGF + 1, 10000)
    t_51N_PGF =  ((Dial_51N_PGF * a_51N_PGF )  / (((I_51N_PGF / Pick_up_51N_PGF) ** n_51N_PGF) - 1)) + b_51N_PGF
    Etiqueta_N_PGF='Curva de Tierra PGF'
    Diccionario['51N_PGF']=[t_51N_PGF,I_51N_PGF,'green',Etiqueta_N_PGF,Dial_51N_PGF,Pick_up_51N_PGF,Tipo_51N_PGF]

    Claves_Fase = ['51F_OR', '51F_PGF']

    Claves_Tierra = ['51N_OR', '51N_PGF']

    # Crear una copia del diccionario con sólo las claves especificadas
    Diccionario_Fase= {clave: Diccionario[clave] for clave in Claves_Fase if clave in Diccionario}
    Diccionario_Tierra= {clave: Diccionario[clave] for clave in Claves_Tierra if clave in Diccionario}
    Claves_Fase_OR = ['51F_OR']
    Claves_Fase_PGF = ['51F_PGF']
    Claves_Tierra_OR = ['51N_OR']
    Claves_Tierra_PGF = ['51N_PGF']
    Diccionario_Fase_OR={clave: Diccionario[clave] for clave in Claves_Fase_OR if clave in Diccionario}
    Diccionario_Fase_PGF={clave: Diccionario[clave] for clave in Claves_Fase_PGF if clave in Diccionario}
    Diccionario_Tierra_OR={clave: Diccionario[clave] for clave in Claves_Tierra_OR if clave in Diccionario}
    Diccionario_Tierra_PGF={clave: Diccionario[clave] for clave in Claves_Tierra_PGF if clave in Diccionario}


    # Graficar(Diccionario, 'Coordinación Protecciones de Sobrecorriente de Fase')
    # plt.show()

    Fig_Fase=[]
    Fig_Tierra=[]
    Fig_Fase.append(Graficar(Diccionario_Fase_OR, 'Coordinación Protecciones de Sobrecorriente de Fase OR'))
    Fig_Fase.append(Graficar(Diccionario_Fase_PGF, 'Coordinación Protecciones de Sobrecorriente de Fase PGF'))
    Fig_Tierra.append(Graficar(Diccionario_Tierra_OR, 'Coordinación Protecciones de Sobrecorriente de Tierra OR'))
    Fig_Tierra.append(Graficar(Diccionario_Tierra_PGF, 'Coordinación Protecciones de Sobrecorriente de Tierra PGF'))

    def Unir_Graficas(Fig1, Fig2, Titulo):
        ax1 = Fig1.get_axes()[0]

        # Obtener los datos de línea y de texto de la primera gráfica
        lines1 = ax1.get_lines()
        texts1 = ax1.texts

        # Obtener los ejes de la segunda gráfica
        ax2 = Fig2.get_axes()[0]

        # Obtener los datos de línea y de texto de la segunda gráfica
        lines2 = ax2.get_lines()
        texts2 = ax2.texts
        # Crear una nueva figura y un nuevo objeto ax
        plt.ioff() 
        Fig3 = plt.figure(figsize=(10, 12)) 
        ax3 = Fig3.add_subplot(111)
        plt.xlabel('Corriente (A)')
        plt.ylabel('Tiempo(s)')
        plt.grid(True,which='both')
        plt.xscale('log')
        plt.yscale('log')
        plt.title(Titulo)
        ax3.set_xlim(10, 1e4)
        ax3.set_ylim(0.005, 1e2)
        plt.close(Fig3)
        # Añadir las líneas y los datos de texto de la primera gráfica a la nueva gráfica
        for line in lines1:
            ax3.plot(line.get_xdata(), line.get_ydata(), color=line.get_color(),
                    marker=line.get_marker(), markeredgecolor=line.get_markeredgecolor(),
                    markersize=line.get_markersize(), linestyle=line.get_linestyle(),
                    label=line.get_label())

        for text in texts1:
            x, y = text.get_position()
            ax3.text(x, y, text.get_text(), color=text.get_color(),
                    fontsize=text.get_fontsize(), fontweight=text.get_fontweight())

        # Añadir las líneas y los datos de texto de la segunda gráfica a la nueva gráfica
        for line in lines2:
            ax3.plot(line.get_xdata(), line.get_ydata(), color=line.get_color(),
                    marker=line.get_marker(), markeredgecolor=line.get_markeredgecolor(),
                    markersize=line.get_markersize(), linestyle=line.get_linestyle(),
                    label=line.get_label())
        for text in texts2:
            x, y = text.get_position()
            ax3.text(x, y, text.get_text(), color=text.get_color(),
                    fontsize=text.get_fontsize(), fontweight=text.get_fontweight())
        plt.close(Fig1)  # Cerrar la primera figura
        plt.close(Fig2)  # Cerrar la segunda figura
        plt.close(Fig3)  # Cerrar la figura resultante
        return Fig3

    ruta_excel = Nombre_Directorio_Protecciones
    if Proteccion_Cabecera.V51F==1:
        Figura1=Unir_Graficas(Fig_Fase[0],Fig_Fase[1],'Coordinación Protecciones de Fase')
    else:
        Figura1=Fig_Fase[1]
    Figura1.savefig( ruta_excel + '\Figura1.png', bbox_inches='tight')
    plt.close(Figura1)
    if Proteccion_Cabecera.V51N==1:
        Figura2=Unir_Graficas(Fig_Tierra[0],Fig_Tierra[1],'Coordinación Protecciones de Tierra')
        plt.close(Figura2)
    else:
        Figura2=Unir_Graficas(Fig_Tierra[1],Fig_Tierra[1],'Coordinación Protecciones de Sobrecorriente de Tierra PGF')
    Figura2.savefig( ruta_excel + '\Figura2.png', bbox_inches='tight')
    plt.close(Figura2)

    Diccionario_Falla_OR={}
    Diccionario_Falla_PGF={}
    Lista_Fallas=['Trifásica','Bifásica','Monofásica']
    k=0
    m=2
    for i in Lista_Frames_Fase:
        for Indice, j in i.iterrows():
            T_OR=j['Tiempo Actuación Rele Cabecera (S)']
            I_OR=j['Corriente Falla Relé Cabecera(A)']
            Resistencia=j['Resistencia (Ohm)']
            I=np.array([I_OR,I_OR])
            t=np.array([0,100])
            Nodo=j['Nodo Bajo Falla']
            Tipo=Lista_Fallas[k]
            if T_OR!='No Opera':
                T_OR=round(T_OR, 2)
                Diccionario_Falla_OR['Falla']=[t,I,'magenta','Disparo OR',\
                                                T_OR ,I_OR,'Corto']
                Fig_Corto=Graficar(Diccionario_Falla_OR, ' ')
                Figura1=Unir_Graficas(Fig_Corto,Fig_Fase[0],\
                        'Disparo Relé OR - Falla ' + Tipo + ' - Nodo ' + str(Nodo) + ' - Resistencia Falla: ' + str(Resistencia))
                
            T_PGF=j['Tiempo Actuación Rele Parque Solar(S)']
            I_PGF=j['Corriente Falla Relé Parque Solar(A)']
            I=np.array([I_PGF,I_PGF])
            t=np.array([0,100])
            if T_PGF!='No Opera':
                T_PGF=round(T_PGF, 2)
                Diccionario_Falla_PGF['Falla']=[t,I,'magenta','Disparo PGF',\
                                                T_PGF ,I_PGF,'Corto']
                Fig_Corto2=Graficar(Diccionario_Falla_PGF, ' ')
                Figura2=Unir_Graficas(Fig_Corto2,Fig_Fase[1],\
                        'Disparo Relé PGF - Falla ' + Tipo + ' - Nodo ' + str(Nodo) + ' - Resistencia Falla: ' + str(Resistencia))
            if I_PGF>(0.975*I_OR) and I_PGF<(1.025*I_OR) and T_OR!='No Opera' and T_PGF!='No Opera':
                Figura3=Unir_Graficas(Figura1,Figura2,\
                    'Disparos Sistema Cordinación de Protección - Falla ' + Tipo + ' - Nodo ' + str(Nodo) + ' - Resistencia Falla: ' + str(Resistencia))
                m=m+1
                Figura3.savefig( ruta_excel + '\Figura' + str(m) + '.png', bbox_inches='tight')
                plt.close(Figura3)
            else:
                if T_OR!='No Opera':
                    m=m+1
                    Figura1.savefig( ruta_excel + '\Figura' + str(m) + '.png', bbox_inches='tight')
                    plt.close(Figura1)
                if T_PGF!='No Opera':
                    m=m+1
                    Figura2.savefig( ruta_excel + '\Figura' + str(m) + '.png', bbox_inches='tight')
                    plt.close(Figura2)
        k=k+1
        plt.close('all') 
        
    k=0

    for i in Lista_Frames_Tierra:
        for Indice, j in i.iterrows():
            T_OR=j['Tiempo Actuación Rele Cabecera (S)']
            I_OR=j['Corriente Falla Relé Cabecera(A)']
            Resistencia=j['Resistencia (Ohm)']
            I=np.array([I_OR,I_OR])
            t=np.array([0,100])
            Nodo=j['Nodo Bajo Falla']
            Tipo=Lista_Fallas[k]
            if T_OR!='No Opera':
                T_OR=round(T_OR, 2)
                Diccionario_Falla_OR['Falla']=[t,I,'magenta','Disparo OR',\
                                            T_OR ,I_OR,'Corto']
                Fig_Corto=Graficar(Diccionario_Falla_OR, ' ')
                Figura1=Unir_Graficas(Fig_Corto,Fig_Tierra[0],\
                        'Disparo Relé OR - Falla ' + Tipo + ' - Nodo ' + str(Nodo) +\
                              ' - Resistencia Falla: ' + str(Resistencia) + 'Ohm')
                
            T_PGF=j['Tiempo Actuación Rele Parque Solar(S)']
            I_PGF=j['Corriente Falla Relé Parque Solar(A)']
            I=np.array([I_PGF,I_PGF])
            t=np.array([0,100])
            if T_PGF!='No Opera':
                T_PGF=round(T_PGF, 2)
                Diccionario_Falla_PGF['Falla']=[t,I,'magenta','Disparo PGF',\
                                            T_PGF ,I_PGF,'Corto']
                Fig_Corto2=Graficar(Diccionario_Falla_PGF, ' ')
                Figura2=Unir_Graficas(Fig_Corto2,Fig_Tierra[1],\
                        'Disparo Relé PGF - Falla ' + Tipo + ' - Nodo ' + str(Nodo) +\
                              ' - Resistencia Falla: ' + str(Resistencia) + 'Ohm')
            if I_PGF>(0.99*I_OR) and I_PGF<(1.01*I_OR) and T_OR!='No Opera' and T_PGF!='No Opera' :
                Figura3=Unir_Graficas(Figura1,Figura2,\
                    'Disparos Sistema Cordinación de Protección - Falla ' + Tipo + ' - Nodo ' + str(Nodo) +\
                          ' - Resistencia Falla: ' + str(Resistencia) + 'Ohm')
                m=m+1
                Figura3.savefig( ruta_excel + '\Figura' + str(m) + '.png', bbox_inches='tight')
                plt.close(Figura3)
            else:
                if T_OR!='No Opera':
                    m=m+1
                    Figura1.savefig( ruta_excel + '\Figura' + str(m) + '.png', bbox_inches='tight')
                    plt.close(Figura1)
                if T_PGF!='No Opera':
                    m=m+1
                    Figura2.savefig( ruta_excel + '\Figura' + str(m) + '.png', bbox_inches='tight')
                    plt.close(Figura2)
        plt.close('all') 
        k=k+1
