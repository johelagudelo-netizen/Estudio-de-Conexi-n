def Funcion(Lista_Frames_Fase,Lista_Frames_Tierra,Lista_Frames_Tensiones,\
                            Proteccion_Cabecera,Nombre_Directorio_Protecciones,\
                                Diccionario_Curvas_PGF,Curva_Proyecto):   
    import pandas as pd
    import math as math
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import numpy as np
    from sympy import sqrt
    import openpyxl
    from openpyxl import Workbook
    from openpyxl.styles import Font, NamedStyle, Border, Side, Alignment, Protection, PatternFill
    from openpyxl.drawing.image import Image
    from openpyxl.utils.dataframe import dataframe_to_rows
    from openpyxl.worksheet.table import Table, TableStyleInfo
    from openpyxl.utils import get_column_letter

    import sys
    import config_powerfactory  # ruta de PowerFactory: ver config_powerfactory.py
    import powerfactory as pf
    app = pf.GetApplication()

    Nodo_Mt_OR=app.GetCalcRelevantObjects(Curva_Proyecto.Barra_MT_OR + '.ElmTerm')[0]
    tension_kV=Nodo_Mt_OR.uknom


    RTC=Proteccion_Cabecera.RTC
    Curva51F=Proteccion_Cabecera.Curva51F
    Curva51N=Proteccion_Cabecera.Curva51N
    Dial51F=Proteccion_Cabecera.Dial51F
    Dial51N=Proteccion_Cabecera.Dial51N
    Pick_up51F=Proteccion_Cabecera.Pick_up51F
    Pick_up51N=Proteccion_Cabecera.Pick_up51N
    Pick_up50F=Proteccion_Cabecera.Pick_up50F
    Pick_up50N=Proteccion_Cabecera.Pick_up50N
    Delay_Instantanea_Fase=Proteccion_Cabecera.Delay_Instantanea_Fase
    Delay_Instantanea_Tierra=Proteccion_Cabecera.Delay_Instantanea_Tierra

    # Dial51F_PGF='0.09'
    # Dial51N_PGF='0.15'
    # Pick_up51F_PGF='192'
    # Pick_up51N_PGF='87'


    
    Dial51F_PGF=Diccionario_Curvas_PGF['Dial51F_PGF']
    Dial51N_PGF=Diccionario_Curvas_PGF['Dial51N_PGF']
    Pick_up51F_PGF=Diccionario_Curvas_PGF['Pick_up51F_PGF']
    Pick_up51N_PGF=Diccionario_Curvas_PGF['Pick_up51N_PGF']



    Diccionario_Fase_OR={'RTC':[RTC],'CURVA':[Curva51F],'PICKUP 51F':[Pick_up51F],\
                                'DIAL 51F':[Dial51F],'PICKUP 50 F':[Pick_up50F],\
                                'DELAY 50F':[Delay_Instantanea_Fase] }

    Frame_Fase_OR=pd.DataFrame(Diccionario_Fase_OR)  
        
    Diccionario_Tierra_OR={'RTC':[RTC],'CURVA':[Curva51N],'PICKUP 51N':[Pick_up51N],\
                                'DIAL 51N':[Dial51N],'PICKUP 50N':[Pick_up50N],\
                                'DELAY 50N':[Delay_Instantanea_Tierra] }

    Frame_Tierra_OR=pd.DataFrame(Diccionario_Tierra_OR)  
        
    Diccionario_Fase_PGF={'CURVA':[Curva51F],'PICKUP 51 F':[Pick_up51F_PGF],\
                                'DIAL 51F':[Dial51F_PGF]}

    Frame_Fase_PGF=pd.DataFrame(Diccionario_Fase_PGF)  
        
    Diccionario_Tierra_PGF={'CURVA':[Curva51N],'PICKUP 51 N':[Pick_up51N_PGF],\
                                'DIAL 51N':[Dial51N_PGF]}
        
    Frame_Tierra_PGF=pd.DataFrame(Diccionario_Tierra_PGF)  


    Libro = Workbook()

    # Seleccionar la hoja activa (por defecto es la primera)
    Hoja = Libro.active
    Hoja.title= 'Ansi_50_50N_51_51N' 

    for i in range(2, 40):  # Recorre las columnas de la 1 a la 4
        j = openpyxl.utils.get_column_letter(i)
        Hoja.column_dimensions[j].width = 20


    Estilo_titulo=NamedStyle(name="Estilo_titulo")
    Estilo_titulo.font=Font(color='FFFFFF')
    Estilo_titulo.fill=PatternFill("solid",fgColor='333F4F')
    Estilo_titulo.alignment= Alignment(horizontal='center', vertical='center',wrap_text=True)
    Estilo_titulo.border=Border(left=Side(border_style="thin", color="000000"),
                        right=Side(border_style="thin", color="000000"),
                        top=Side(border_style="thin", color="000000"),
                        bottom=Side(border_style="thin", color="000000"))

    Estilo_texto=NamedStyle(name="Estilo_texto")
    Estilo_texto.alignment= Alignment(horizontal='center', vertical='center',wrap_text=True)
    Estilo_texto.border=Border(left=Side(border_style="thin", color="000000"),
                        right=Side(border_style="thin", color="000000"),
                        top=Side(border_style="thin", color="000000"),
                        bottom=Side(border_style="thin", color="000000"))



    Lista_Titulos1=['Corriente Sensada Relé Fase - Falla Trifásica',\
                    'Corriente Sensada Relé Fase - Falla Bifásica',\
                        'Corriente Sensada Relé Fase - Falla Monofásica']


    def Ubicar_Frame(fila,Columna,df,Estilo_texto,Hoja):
        for r in dataframe_to_rows(df, index=False, header=True):
            Estilo=Estilo_texto
            for j, c in enumerate(r, start=Columna):  # La columna 2 es la columna C
                cell=Hoja.cell(row=fila, column=j, value=c)
                cell.alignment = Alignment(wrap_text=True)
                cell.style=Estilo
            fila += 1  # Incrementar la variable i para la siguiente fila

    Ubicar_Frame(3,2,Frame_Fase_OR,Estilo_texto,Hoja)
    Ubicar_Frame(3,10,Frame_Tierra_OR,Estilo_texto,Hoja)
    Ubicar_Frame(8,2,Frame_Fase_PGF,Estilo_texto,Hoja)
    Ubicar_Frame(8,10,Frame_Tierra_PGF,Estilo_texto,Hoja)

    Hoja.merge_cells(start_row=1, start_column=2, end_row=2, end_column=7)
    celda_titulo=Hoja.cell(row=1, column=2,value='AJUSTE DE FASE PROTECCIÓN DE SOBRECORRIENTE OR')
    celda_titulo.style=Estilo_titulo    

    Hoja.merge_cells(start_row=1, start_column=10, end_row=2, end_column=15)
    celda_titulo=Hoja.cell(row=1, column=10,value='AJUSTE DE TIERRA PROTECCIÓN DE SOBRECORRIENTE OR')
    celda_titulo.style=Estilo_titulo    

    Hoja.merge_cells(start_row=6, start_column=2, end_row=7, end_column=4)
    celda_titulo=Hoja.cell(row=6, column=2,value='AJUSTE DE FASE PROTECCIÓN DE SOBRECORRIENTE PGF')
    celda_titulo.style=Estilo_titulo  

    Hoja.merge_cells(start_row=6, start_column=10, end_row=7, end_column=12)
    celda_titulo=Hoja.cell(row=6, column=10,value='AJUSTE DE TIERRA PROTECCIÓN DE SOBRECORRIENTE PGF')
    celda_titulo.style=Estilo_titulo    


    i = 12
    m=0


    for df in Lista_Frames_Fase:
        Hoja.merge_cells(start_row=i-1, start_column=2, end_row=i-1, end_column=df.shape[1]+1)
        celda_titulo=Hoja.cell(row=i-1, column=2, value=Lista_Titulos1[m])
        celda_titulo.style=Estilo_titulo
        k=0
        for r in dataframe_to_rows(df, index=False, header=True):
            if k==0:
                Estilo=Estilo_titulo
            else:
                Estilo=Estilo_texto
            for j, c in enumerate(r, start=2):  # La columna 2 es la columna C
                cell=Hoja.cell(row=i, column=j, value=c)
                cell.alignment = Alignment(wrap_text=True)
                cell.style=Estilo
            i += 1  # Incrementar la variable i para la siguiente fila
            k += 1 
        i += 2  # Incrementar la variable i en 2 para agregar dos filas vacías
        m +=1

    i=12
    m=0
    Lista_Titulos2=['Corriente Sensada Relé Tierra - Falla Trifásica',\
                    'Corriente Sensada Relé Tierra - Falla Bifásica',\
                        'Corriente Sensada Relé Tierra - Falla Monofásica']
    for df in Lista_Frames_Tierra:
        Hoja.merge_cells(start_row=i-1, start_column=10, end_row=i-1, end_column=df.shape[1]+9)
        celda_titulo=Hoja.cell(row=i-1, column=10, value=Lista_Titulos2[m])
        celda_titulo.style=Estilo_titulo
        k=0
        for r in dataframe_to_rows(df, index=False, header=True):
            if k==0:
                Estilo=Estilo_titulo
            else:
                Estilo=Estilo_texto
            for j, c in enumerate(r, start=10):  # La columna 2 es la columna C
                cell=Hoja.cell(row=i, column=j, value=c)
                cell.alignment = Alignment(wrap_text=True)
                cell.style=Estilo
            i += 1  # Incrementar la variable i para la siguiente fila
            k += 1 
        i += 2  # Incrementar la variable i en 2 para agregar dos filas vacías
        m +=1


    Hoja_Tensiones=Libro.create_sheet()

    Hoja_Tensiones.title= 'Ansi27_59_59N'     
    Libro.active=Hoja_Tensiones


    xtiempo=[1,0.5,0.8,2.5,2.3,2.2]

    xHVRT=[0,0,0,2,2,21]
    yHVRT=[1.1,1.2,1.2,1.2,1.1,1.1]

    #### Curva LVRT

    xLVRT=[0,0,0,0.5,2,4,20,20,21]
    yLVRT=[0.9,0.1,0.1,0.1,0.1,0.85,0.85,0.9,0.9]

    ### Ajuste 59

    x59=[0.5,0.5,2.5,2.5,21]
    y59=[1.3,1.25,1.25,1.15,1.15]

    ######## Ajuste ANSI 27

    x27=[5,5,10,10,21]
    y27=[0,0.6,0.6,0.8,0.8]


    def determinar_ANSI_27(Tension_Minima):
        if Tension_Minima <= 0.6:
            return '5'
        elif Tension_Minima> 0.6 and Tension_Minima<0.8: 
            return '10'
        else:
            return 'No Opera'
    
    def determinar_ANSI_59(Tension_Maxima):
        if Tension_Maxima > 1.25:
            return '0.5'
        elif Tension_Maxima >= 1.15 and Tension_Maxima<=1.25: 
            return '2.5'
        else:
            return 'No Opera'
    
    def determinar_ANSI_59N(Tension_Residual):
        if Tension_Residual > 0.3:
            return '0.15'
        else:
            return 'No Opera'
            

    for df in Lista_Frames_Tensiones:
        Nombre_Columnas=['Tensión sensada Rele Parque Solar (pu) - Fase A',\
                         'Tensión sensada Rele Parque Solar (pu) - Fase B',\
                         'Tensión sensada Rele Parque Solar (pu) - Fase C']
        df['Tensión Máxima'] = df[Nombre_Columnas].max(axis=1)
        df['Tensión Mínima'] = df[Nombre_Columnas].min(axis=1)
        df['Actuación Relé ANSI 27 (s)'] =df['Tensión Mínima'].apply(determinar_ANSI_27)
        df['Actuación Relé ANSI 59 (s)'] =df['Tensión Máxima'].apply(determinar_ANSI_59)
        df['Actuación Relé ANSI 59N (s)'] =df['Tensión sensada Rele Parque Solar (pu) - Residual']\
                                            .apply(determinar_ANSI_59N)



    for i in range(2, 40):  # Recorre las columnas de la 1 a la 4
        j = openpyxl.utils.get_column_letter(i)
        Hoja_Tensiones.column_dimensions[j].width = 20

    i = 12
    m=0

    Lista_Titulos_3=['Falla Trifásica','Falla Bifásica','Falla Monofásica']
    for df in Lista_Frames_Tensiones:
        k=0
        Hoja_Tensiones.merge_cells(start_row=i-1, start_column=2, end_row=i-1, end_column=df.shape[1]+1)
        celda_titulo=Hoja_Tensiones.cell(row=i-1, column=2, value=Lista_Titulos_3[m])
        celda_titulo.style=Estilo_titulo
        for r in dataframe_to_rows(df, index=False, header=True):
            if k==0:
                Estilo=Estilo_titulo
            else:
                Estilo=Estilo_texto
            for j, c in enumerate(r, start=2):  
                cell=Hoja_Tensiones.cell(row=i, column=j, value=c)
                cell.alignment = Alignment(wrap_text=True)
                cell.style=Estilo
            i += 1  # Incrementar la variable i para la siguiente fila
            k += 1 
        i += 2  # Incrementar la variable i en 2 para agregar dos filas vacías
        m +=1

        Diccionario_Ajustes_Tensiones={'Protección ANSI':['27','27','59','59','59N'],\
                     'Etapa':['1','2','1','2','-'],\
                        'Ajuste Tensión (pu)':[0.8,0.6,1.15,1.25,0.3],\
                        'Tiempo Actuación (s)':[10,5,2.5,0.5,0.15]}
        
        df_Ajustes_Tensiones=pd.DataFrame(Diccionario_Ajustes_Tensiones)
        df_Ajustes_Tensiones['Ajuste Tensión (kV)']=\
            df_Ajustes_Tensiones['Ajuste Tensión (pu)']*tension_kV/(3**0.5)
        
        df_Ajustes_Tensiones = df_Ajustes_Tensiones[['Protección ANSI',\
                                'Etapa','Ajuste Tensión (pu)','Ajuste Tensión (kV)',\
                                    'Tiempo Actuación (s)']]
        
        Ubicar_Frame(2,2,df_Ajustes_Tensiones,Estilo_texto,Hoja_Tensiones)

        Hoja_Tensiones.merge_cells(start_row=1, start_column=2, end_row=1, end_column=6)
        celda_titulo=Hoja_Tensiones.cell(row=1, column=2,value='AJUSTES: ANSI 27 - ANSI 59 - ANSI 59N')
        celda_titulo.style=Estilo_titulo    


    plt.figure(figsize=(14,10))
    plt.xlim(0,21)
    plt.ylim(0,1.3)

    plt.grid(which='both')
    plt.title(' Curvas HVRT y LVRT para la planta fotovoltaica')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Valor tensión línea-línea en punto de conexión (p.u)')


    plt.plot(xHVRT,yHVRT,'-o',color='b', label='Curva HVRT')
    for i in range(len(xHVRT)):
            plt.text(xHVRT[i],yHVRT[i]+0.01,f'({yHVRT[i]})')

    plt.plot(xLVRT,yLVRT,'-o',color='g', label='Curva LVRT')
    for i in range(len(xLVRT)):
            plt.text(xLVRT[i],yLVRT[i]+0.01,f'({yLVRT[i]})')

    plt.plot(x59,y59,'-o',color='r', label='Ajuste 59')
    for i in range(len(x59)):
            plt.text(x59[i],y59[i]+0.01,f'({y59[i]})')

    plt.plot(x27,y27,'-o',color='y', label='Ajuste 27')
    for i in range(len(x27)):
            plt.text(x27[i],y27[i]+0.01,f'({y27[i]})')
    plt.legend()
    plt.savefig(Nombre_Directorio_Protecciones + '/' +'Curvas HVRT_LVRT.png')
    

    Hoja_Frecuencia=Libro.create_sheet()

    Hoja_Frecuencia.title= 'Ansi81U_81O'     
    Libro.active=Hoja_Frecuencia


    for i in range(2, 40):  # Recorre las columnas de la 1 a la 4
        j = openpyxl.utils.get_column_letter(i)
        Hoja_Frecuencia.column_dimensions[j].width = 20

    Diccionario_Ajustes_Frecuencia={'Protección ANSI':['87U','87O'],\
                     'Ajuste':['57','62'],\
                        'Tiempo Actuación (s)':[0.2,0.2]}
        
    df_Ajustes_Frecuencia=pd.DataFrame(Diccionario_Ajustes_Frecuencia)     
    Ubicar_Frame(2,2,df_Ajustes_Frecuencia,Estilo_texto,Hoja_Frecuencia)

    nombre_archivo = "Cordinacion.xlsx"
    Libro.save(Nombre_Directorio_Protecciones + '/' + nombre_archivo)



