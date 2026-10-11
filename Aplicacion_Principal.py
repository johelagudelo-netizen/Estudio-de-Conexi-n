import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
from tkinter import filedialog
import sys
import pandas as pd
try:
    import config_powerfactory  # ruta de PowerFactory: ver config_powerfactory.py
    import powerfactory as pf
    app = pf.GetApplication()
except Exception as error:
    _raiz = tk.Tk()
    _raiz.withdraw()
    messagebox.showerror('PowerFactory no disponible', str(error))
    sys.exit(1)

class Cabecera:
     def __init__(self):
         self.RTC=0
         self.Curva51F=''
         self.Curva51N=''
         self.Pick_up51F=''
         self.Pick_up51N=''
         self.Dial51F=''
         self.Dial51N=''
         self.Pick_up50F=''
         self.Pick_up50N=''
         self.Delay_Instantanea_Fase=''
         self.Delay_Instantanea_Tierra=''
         self.Nodo=''
         self.V51F=''
         self.V51N=''
         self.V50F=''
         self.V50N=''


     def Actualizar_Cabecera(self,RTC,Curva51F,Curva51N,Pick_up51F,\
        Pick_up51N,Dial51F,Dial51N,Pick_up50F,Pick_up50N,Delay_Instantaneo_T,\
            Delay_Instantaneo_F,Nodo,Sensado,Existe_51F,Existe_51N,\
                Existe_50F,Existe_50N):
        self.RTC=RTC
        self.Curva51F=Curva51F
        self.Curva51N=Curva51N
        self.Pick_up51F=Pick_up51F
        self.Pick_up51N=Pick_up51N
        self.Dial51F=Dial51F
        self.Dial51N=Dial51N
        self.Pick_up50F=Pick_up50F
        self.Pick_up50N=Pick_up50N
        self.Delay_Instantanea_Fase=Delay_Instantaneo_F
        self.Delay_Instantanea_Tierra=Delay_Instantaneo_T
        self.Nodo=Nodo
        self.Elm_Sensado=Sensado
        self.V51F=Existe_51F
        self.V51N=Existe_51N
        self.V50F=Existe_50F
        self.V50N=Existe_50N


Proteccion_Cabecera=Cabecera()


class Curva_PGF:
     def __init__(self):
         self.Barra_MT_OR=''
         self.Barra_BT_PGF=''
         self.Barra_MT_PGF=''
         self.RFalla_1=''
         self.RFalla_2=''
         self.RFalla_3=''
         self.Variacion=''
         self.Sensado=''


     def Actualizar_Curva_PGF(self,Barra_MT_OR,Barra_BT_PGF,Barra_MT_PGF,\
                                RFalla1,RFalla2,RFalla3,Variacion,Sensado):
            self.Barra_MT_OR=Barra_MT_OR
            self.Barra_BT_PGF=Barra_BT_PGF
            self.Barra_MT_PGF=Barra_MT_PGF
            self.RFalla_1=RFalla1
            self.RFalla_2=RFalla2
            self.RFalla_3=RFalla3
            self.Variacion=Variacion
            self.Sensado=Sensado

Curva_Proyecto=Curva_PGF()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicativo de EDC")

        width = 600
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, \
                                    (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLabel_1 = tk.Label(root, text="APLICATIVO DE EDC - ESTUDIOS DE CONEXIÓN SIMPLIFICADOS", \
                             bg="#d68017", fg="#333333", justify="center")
        GLabel_1.place(x=100, y=10, width=400, height=50)

        self.Archivo_Entrada = tk.StringVar()
        # Crear el campo de texto con la variable de texto asociada
        self.Archivo_Entrada_Entry = tk.Entry(root, textvariable=self.Archivo_Entrada, state="readonly")
        self.Archivo_Entrada_Entry.place(x=100, y=100, width=200, height=25)

        GButton_1 = tk.Button(root, text="Agregar Archivo", \
                    bg="#d9841d", fg="#000000", command=self.GButton_1_command)
        GButton_1.place(x=325, y=100, width=175, height=30)
        
        GButton_2 = tk.Button(root, text="Power Factory Desatendido", \
                    bg="#d9841d", fg="#000000", command=self.GButton_2_command)
        GButton_2.place(x=100, y=150, width=175, height=30)

        self.GCheckBox_1 = tk.Checkbutton(root, text=" ", 
                                    font=tkFont.Font(family='Times', size=10),
                                    fg="#333333", justify="center",
                                    offvalue="10", onvalue="11")
        self.GCheckBox_1.place(x=100, y=200, width=150, height=25)  

        GButton_3 = tk.Button(root, text="Construir Red", bg="#d9841d", \
                              fg="#000000", command=self.GButton_3_command)
        GButton_3.place(x=100, y=250, width=175, height=30)

        self.GCheckBox_2 = tk.Checkbutton(root, text=" ", 
                                    font=tkFont.Font(family='Times', size=10),
                                    fg="#333333", justify="center",
                                    offvalue="20", onvalue="21")
        self.GCheckBox_2.place(x=100, y=300, width=150, height=25) 

        GButton_4 = tk.Button(root, text="Generar Grafico", bg="#d9841d", \
                              fg="#000000", command=self.GButton_4_command)
        GButton_4.place(x=100, y=350, width=175, height=30)

        self.GCheckBox_3 = tk.Checkbutton(root, text=" ", 
                                    font=tkFont.Font(family='Times', size=10),
                                    fg="#333333", justify="center",
                                    offvalue="30", onvalue="31")
        self.GCheckBox_3.place(x=100, y=400, width=150, height=25)

        GButton_5 = tk.Button(root, text="Flujo Carga", bg="#d9841d",\
                              fg="#000000", command=self.GButton_5_command)
        GButton_5.place(x=325, y=150, width=175, height=30)

        self.GCheckBox_4 = tk.Checkbutton(root, text=" ", 
                                    font=tkFont.Font(family='Times', size=10),
                                    fg="#333333", justify="center",
                                    offvalue="40", onvalue="41")
        self.GCheckBox_4.place(x=350, y=200, width=150, height=25)


        GButton_6 = tk.Button(root, text="CortoCircuito", bg="#d9841d", \
                              fg="#000000", command=self.GButton_6_command)
        GButton_6.place(x=325, y=250, width=175, height=30)
        
        self.GCheckBox_5 = tk.Checkbutton(root, text=" ", 
                                    font=tkFont.Font(family='Times', size=10),
                                    fg="#333333", justify="center",
                                    offvalue="50", onvalue="51")
        self.GCheckBox_5.place(x=350, y=300, width=150, height=25)

        
        GButton_Mod_Prot = tk.Button(root, text="Cordinación Protecciones", bg="#d9841d", \
                              fg="#000000", command=self.GButton_Mod_Prot_command)
        GButton_Mod_Prot.place(x=325, y=350, width=175, height=30)
        
        self.GCheckBox_Prot = tk.Checkbutton(root, text=" ", 
                                    font=tkFont.Font(family='Times', size=10),
                                    fg="#333333", justify="center",
                                    offvalue="50", onvalue="51")
        self.GCheckBox_Prot.place(x=350, y=400, width=150, height=25)
        


    def GButton_Mod_Prot_command(self):
        print("Hola Mundo")
        self.open_Cordinacion_window()
        
        

    def GButton_1_command(self):
        print("Seleccionar Archivo")
        fichero=filedialog.askopenfile(title="Abrir Proyecto")
        if fichero: 
            self.Archivo_Entrada.set(fichero.name)
            self.Nombre_Fichero=fichero.name

    def GButton_2_command(self):
        try:
            app.Show()
            messagebox.showinfo('Modo Interactivo', 'Ejecución Exitosa de Modo Desatendido')
            self.GCheckBox_1.invoke()

        except:
            messagebox.showinfo('Modo Interactivo', 'Ejecución Fallida de Modo Desatendido')

    def GButton_3_command(self):
        Valor=app.GetActiveProject()
        print(Valor)
        if Valor !=None:
            messagebox.showinfo('Proyecto Activo', ' Puede empezar a crear la red en el proyecto Activo')
            import Tipo_Lineas
            Tipo_Lineas.Funcion(self.Nombre_Fichero)
            import Tipo_Transformadores
            Tipo_Transformadores.Funcion(self.Nombre_Fichero)
            import Caracteristicas_Tiempo
            Caracteristicas_Tiempo.Funcion(self.Nombre_Fichero)
            import Nodos
            Nodos.Funcion(self.Nombre_Fichero)
            import Lineas
            Lineas.Funcion(self.Nombre_Fichero)
            import Transformadores
            Transformadores.Funcion(self.Nombre_Fichero)
            import Cargas
            Cargas.Funcion(self.Nombre_Fichero)
            self.GCheckBox_2.invoke()
            
        else:
            messagebox.showinfo('Proyecto Activo', ' Active un proyecto para crear la Red')

    def GButton_4_command(self):
        import Feeder
        Feeder.Funcion(self.Nombre_Fichero)
        self.GCheckBox_3.invoke()

    def GButton_5_command(self):
        print("command")
        Caso_Estudio=app.GetActiveStudyCase()
        try:
            Contingencias=app.GetFromStudyCase('Contingencias.SetSelect')
        except:
            Contingencias=Caso_Estudio.CreateObject('SetSelect','Contingencias')
        try:
            Nodos=app.GetFromStudyCase('Nodos.SetSelect')
        except:
            Nodos=Caso_Estudio.CreateObject('SetSelect','Nodos')
        try:
            Cargabilidades=app.GetFromStudyCase('Cargabilidades.SetSelect')
        except:
            Cargabilidades=Caso_Estudio.CreateObject('SetSelect','Cargabilidades')
        self.open_second_window()
        self.GCheckBox_4.invoke()

    def GButton_6_command(self):
        Caso_Estudio=app.GetActiveStudyCase()
        try:
            Nodos_Corto=app.GetFromStudyCase('Nodos_Corto.SetSelect')
        except:
            Nodos_Corto=Caso_Estudio.CreateObject('SetSelect','Nodos_Corto')
        self.open_Tercer_window()
        self.GCheckBox_5.invoke()
        
   
        
   
    def open_Tercer_window(self):
        root3 = tk.Toplevel(self.root)
        root3.title("Aplicativo de EDC 2")
        width = 1000
        height = 600
        screenwidth = root3.winfo_screenwidth()
        screenheight = root3.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, \
                                    (screenheight - height) / 2)
        root3.geometry(alignstr)
        root3.resizable(width=False, height=False)
        GLabel_5 = tk.Label(root3, text="APLICATIVO DE EDC - ESTUDIOS DE CONEXIÓN SIMPLIFICADOS", \
                             bg="#d68017", fg="#333333", justify="center")
        GLabel_5.place(x=100, y=10, width=800, height=50)

        GLabel_2 = tk.Label(root3, text="Año", \
                              justify="center")
        GLabel_2.place(x=100, y=75, width=50, height=20)

        Opciones_Corto_Año= ["2024","2025", "2026", "2027", "2028","2029", \
                 "2030", "2031", "2032","2033", "2034"]     

        # Crear un frame contenedor
        frame_contenedor_corto1 = tk.Frame(root3)
        frame_contenedor_corto1.place(x=100, y=100, width=75, height=70)

        # Crear la lista desplegable con scroll
        scrollbar_corto1 = tk.Scrollbar(frame_contenedor_corto1, orient=tk.VERTICAL)
        lista_desplegable_corto1 = tk.Listbox(frame_contenedor_corto1, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar_corto1.set)
        scrollbar_corto1.config(command=lista_desplegable_corto1.yview)
        scrollbar_corto1.pack(side=tk.RIGHT, fill=tk.Y)
        for opcion in Opciones_Corto_Año:
            lista_desplegable_corto1.insert(tk.END, opcion)
        lista_desplegable_corto1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Botón para mostrar la selección
        GButton_corto1 = tk.Button(root3, text="Aceptar",  \
                      bg="#d9841d",fg="#000000", \
                command=lambda: self.GButton_Corto1_command(lista_desplegable_corto1.curselection(), Opciones_Corto_Año))
        GButton_corto1.place(x=100, y=185, width=75, height=20)
        
        self.texto_seleccion_corto1 = tk.Text(root3, wrap=tk.WORD, width=10, height=2)
        self.texto_seleccion_corto1.place(x=100, y=280)

        # Etiquetas para los títulos de los textos
        titulo_texto_seleccion_corto1 = tk.Label(root3, text="Año:", font=("Arial", 10, "bold"))
        titulo_texto_seleccion_corto1.place(x=100, y=250)
        
        
        GLabel_corto2 = tk.Label(root3, text="Variaciones", \
                              justify="center")
        GLabel_corto2.place(x=200, y=75, width=75, height=20)

        # Crear Frame contenedor para lista de Variaciones
        self.frame_contenedor_corto2 = tk.Frame(root3,bg="white")
        self.frame_contenedor_corto2.place(x=200, y=100, width=150, height=50)

        self.scrollbar_corto2 = tk.Scrollbar(self.frame_contenedor_corto2, orient=tk.VERTICAL)
        
        # Crear la lista desplegable con scroll para Variaciones
        self.lista_desplegable_corto2 = tk.Listbox(self.frame_contenedor_corto2, \
                                selectmode=tk.MULTIPLE, yscrollcommand=self.scrollbar_corto2.set)
        self.scrollbar_corto2.config(command=self.lista_desplegable_corto2.yview)
        self.scrollbar_corto2.pack(side=tk.RIGHT, fill=tk.Y)

        self.opciones_Variaciones_2=[]
        GButton_corto2 = tk.Button(root3, text="Actualizar Variaciones",  \
                      bg="#d9841d",fg="#000000", command=lambda: self.GButton_corto2_command())
        GButton_corto2.place(x=375, y=100, width=175, height=30)

        # Botón para mostrar la selección
        GButton_corto3 = tk.Button(root3, text="Seleccionar Variaciones",  \
                      bg="#d9841d",fg="#000000", \
                        command=lambda: self.GButton_corto3_command(self.lista_desplegable_corto2.curselection(),self.opciones_Variaciones_2))
        GButton_corto3.place(x=375, y=175, width=175, height=30)

        self.texto_seleccion_corto2 = tk.Text(root3, wrap=tk.WORD, width=17, height=2)
        self.texto_seleccion_corto2.place(x=200, y=175)
        
        titulo_texto_seleccion_corto2 = tk.Label(root3, text="Variaciones:", font=("Arial", 10, "bold"))
        titulo_texto_seleccion_corto2.place(x=200, y=150)
        

        GButton_corto4 = tk.Button(root3, text="Ejecutar CortoCircuito",  \
                      bg="#d9841d",fg="#000000", \
                        command=lambda: self.GButton_corto4_command())
        GButton_corto4.place(x=375, y=250, width=175, height=30)  
        
        self.Direccion_Entrada_corto = tk.StringVar()
        # Crear el campo de texto con la variable de texto asociada
        self.Direccion1_Entry_corto = tk.Entry(root3, textvariable=self.Direccion_Entrada_corto, state="readonly")
        self.Direccion1_Entry_corto.place(x=100, y=340, width=200, height=25)

        GButton_10_corto = tk.Button(root3, text="Agregar Carpeta PDFs", \
                    bg="#d9841d", fg="#000000", command=self.GButton_10_corto_command)
        GButton_10_corto.place(x=325, y=340, width=175, height=30)


        self.Direccion_Entrada_corto2 = tk.StringVar()
        # Crear el campo de texto con la variable de texto asociada
        self.Direccion2_Entry_corto = tk.Entry(root3, textvariable=self.Direccion_Entrada_corto2, state="readonly")
        self.Direccion2_Entry_corto.place(x=100, y=390, width=200, height=25)

        GButton_11_corto = tk.Button(root3, text="Agregar Carpeta Excel", \
                    bg="#d9841d", fg="#000000", command=self.GButton_11_corto_command)
        GButton_11_corto.place(x=325, y=390, width=175, height=30)

        GLabel_6_corto = tk.Label(root3, text="Diagramas", \
                              justify="center")
        GLabel_6_corto.place(x=100, y=425, width=75, height=20)

        # Crear Frame contenedor para lista de Diagramas
        self.frame_contenedor_corto4 = tk.Frame(root3,bg="white")
        self.frame_contenedor_corto4.place(x=100, y=450, width=200, height=50)

        self.scrollbar_corto4 = tk.Scrollbar(self.frame_contenedor_corto4, orient=tk.VERTICAL)
        
        # Crear la lista desplegable con scroll para Diagramas
        self.lista_desplegable_corto4 = tk.Listbox(self.frame_contenedor_corto4, selectmode=tk.MULTIPLE, yscrollcommand=self.scrollbar_corto4.set)
        self.scrollbar_corto4.config(command=self.lista_desplegable_corto4.yview)
        self.scrollbar_corto4.pack(side=tk.RIGHT, fill=tk.Y)

        self.opciones_Diagramas_corto=[]
        GButton_12_corto = tk.Button(root3, text="Actualizar Diagramas",  \
                      bg="#d9841d",fg="#000000", command=lambda: self.GButton_12_corto_command())
        GButton_12_corto.place(x=325, y=475, width=175, height=30)

        # Botón para mostrar la selección
        GButton_13_corto = tk.Button(root3, text="Seleccionar Diagramas",  \
                      bg="#d9841d",fg="#000000", command=lambda: self.GButton_13_corto_command(self.lista_desplegable_corto4.curselection(),self.opciones_Diagramas_corto))
        GButton_13_corto.place(x=325, y=550, width=175, height=30)

        self.texto_seleccion_corto4 = tk.Text(root3, wrap=tk.WORD, width=23, height=2)
        self.texto_seleccion_corto4.place(x=100, y=540)
        
        titulo_texto_seleccion_corto4 = tk.Label(root3, text="Diagramas Impresión:", font=("Arial", 10, "bold"))
        titulo_texto_seleccion_corto4.place(x=100, y=510)

        
    def GButton_Corto1_command(self, seleccion, opciones):
        print(opciones)
        print('Boton 7 presionado')
        print(seleccion)
        seleccion_texto = [opciones[index] for index in seleccion]
        self.Texto_Años=seleccion_texto.copy()
        self.texto_seleccion_corto1.delete(1.0, tk.END)
        self.texto_seleccion_corto1.insert(tk.END, ", ".join(seleccion_texto))    

        
    def GButton_corto2_command(self):
        print("Buscar Variaciones")
        Folder_Variaciones=app.GetProjectFolder('scheme')
        self.opciones_Variaciones_2.clear()
        app.PrintPlain(Folder_Variaciones)
        Variaciones=Folder_Variaciones.GetContents()
        self.lista_desplegable_corto2.delete(0, tk.END)
        for i in Variaciones:
            self.opciones_Variaciones_2.append(i.GetAttribute('loc_name'))
        
        for opcion in self.opciones_Variaciones_2:
            self.lista_desplegable_corto2.insert(tk.END, opcion)
        self.lista_desplegable_corto2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def GButton_corto3_command(self, seleccion, opciones):
        print(opciones)
        print(seleccion)
        print('Boton 13 presionado')
        print(seleccion)
        seleccion_texto = [opciones[index] for index in seleccion]
        self.Texto_Variaciones_2=seleccion_texto.copy()
        self.texto_seleccion_corto2.delete(1.0, tk.END)
        self.texto_seleccion_corto2.insert(tk.END, ", ".join(seleccion_texto)) 
        
        
    def GButton_10_corto_command(self):
        print("Seleccionar Archivo")
        Directorio=filedialog.askdirectory(title="Abrir ruta")
        if Directorio: 
            self.Direccion_Entrada_corto.set(Directorio)
            self.Nombre_Directorio_corto=Directorio
        
    
    def GButton_11_corto_command(self):
        print("Seleccionar Archivo")
        Directorio=filedialog.askdirectory(title="Abrir ruta")
        if Directorio: 
            self.Direccion_Entrada_corto2.set(Directorio)
            self.Nombre_Directorio_corto2=Directorio

    def GButton_12_corto_command(self):
        print("Buscar Diagramas")
        Folder_Diagramas=app.GetProjectFolder('dia')
        self.opciones_Diagramas_corto.clear()
        app.PrintPlain(Folder_Diagramas)
        Diagramas=Folder_Diagramas.GetContents()
        self.lista_desplegable_corto4.delete(0, tk.END)
        for i in Diagramas:
            self.opciones_Diagramas_corto.append(i.GetAttribute('loc_name'))
        
        for opcion in self.opciones_Diagramas_corto:
            self.lista_desplegable_corto4.insert(tk.END, opcion)
        self.lista_desplegable_corto4.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
    def GButton_13_corto_command(self, seleccion, opciones):
        print(opciones)
        print(seleccion)
        print('Boton 13 presionado')
        print(seleccion)
        seleccion_texto = [opciones[index] for index in seleccion]
        self.Diagramas_Texto_Corto=seleccion_texto.copy()
        self.texto_seleccion_corto4.delete(1.0, tk.END)
        self.texto_seleccion_corto4.insert(tk.END, ", ".join(seleccion_texto)) 
        
    def GButton_corto4_command(self):
        import Corto
        Corto.Funcion(self.Texto_Años, self.Texto_Variaciones_2,self.Diagramas_Texto_Corto ,  self.Nombre_Directorio_corto, self.Nombre_Directorio_corto2)

    def open_second_window(self):
        Archivo=self.Nombre_Fichero
        root2 = tk.Toplevel(self.root)
        root2.title("Aplicativo de EDC 2")
        width = 1000
        height = 600
        screenwidth = root2.winfo_screenwidth()
        screenheight = root2.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, \
                                    (screenheight - height) / 2)
        root2.geometry(alignstr)
        root2.resizable(width=False, height=False)
        GLabel_5 = tk.Label(root2, text="APLICATIVO DE EDC - ESTUDIOS DE CONEXIÓN SIMPLIFICADOS", \
                             bg="#d68017", fg="#333333", justify="center")
        GLabel_5.place(x=100, y=10, width=800, height=50)

        GLabel_2 = tk.Label(root2, text="Hora", \
                              justify="center")
        GLabel_2.place(x=100, y=75, width=50, height=20)

        # Lista de opciones
        opciones = ["00","01", "02", "03", "04","05", "06", "07", "08","09", "10", "11", "12", "13", "14","15", "16", "17", "18","19", "20", "21", "22","23"]

        # Crear un frame contenedor
        frame_contenedor = tk.Frame(root2)
        frame_contenedor.place(x=100, y=100, width=75, height=100)

        # Crear la lista desplegable con scroll
        scrollbar = tk.Scrollbar(frame_contenedor, orient=tk.VERTICAL)
        lista_desplegable = tk.Listbox(frame_contenedor, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar.set)
        scrollbar.config(command=lista_desplegable.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        for opcion in opciones:
            lista_desplegable.insert(tk.END, opcion)
        lista_desplegable.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Botón para mostrar la selección
        GButton_7 = tk.Button(root2, text="Aceptar",  \
                      bg="#d9841d",fg="#000000", command=lambda: self.GButton_7_command(lista_desplegable.curselection(), opciones))
        GButton_7.place(x=100, y=210, width=75, height=20)

        GLabel_3 = tk.Label(root2, text="Año", \
                              justify="center")
        GLabel_3.place(x=425, y=75, width=50, height=20)

        Escenarios=pd.read_excel(Archivo, sheet_name='Proyecciones_Demanda')
        opciones_Demanda=Escenarios.columns[1:].tolist()  
        # Crear un frame contenedor
        frame_contenedor_2 = tk.Frame(root2)
        frame_contenedor_2.place(x=260, y=100, width=75, height=100)

        # Crear la lista desplegable con scroll
        scrollbar_2 = tk.Scrollbar(frame_contenedor_2, orient=tk.VERTICAL)
        lista_desplegable_2 = tk.Listbox(frame_contenedor_2, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar_2.set)
        scrollbar_2.config(command=lista_desplegable_2.yview)
        scrollbar_2.pack(side=tk.RIGHT, fill=tk.Y)
        for opcion in opciones_Demanda:
            lista_desplegable_2.insert(tk.END, opcion)
        lista_desplegable_2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Botón para mostrar la selección
        GButton_8 = tk.Button(root2, text="Aceptar",  \
                      bg="#d9841d",fg="#000000", command=lambda: self.GButton_8_command(lista_desplegable_2.curselection(), opciones_Demanda))
        GButton_8.place(x=260, y=210, width=75, height=20)

        GLabel_4 = tk.Label(root2, text="Demanda", \
                              justify="center")
        GLabel_4.place(x=260, y=75, width=75, height=20)
        
        # Lista de opciones
        opciones_Año=Escenarios['AÑO']
        opciones_Año = opciones_Año.tolist()  
        # Crear un frame contenedor
        frame_contenedor_3 = tk.Frame(root2)
        frame_contenedor_3.place(x=425, y=100, width=75, height=100)

        # Crear la lista desplegable con scroll
        scrollbar_3 = tk.Scrollbar(frame_contenedor_3, orient=tk.VERTICAL)
        lista_desplegable_3 = tk.Listbox(frame_contenedor_3, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar_3.set)
        scrollbar_3.config(command=lista_desplegable_3.yview)
        scrollbar_3.pack(side=tk.RIGHT, fill=tk.Y)
        for opcion in opciones_Año:
            lista_desplegable_3.insert(tk.END, opcion)
        lista_desplegable_3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Botón para mostrar la selección
        GButton_9 = tk.Button(root2, text="Aceptar",  \
                      bg="#d9841d",fg="#000000", command=lambda: self.GButton_9_command(lista_desplegable_3.curselection(), opciones_Año))
        GButton_9.place(x=425, y=210, width=75, height=20)


        # Texto para mostrar las selecciones
        self.texto_seleccion_1 = tk.Text(root2, wrap=tk.WORD, width=10, height=2)
        self.texto_seleccion_1.place(x=100, y=280)

        self.texto_seleccion_2 = tk.Text(root2, wrap=tk.WORD, width=10, height=2)
        self.texto_seleccion_2.place(x=260, y=280)

        self.texto_seleccion_3 = tk.Text(root2, wrap=tk.WORD, width=10, height=2)
        self.texto_seleccion_3.place(x=420, y=280)

        # Etiquetas para los títulos de los textos
        titulo_texto_seleccion_1 = tk.Label(root2, text="Hora:", font=("Arial", 10, "bold"))
        titulo_texto_seleccion_1.place(x=100, y=250)

        titulo_texto_seleccion_2 = tk.Label(root2, text="Demanda:", font=("Arial", 10, "bold"))
        titulo_texto_seleccion_2.place(x=260, y=250)

        titulo_texto_seleccion_3 = tk.Label(root2, text="Año:", font=("Arial", 10, "bold"))
        titulo_texto_seleccion_3.place(x=420, y=250)

        self.Direccion_Entrada = tk.StringVar()
        # Crear el campo de texto con la variable de texto asociada
        self.Direccion1_Entry = tk.Entry(root2, textvariable=self.Direccion_Entrada, state="readonly")
        self.Direccion1_Entry.place(x=100, y=340, width=200, height=25)

        GButton_10 = tk.Button(root2, text="Agregar Carpeta PDFs", \
                    bg="#d9841d", fg="#000000", command=self.GButton_10_command)
        GButton_10.place(x=325, y=340, width=175, height=30)


        self.Direccion_Entrada_2 = tk.StringVar()
        # Crear el campo de texto con la variable de texto asociada
        self.Direccion2_Entry = tk.Entry(root2, textvariable=self.Direccion_Entrada_2, state="readonly")
        self.Direccion2_Entry.place(x=100, y=390, width=200, height=25)

        GButton_11 = tk.Button(root2, text="Agregar Carpeta Excel", \
                    bg="#d9841d", fg="#000000", command=self.GButton_11_command)
        GButton_11.place(x=325, y=390, width=175, height=30)

        GLabel_6 = tk.Label(root2, text="Diagramas", \
                              justify="center")
        GLabel_6.place(x=100, y=425, width=75, height=20)

        # Crear Frame contenedor para lista de Diagramas
        self.frame_contenedor_4 = tk.Frame(root2,bg="white")
        self.frame_contenedor_4.place(x=100, y=450, width=200, height=50)

        self.scrollbar_4 = tk.Scrollbar(self.frame_contenedor_4, orient=tk.VERTICAL)
        
        # Crear la lista desplegable con scroll para Diagramas
        self.lista_desplegable_4 = tk.Listbox(self.frame_contenedor_4, selectmode=tk.MULTIPLE, yscrollcommand=self.scrollbar_4.set)
        self.scrollbar_4.config(command=self.lista_desplegable_4.yview)
        self.scrollbar_4.pack(side=tk.RIGHT, fill=tk.Y)

        self.opciones_Diagramas=[]
        GButton_12 = tk.Button(root2, text="Actualizar Diagramas",  \
                      bg="#d9841d",fg="#000000", command=lambda: self.GButton_12_command())
        GButton_12.place(x=325, y=475, width=175, height=30)

        # Botón para mostrar la selección
        GButton_13 = tk.Button(root2, text="Seleccionar Diagramas",  \
                      bg="#d9841d",fg="#000000", command=lambda: self.GButton_13_command(self.lista_desplegable_4.curselection(),self.opciones_Diagramas))
        GButton_13.place(x=325, y=550, width=175, height=30)

        self.texto_seleccion_4 = tk.Text(root2, wrap=tk.WORD, width=23, height=2)
        self.texto_seleccion_4.place(x=100, y=540)
        
        titulo_texto_seleccion_4 = tk.Label(root2, text="Diagramas Impresión:", font=("Arial", 10, "bold"))
        titulo_texto_seleccion_4.place(x=100, y=510)

        # Variaciones

        GLabel_6 = tk.Label(root2, text="Variaciones", \
                              justify="center")
        GLabel_6.place(x=550, y=75, width=75, height=20)

        # Crear Frame contenedor para lista de Variaciones
        self.frame_contenedor_5 = tk.Frame(root2,bg="white")
        self.frame_contenedor_5.place(x=550, y=100, width=150, height=50)

        self.scrollbar_5 = tk.Scrollbar(self.frame_contenedor_5, orient=tk.VERTICAL)
        
        # Crear la lista desplegable con scroll para Variaciones
        self.lista_desplegable_5 = tk.Listbox(self.frame_contenedor_5, selectmode=tk.MULTIPLE, yscrollcommand=self.scrollbar_5.set)
        self.scrollbar_5.config(command=self.lista_desplegable_5.yview)
        self.scrollbar_5.pack(side=tk.RIGHT, fill=tk.Y)

        self.opciones_Variaciones=[]
        GButton_14 = tk.Button(root2, text="Actualizar Variaciones",  \
                      bg="#d9841d",fg="#000000", command=lambda: self.GButton_14_command())
        GButton_14.place(x=715, y=100, width=175, height=30)

        # Botón para mostrar la selección
        GButton_15 = tk.Button(root2, text="Seleccionar Variaciones",  \
                      bg="#d9841d",fg="#000000", command=lambda: self.GButton_15_command(self.lista_desplegable_5.curselection(),self.opciones_Variaciones))
        GButton_15.place(x=715, y=175, width=175, height=30)

        self.texto_seleccion_5 = tk.Text(root2, wrap=tk.WORD, width=17, height=2)
        self.texto_seleccion_5.place(x=550, y=175)
        
        titulo_texto_seleccion_5 = tk.Label(root2, text="Variaciones:", font=("Arial", 10, "bold"))
        titulo_texto_seleccion_5.place(x=550, y=150)

        GLabel_7 = tk.Label(root2, text="Definir Carácteristicas de Tiempo", \
                              justify="center")
        GLabel_7.place(x=550, y=250, width=200, height=20)

        GButton_16 = tk.Button(root2, text="Crear Carácteristicas",  \
                      bg="#d9841d",fg="#000000", command=lambda: self.GButton_16_command())
        GButton_16.place(x=550, y=280, width=150, height=30)

        GButton_17 = tk.Button(root2, text="Asignar Carácteristicas",  \
                      bg="#d9841d",fg="#000000", command=lambda: self.GButton_17_command())
        GButton_17.place(x=730, y=280, width=150, height=30)

        GButton_18 = tk.Button(root2, text="Asignar Zona",  \
                      bg="#d9841d",fg="#000000", command=lambda: self.GButton_18_command())
        GButton_18.place(x=650, y=380, width=150, height=30)
        
        GButton_19 = tk.Button(root2, text="Ejecutar Flujo",  \
                      bg="#d9841d",fg="#000000", command=lambda: self.GButton_19_command())
        GButton_19.place(x=650, y=500, width=150, height=50)

    def GButton_7_command(self, seleccion, opciones):
        print(opciones)
        print('Boton 7 presionado')
        print(seleccion)
        seleccion_texto = [opciones[index] for index in seleccion]
        self.Texto_Horas=seleccion_texto.copy()
        self.texto_seleccion_1.delete(1.0, tk.END)
        self.texto_seleccion_1.insert(tk.END, ", ".join(seleccion_texto))

    def GButton_8_command(self, seleccion, opciones):
        print(opciones)
        print('Boton 8 presionado')
        print(seleccion)
        seleccion_texto = [opciones[index] for index in seleccion]
        self.Texto_Escenarios=seleccion_texto.copy()
        self.texto_seleccion_2.delete(1.0, tk.END)
        self.texto_seleccion_2.insert(tk.END, ", ".join(seleccion_texto))
    
    def GButton_9_command(self, seleccion, opciones):
        print(opciones)
        print('Boton 9 presionado')
        print(seleccion)
        seleccion_texto = [str(opciones[index]) for index in seleccion]
        self.Texto_Años=seleccion_texto.copy()
        self.texto_seleccion_3.delete(1.0, tk.END)
        self.texto_seleccion_3.insert(tk.END, ", ".join(seleccion_texto))

    def GButton_10_command(self):
        print("Seleccionar Archivo")
        Directorio=filedialog.askdirectory(title="Abrir ruta PDFs")
        if Directorio: 
            self.Direccion_Entrada.set(Directorio)
            self.Nombre_Directorio=Directorio
    
    def GButton_11_command(self):
        print("Seleccionar Archivo")
        Directorio=filedialog.askdirectory(title="Abrir ruta Excel")
        if Directorio: 
            self.Direccion_Entrada_2.set(Directorio)
            self.Nombre_Directorio_2=Directorio

    def GButton_12_command(self):
        print("Buscar Diagramas")
        Folder_Diagramas=app.GetProjectFolder('dia')
        self.opciones_Diagramas.clear()
        app.PrintPlain(Folder_Diagramas)
        Diagramas=Folder_Diagramas.GetContents()
        self.lista_desplegable_4.delete(0, tk.END)
        for i in Diagramas:
            self.opciones_Diagramas.append(i.GetAttribute('loc_name'))
        
        for opcion in self.opciones_Diagramas:
            self.lista_desplegable_4.insert(tk.END, opcion)
        self.lista_desplegable_4.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def GButton_13_command(self, seleccion, opciones):
        print(opciones)
        print(seleccion)
        print('Boton 13 presionado')
        print(seleccion)
        seleccion_texto = [opciones[index] for index in seleccion]
        self.Diagramas_Texto=seleccion_texto.copy()
        self.texto_seleccion_4.delete(1.0, tk.END)
        self.texto_seleccion_4.insert(tk.END, ", ".join(seleccion_texto))   
    
    def GButton_14_command(self):
        print("Buscar Variaciones")
        Folder_Variaciones=app.GetProjectFolder('scheme')
        self.opciones_Variaciones.clear()
        app.PrintPlain(Folder_Variaciones)
        Variaciones=Folder_Variaciones.GetContents()
        self.lista_desplegable_5.delete(0, tk.END)
        for i in Variaciones:
            self.opciones_Variaciones.append(i.GetAttribute('loc_name'))
        
        for opcion in self.opciones_Variaciones:
            self.lista_desplegable_5.insert(tk.END, opcion)
        self.lista_desplegable_5.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def GButton_15_command(self, seleccion, opciones):
        print(opciones)
        print(seleccion)
        print('Boton 13 presionado')
        print(seleccion)
        seleccion_texto = [opciones[index] for index in seleccion]
        self.Texto_Variaciones=seleccion_texto.copy()
        self.texto_seleccion_5.delete(1.0, tk.END)
        self.texto_seleccion_5.insert(tk.END, ", ".join(seleccion_texto)) 

    def GButton_16_command(self):
        print("Caracteristicas")
        import Caracteristicas_Tiempo_2
        Caracteristicas_Tiempo_2.Funcion(self.Nombre_Fichero)

    def GButton_17_command(self):
        print("Caracteristicas")
        Cargas= pd.read_excel(self.Nombre_Fichero, sheet_name='Cargas')
        Caracteristicas_Circuito=pd.read_excel(self.Nombre_Fichero, sheet_name='Char_Tiempo')
        Caracteristicas_Circuito = Caracteristicas_Circuito.dropna(axis=1, how='all')
        Folder_Caracteristicas = app.GetProjectFolder('chars')
        for i, Carga in Cargas.iterrows():
            Nombre=Carga['NOMBRE']
            Tipo_Activa=Carga['Circuito_Activa']
            Tipo_Reactiva=Carga['Circuito_Reactiva']
            Carga_pf_0=app.GetCalcRelevantObjects(str(Nombre) + '.ElmLod')
            if not Carga_pf_0:
                continue
            Carga_pf=Carga_pf_0[0]
            app.PrintPlain(Carga_pf)
            Cha_Activa=Folder_Caracteristicas.GetContents(Tipo_Activa + '.ChaTime')[0]
            Cha_Reactiva=Folder_Caracteristicas.GetContents(Tipo_Reactiva + '.ChaTime')[0]
            P_Nombre_Circuito=Cha_Activa.GetAttribute('loc_name')
            Q_Nombre_Circuito=Cha_Reactiva.GetAttribute('loc_name')
            P_Max_Circuito=Caracteristicas_Circuito[P_Nombre_Circuito].max()
            Q_Max_Circuito=abs(Caracteristicas_Circuito[Q_Nombre_Circuito]).max()
            Carga_pf.plini=P_Max_Circuito*Carga['%_Activa']
            Carga_pf.qlini=Q_Max_Circuito*Carga['%_Reactiva']
            try:
                Referencia=Carga_pf.GetContents('*.ChaRef')
            except:
                Referencia=[]
            for i in Referencia:
                i.Delete()
            refObj =Carga_pf.CreateObject('ChaRef','plini')
            refObj.typ_id = Cha_Activa
            refObj = Carga_pf.CreateObject('ChaRef','qlini')
            refObj.typ_id = Cha_Reactiva  
    
    def GButton_18_command(self):
        print("Zonas")
        import Zonas
        Zonas.Funcion(self.Nombre_Fichero)

    def GButton_19_command(self):
        print("Flujos")
        import Flujos
        Flujos.Funcion(self.Nombre_Fichero,self.Texto_Variaciones,self.Texto_Escenarios, \
                       self.Texto_Años,self.Texto_Horas,self.Diagramas_Texto,\
                          self.Nombre_Directorio,self.Nombre_Directorio_2 )
    
    def open_Cordinacion_window(self):
        root4 = tk.Toplevel(self.root)
        root4.title("Aplicativo de EDC - Coordinación")
        width = 650
        height = 500
        screenwidth = root4.winfo_screenwidth()
        screenheight = root4.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root4.geometry(alignstr)

        # Crear un canvas y un frame general
        self.canvas_p = tk.Canvas(root4)
        self.frame_general_p = tk.Frame(self.canvas_p)

        # Crear un scrollbar y asociarlo al canvas
        self.scrollbar_p = tk.Scrollbar(root4, orient="vertical", command=self.canvas_p.yview)
        self.canvas_p.configure(yscrollcommand=self.scrollbar_p.set)

        # Empacar el canvas y el scrollbar en la ventana principal
        self.canvas_p.pack(side="left", fill="both", expand=True)
        self.scrollbar_p.pack(side="right", fill="y")

        frame_Sobrecorriente = tk.Frame(self.frame_general_p,bd=2, relief=tk.GROOVE,\
                                         width=600, height=580)
        frame_Sobrecorriente.pack(padx=10,pady=10)
        self.label_Sobrecorriente_p = tk.Label(frame_Sobrecorriente,\
                                        text="Proteccion Cabecera ")
        self.label_Sobrecorriente_p.place(x=10, y=10)



        self.label_TC_P_p = tk.Label(frame_Sobrecorriente, text="I Nom prim TC:")
        self.label_TC_P_p.place(x=10, y=30)
        self.entry_TC_P_p = tk.Entry(frame_Sobrecorriente)
        self.entry_TC_P_p.place(x=110, y=30)

        self.label_TC_S_p = tk.Label(frame_Sobrecorriente, text="I Nom sec TC:")
        self.label_TC_S_p.place(x=310, y=30)
        self.entry_TC_S_p = tk.Entry(frame_Sobrecorriente)
        self.entry_TC_S_p.place(x=410, y=30)



        self.frame_Proteccion_Fase_p = tk.Frame(frame_Sobrecorriente, bd=2, relief=tk.GROOVE)
        self.frame_Proteccion_Fase_p.place(x=10, y=60, width=250, height=250)
        self.label_Proteccion_Fase_p = tk.Label(self.frame_Proteccion_Fase_p, text="Temporizada (51F) ")
        self.label_Proteccion_Fase_p.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.Proteccion_Fase_p = tk.IntVar(value=0)
        check_Proteccion_Fase_p = tk.Checkbutton(self.frame_Proteccion_Fase_p, text=" ",
                                    variable=self.Proteccion_Fase_p, \
                                    onvalue=1, offvalue=0)
        check_Proteccion_Fase_p.place(x=150, y=5)

        # Formulario de falla_trifasica
        self.label_Pick_up_p = tk.Label(self.frame_Proteccion_Fase_p, text="Pick Up (A prim):")
        self.label_Pick_up_p.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_Pick_up_p = tk.Entry(self.frame_Proteccion_Fase_p)
        self.entry_Pick_up_p.grid(row=1, column=1, padx=10, pady=5)

        self.label_Dial_p = tk.Label(self.frame_Proteccion_Fase_p, text="Dial (s):")
        self.label_Dial_p.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_Dial_p = tk.Entry(self.frame_Proteccion_Fase_p)
        self.entry_Dial_p.grid(row=2, column=1, padx=10, pady=5)

        self.label_Curva_p = tk.Label(self.frame_Proteccion_Fase_p, text="Curva:")
        self.label_Curva_p.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        frame_contenedor_Curvas1 = tk.Frame(self.frame_Proteccion_Fase_p)
        frame_contenedor_Curvas1.place(x=50, y=100, width=200, height=70)
        scrollbar_Curvas51 = tk.Scrollbar(frame_contenedor_Curvas1, orient=tk.VERTICAL)
        lista_desplegable_Curvas51 = tk.Listbox(frame_contenedor_Curvas1, selectmode=tk.SINGLE, yscrollcommand=scrollbar_Curvas51.set)
        scrollbar_Curvas51.config(command=lista_desplegable_Curvas51.yview)
        scrollbar_Curvas51.pack(side=tk.RIGHT, fill=tk.Y)
        Curvas=["VI_IEC","NI_IEC","EI_IEC","NI_IEEE","VI_IEEE","EI_IEEE",\
                'EI_ANSI','VI_ANSI','NI_ANSI','TLI_ANSI','TLVI_ANSI','TLEI_ANSI','ITC_ANSI','EITC_ANSI']
       
        for opcion in Curvas:
            lista_desplegable_Curvas51.insert(tk.END, opcion)
        lista_desplegable_Curvas51.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.texto_seleccion_Curvas_Fase_p = tk.Text(self.frame_Proteccion_Fase_p,\
                                                   wrap=tk.WORD, width=17, height=1)
        self.texto_seleccion_Curvas_Fase_p.place(x=50, y=210)

        GButton_2 = tk.Button(self.frame_Proteccion_Fase_p, text="Seleccionar", bg="#d9841d", \
                      fg="#000000",\
                       command=lambda: self.GButton_2_command_p(lista_desplegable_Curvas51.curselection(),Curvas))
        GButton_2.place(x=50, y=175, width=175, height=30)


        self.label_Curva3_p = tk.Label(self.frame_Proteccion_Fase_p, text="Curva:")
        self.label_Curva3_p.place(x=10, y=210)



        self.frame_Proteccion_Tierra_p = tk.Frame(frame_Sobrecorriente, bd=2, relief=tk.GROOVE)
        self.frame_Proteccion_Tierra_p.place(x=310, y=60, width=250, height=250)
        self.label_Proteccion_Tierra_p = tk.Label(self.frame_Proteccion_Tierra_p, text="Temporizada (51N) ")
        self.label_Proteccion_Tierra_p.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.Proteccion_Tierra_p = tk.IntVar(value=0)
        check_Proteccion_Tierra_p = tk.Checkbutton(self.frame_Proteccion_Tierra_p, text=" ",
                                    variable=self.Proteccion_Tierra_p, \
                                    onvalue=1, offvalue=0)
        check_Proteccion_Tierra_p.place(x=150, y=5)


        # Formulario de falla_trifasica
        self.label_Pick_up2_p = tk.Label(self.frame_Proteccion_Tierra_p, text="Pick Up (A prim):")
        self.label_Pick_up2_p.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_Pick_up2_p = tk.Entry(self.frame_Proteccion_Tierra_p)
        self.entry_Pick_up2_p.grid(row=1, column=1, padx=10, pady=5)

        self.label_Dial2_p = tk.Label(self.frame_Proteccion_Tierra_p, text="Dial (s):")
        self.label_Dial2_p.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_Dial2_p = tk.Entry(self.frame_Proteccion_Tierra_p)
        self.entry_Dial2_p.grid(row=2, column=1, padx=10, pady=5)

        self.label_Curva2_p = tk.Label(self.frame_Proteccion_Tierra_p, text="Curva:")
        self.label_Curva2_p.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        frame_contenedor_Curvas2 = tk.Frame(self.frame_Proteccion_Tierra_p)
        frame_contenedor_Curvas2.place(x=50, y=100, width=200, height=70)
        scrollbar_Curvas512 = tk.Scrollbar(frame_contenedor_Curvas2, orient=tk.VERTICAL)
        lista_desplegable_Curvas512 = tk.Listbox(frame_contenedor_Curvas2, selectmode=tk.SINGLE,\
                                                  yscrollcommand=scrollbar_Curvas512.set)
        scrollbar_Curvas512.config(command=lista_desplegable_Curvas512.yview)
        scrollbar_Curvas512.pack(side=tk.RIGHT, fill=tk.Y)
        Curvas=["VI_IEC","NI_IEC","EI_IEC","NI_IEEE","VI_IEEE","EI_IEEE",\
                'EI_ANSI','VI_ANSI','NI_ANSI','TLI_ANSI','TLVI_ANSI','TLEI_ANSI','ITC_ANSI','EITC_ANSI']
        for opcion in Curvas:
            lista_desplegable_Curvas512.insert(tk.END, opcion)
        lista_desplegable_Curvas512.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.texto_seleccion_Curvas_Tierra_p = tk.Text(self.frame_Proteccion_Tierra_p,\
                                                   wrap=tk.WORD, width=17, height=1)
        self.texto_seleccion_Curvas_Tierra_p.place(x=50, y=210)

        GButton_3 = tk.Button(self.frame_Proteccion_Tierra_p, text="Seleccionar", bg="#d9841d", \
                      fg="#000000",\
                       command=lambda: self.GButton_3_command_p(lista_desplegable_Curvas512.curselection(),Curvas))
        GButton_3.place(x=50, y=175, width=175, height=30)
        self.label_Curva4_p = tk.Label(self.frame_Proteccion_Tierra_p, text="Curva:")
        self.label_Curva4_p.place(x=10, y=210)



        self.frame_Proteccion_Fase_I_p = tk.Frame(frame_Sobrecorriente, bd=2, relief=tk.GROOVE)
        self.frame_Proteccion_Fase_I_p.place(x=10, y=320, width=250, height=100)
        self.label_Proteccion_Fase_I_p = tk.Label(self.frame_Proteccion_Fase_I_p, text="Instantanea (50F) ")
        self.label_Proteccion_Fase_I_p.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.Proteccion_Fase_I_p = tk.IntVar(value=0)
        check_Proteccion_Fase_I_p = tk.Checkbutton(self.frame_Proteccion_Fase_I_p, text=" ",
                                    variable=self.Proteccion_Fase_I_p, \
                                    onvalue=1, offvalue=0)
        check_Proteccion_Fase_I_p.place(x=150, y=5)

        self.label_Pick_up4_p = tk.Label(self.frame_Proteccion_Fase_I_p, text="Pick Up (A prim):")
        self.label_Pick_up4_p.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_Pick_up4_p = tk.Entry(self.frame_Proteccion_Fase_I_p)
        self.entry_Pick_up4_p.grid(row=1, column=1, padx=10, pady=5)

        self.label_Pick_up4_p = tk.Label(self.frame_Proteccion_Fase_I_p, text="Delay (s):")
        self.label_Pick_up4_p.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_delay_Instantanea_Fase_p = tk.Entry(self.frame_Proteccion_Fase_I_p)
        self.entry_delay_Instantanea_Fase_p.grid(row=2, column=1, padx=10, pady=5)

        self.frame_Proteccion_Tierra_I_p = tk.Frame(frame_Sobrecorriente, bd=2, relief=tk.GROOVE)
        self.frame_Proteccion_Tierra_I_p.place(x=310, y=320, width=250, height=100)
        self.label_Proteccion_Tierra_I_p = tk.Label(self.frame_Proteccion_Tierra_I_p, text="Instantanea (50N) ")
        self.label_Proteccion_Tierra_I_p.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.Proteccion_Tierra_I_p = tk.IntVar(value=0)
        check_Proteccion_Tierra_I_p = tk.Checkbutton(self.frame_Proteccion_Tierra_I_p, text=" ",
                                    variable=self.Proteccion_Tierra_I_p, \
                                    onvalue=1, offvalue=0)
        check_Proteccion_Tierra_I_p.place(x=150, y=5)

        self.label_Pick_up3_p = tk.Label(self.frame_Proteccion_Tierra_I_p, text="Pick Up (A prim):")
        self.label_Pick_up3_p.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_Pick_up3_p = tk.Entry(self.frame_Proteccion_Tierra_I_p)
        self.entry_Pick_up3_p.grid(row=1, column=1, padx=10, pady=5)

        self.label_Pick_up3_p = tk.Label(self.frame_Proteccion_Tierra_I_p, text="Delay (s):")
        self.label_Pick_up3_p.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_delay_Instantanea_Tierra_p = tk.Entry(self.frame_Proteccion_Tierra_I_p)
        self.entry_delay_Instantanea_Tierra_p.grid(row=2, column=1, padx=10, pady=5)

        
        self.label_Sobrecorriente_p = tk.Label(frame_Sobrecorriente,\
                                        text="Nodo:")
        self.label_Sobrecorriente_p.place(x=20, y=430)

        self.Nodo_Cabecera_p = tk.Entry(frame_Sobrecorriente)
        self.Nodo_Cabecera_p.place(x=125, y=430)


        # Variable para almacenar la opción seleccionada
        self.opcion_p = tk.StringVar(value=None)

        # Crear los RadioButtons
        self.label_Sobrecorriente_p = tk.Label(frame_Sobrecorriente,\
                                        text="Elemento Sensado:")
        self.label_Sobrecorriente_p.place(x=320, y=430)

        self.Elemento_Sensado_Cabecera_p = tk.Entry(frame_Sobrecorriente)
        self.Elemento_Sensado_Cabecera_p.place(x=430, y=430)

        radio1 = tk.Radiobutton(frame_Sobrecorriente, text="External Grid",\
                                 variable=self.opcion_p, value=".ElmXnet")
        radio1.place(x=350, y=450)

        radio2 = tk.Radiobutton(frame_Sobrecorriente, text="Línea",\
                                 variable=self.opcion_p, value=".ElmLne")
        radio2.place(x=350, y=470)

        radio3 = tk.Radiobutton(frame_Sobrecorriente, text="Transformador",\
                                 variable=self.opcion_p, value=".ElmTr2")
        radio3.place(x=350, y=490)


        GButton_4 = tk.Button(frame_Sobrecorriente, text="Guardar Protección", bg="#d9841d", \
                              fg="#000000", command=self.GButton_4_command_p)
        GButton_4.place(x=75, y=480, width=175, height=30)



        frame_Sobrecorriente_PGF = tk.Frame(self.frame_general_p,bd=2, relief=tk.GROOVE, width=600, height=350)
        frame_Sobrecorriente_PGF.pack(padx=10,pady=10)
        self.label_Sobrecorriente_PGF_p = tk.Label(frame_Sobrecorriente_PGF,\
                                         text="Protección PGF ")
        self.label_Sobrecorriente_PGF_p.place(x=10, y=10)

        self.label_Barra_OR_MT_p = tk.Label(frame_Sobrecorriente_PGF, text="Barra MT OR:")
        self.label_Barra_OR_MT_p.place(x=10, y=35)
        self.entry_Barra_OR_MT_p = tk.Entry(frame_Sobrecorriente_PGF)
        self.entry_Barra_OR_MT_p.place(x=90, y=35)

        self.label_Barra_PGF_MT_p = tk.Label(frame_Sobrecorriente_PGF, text="Barra MT PGF:")
        self.label_Barra_PGF_MT_p.place(x=10, y=65)
        self.entry_Barra_PGF_MT_p = tk.Entry(frame_Sobrecorriente_PGF)
        self.entry_Barra_PGF_MT_p.place(x=90, y=65)

        self.label_Barra_PGF_BT_p = tk.Label(frame_Sobrecorriente_PGF, text="Barra BT PGF:")
        self.label_Barra_PGF_BT_p.place(x=10, y=95)
        self.entry_Barra_PGF_BT_p = tk.Entry(frame_Sobrecorriente_PGF)
        self.entry_Barra_PGF_BT_p.place(x=90, y=95)

        self.opcion_Cortos1_p = tk.IntVar(value=0)
        check_Corto1 = tk.Checkbutton(frame_Sobrecorriente_PGF, text=" ",
                                    variable=self.opcion_Cortos1_p, \
                                    onvalue=1, offvalue=0)
        check_Corto1.place(x=250, y=35)

        self.opcion_Cortos2_p = tk.IntVar(value=0)
        check_Corto2 = tk.Checkbutton(frame_Sobrecorriente_PGF, text=" ",
                                    variable=self.opcion_Cortos2_p,\
                                    onvalue=1, offvalue=0)
        check_Corto2.place(x=250, y=65)

        self.opcion_Cortos3_p = tk.IntVar(value=0)
        check_Corto3 = tk.Checkbutton(frame_Sobrecorriente_PGF, text=" ",
                                    variable=self.opcion_Cortos3_p,\
                                    onvalue=1, offvalue=0)
        check_Corto3.place(x=250, y=95)

        

  
        
        
        self.label_Fallas_p = tk.Label(frame_Sobrecorriente_PGF, text="R Falla MT:")
        self.label_Fallas_p.place(x=10, y=140)

        

        self.label_Fallas_p = tk.Label(frame_Sobrecorriente_PGF, text="R1")
        self.label_Fallas_p.place(x=90, y=120)

        self.entry_Falla1_p = tk.Entry(frame_Sobrecorriente_PGF,width=5)
        self.entry_Falla1_p.place(x=90, y=140)

        self.label_Fallas_p = tk.Label(frame_Sobrecorriente_PGF, text="R2")
        self.label_Fallas_p.place(x=135, y=120)

        self.entry_Falla2_p = tk.Entry(frame_Sobrecorriente_PGF,width=5)
        self.entry_Falla2_p.place(x=135, y=140)

        self.label_Fallas_p = tk.Label(frame_Sobrecorriente_PGF, text="R3")
        self.label_Fallas_p.place(x=180, y=120)

        self.entry_Falla3_p = tk.Entry(frame_Sobrecorriente_PGF,width=5)
        self.entry_Falla3_p.place(x=180, y=140)



                # Variable para almacenar la opción seleccionada
        self.opcion2_p = tk.StringVar(value=None)

        # Crear los RadioButtons
        self.label_Sensado_p = tk.Label(frame_Sobrecorriente_PGF,\
                                        text="Elemento Sensado:")
        self.label_Sensado_p.place(x=320, y=40)

        self.Elemento_Sensado_PGF_p = tk.Entry(frame_Sobrecorriente_PGF)
        self.Elemento_Sensado_PGF_p.place(x=430, y=40)

        radio4 = tk.Radiobutton(frame_Sobrecorriente_PGF, text="Interruptor",\
                                 variable=self.opcion2_p, value=".ElmCoup")
        radio4.place(x=350, y=70)

        radio5 = tk.Radiobutton(frame_Sobrecorriente_PGF, text="Línea",\
                                 variable=self.opcion2_p, value=".ElmLne")
        radio5.place(x=350, y=90)

        radio6 = tk.Radiobutton(frame_Sobrecorriente_PGF, text="Transformador",\
                                 variable=self.opcion2_p, value=".ElmTr2")
        radio6.place(x=350, y=110)

        self.label_Variacion_p = tk.Label(frame_Sobrecorriente_PGF,\
                                        text="Variación:")
        self.label_Variacion_p.place(x=330, y=140)

        self.Variacion_p = tk.Entry(frame_Sobrecorriente_PGF)
        self.Variacion_p.place(x=430, y=140)

       
        GButton_6 = tk.Button(frame_Sobrecorriente_PGF, text="Evaluar Corto", \
                    bg="#d9841d", fg="#000000", command=self.GButton_6_command_p)
        GButton_6.place(x=100, y=230, width=200, height=30)

        

        GButton_7 = tk.Button(frame_Sobrecorriente_PGF, text="Generar Resultados", \
                    bg="#d9841d", fg="#000000", command=self.GButton_7_command_p)
        GButton_7.place(x=300, y=230, width=200, height=30)


        self.Direccion_Entrada_Protecciones_p = tk.StringVar()
        # Crear el campo de texto con la variable de texto asociada
        self.Direccion1_Entry_Protecciones_p = tk.Entry(frame_Sobrecorriente_PGF, textvariable=self.Direccion_Entrada_Protecciones_p, state="readonly")
        self.Direccion1_Entry_Protecciones_p.place(x=100, y=270, width=200, height=25)

        GButton_10_P = tk.Button(frame_Sobrecorriente_PGF, text="Guardar Cordinación", \
                    bg="#d9841d", fg="#000000", command=self.GButton_10_P_command_p)
        GButton_10_P.place(x=300, y=270, width=175, height=30)


        label_T_Cordinación_Fase = tk.Label(frame_Sobrecorriente_PGF,\
                                        text="Delta Coordinación Fase (s):",wraplength=120)
        label_T_Cordinación_Fase.place(x=10, y=175)
        self.entry_Delta_PGF_OR_Fase_p = tk.Entry(frame_Sobrecorriente_PGF)
        self.entry_Delta_PGF_OR_Fase_p.place(x=150, y=175)

        label_T_Cordinación_Tierra = tk.Label(frame_Sobrecorriente_PGF,\
                                        text="Delta Coordinación Tierra (s):",wraplength=120)
        label_T_Cordinación_Tierra.place(x=330, y=175)
        
        self.entry_Delta_PGF_OR_Tierra_p = tk.Entry(frame_Sobrecorriente_PGF)
        self.entry_Delta_PGF_OR_Tierra_p.place(x=450, y=175)
       

        print('Hola Mundo')
        

        
        # Configurar el tamaño del frame general y ajustar el scrollregion del canvas
        frame_general_width = 100
        frame_general_height = 3000
        self.frame_general_p.configure(width=frame_general_width, height=frame_general_height)
        self.canvas_p.config(scrollregion=(0, 0, frame_general_width, frame_general_height))

        # Agregar el frame general al canvas
        self.canvas_p.create_window((0, 0), window=self.frame_general_p, anchor="nw")


    def GButton_2_command_p(self, seleccion, opciones):
        seleccion_texto = [opciones[index] for index in seleccion]
        self.texto_seleccion_Curvas_Fase_p.delete(1.0, tk.END)
        self.texto_seleccion_Curvas_Fase_p.insert(tk.END, ", ".join(seleccion_texto)) 

    
    def GButton_3_command_p(self, seleccion, opciones):
        seleccion_texto = [opciones[index] for index in seleccion]
        self.texto_seleccion_Curvas_Tierra_p.delete(1.0, tk.END)
        self.texto_seleccion_Curvas_Tierra_p.insert(tk.END, ", ".join(seleccion_texto)) 

    def GButton_4_command_p(self):
        RTC = int(self.entry_TC_P_p.get())/int(self.entry_TC_S_p.get())
        Curva51F = self.texto_seleccion_Curvas_Fase_p.get("1.0", "end-1c")
        Curva51N = self.texto_seleccion_Curvas_Tierra_p.get("1.0", "end-1c")
        Pick_up51F = self.entry_Pick_up_p.get() 
        Pick_up51N = self.entry_Pick_up2_p.get()
        Dial51F = self.entry_Dial_p.get()
        Dial51N = self.entry_Dial2_p.get()
        Pick_up50F = self.entry_Pick_up4_p.get()
        Pick_up50N = self.entry_Pick_up3_p.get()
        Delay_Instantaneo_T=self.entry_delay_Instantanea_Tierra_p.get()
        Delay_Instantaneo_F=self.entry_delay_Instantanea_Fase_p.get()
        Nodo=self.Nodo_Cabecera_p.get()
        Nombre_Sensado_Cabecera=self.Elemento_Sensado_Cabecera_p.get()
        Tipo_Sensado_Cabecera=self.opcion_p.get()
        Sensado=Nombre_Sensado_Cabecera + Tipo_Sensado_Cabecera
        Existe_51F=self.Proteccion_Fase_p.get()
        Existe_51N=self.Proteccion_Tierra_p.get()
        Existe_50F=self.Proteccion_Fase_I_p.get()
        Existe_50N=self.Proteccion_Tierra_I_p.get()
        Proteccion_Cabecera.Actualizar_Cabecera(RTC,Curva51F,Curva51N,Pick_up51F,\
        Pick_up51N,Dial51F,Dial51N,Pick_up50F,Pick_up50N,Delay_Instantaneo_T,\
            Delay_Instantaneo_F,Nodo,Sensado,Existe_51F,Existe_51N,\
                Existe_50F,Existe_50N)
        print('Hola Mundo')


    def GButton_6_command_p(self):
        Barra_MT_OR=self.entry_Barra_OR_MT_p.get()
        Barra_BT_PGF=self.entry_Barra_PGF_BT_p.get()
        Barra_MT_PGF=self.entry_Barra_PGF_MT_p.get()
        R_Falla_1=self.entry_Falla1_p.get()
        R_Falla_2=self.entry_Falla2_p.get()
        R_Falla_3=self.entry_Falla3_p.get() 
        Variacion=self.Variacion_p.get()
        Nombre=self.Elemento_Sensado_PGF_p.get()
        Tipo=self.opcion2_p.get()
        Sensado= Nombre + Tipo
        Barras_Corto=[Barra_MT_OR,Barra_MT_PGF,Barra_BT_PGF]
        Seleccion_Corto=[self.opcion_Cortos1_p.get(),self.opcion_Cortos2_p.get(),self.opcion_Cortos3_p.get()]
        Nodos_Corto=[]
        k=0
        for i in Seleccion_Corto:
            if i==1:
                Nodos_Corto.append(Barras_Corto[k])
            k=k+1
        self.Elementos_Corto_p=Nodos_Corto

        Curva_Proyecto.Actualizar_Curva_PGF(Barra_MT_OR,Barra_BT_PGF,Barra_MT_PGF,\
                                R_Falla_1,R_Falla_2,R_Falla_3,Variacion,Sensado)
        
        Delta_Fase=self.entry_Delta_PGF_OR_Fase_p.get()
        Delta_Tierra=self.entry_Delta_PGF_OR_Tierra_p.get()
        
        import Corto_2
        self.Lista_Frames_Fase_p,self.Lista_Frames_Tierra_p,self.Diccionario_Curvas_PGF_p,\
            self.Lista_Frames_Tensiones_p=Corto_2.Funcion(Proteccion_Cabecera,Curva_Proyecto,Nodos_Corto,\
                                                          Delta_Fase,Delta_Tierra)

        print('Hola Mundo')

    def GButton_10_P_command_p(self):
        print("Seleccionar Archivo")
        Directorio=filedialog.askdirectory(title="Abrir ruta")
        if Directorio: 
            self.Direccion_Entrada_Protecciones_p.set(Directorio)
            self.Nombre_Directorio_Protecciones_p=Directorio

    def GButton_7_command_p(self):
        Nodo_MT=Curva_Proyecto.Barra_MT_OR
        Nodo_BT=Curva_Proyecto.Barra_BT_PGF
        RFalla1=Curva_Proyecto.RFalla_1
        RFalla2=Curva_Proyecto.RFalla_2
        RFalla3=Curva_Proyecto.RFalla_3
        Resistencias_Falla=[RFalla1,RFalla2,RFalla3]
        import Resultados_Temporal
        Resultados_Temporal.Funcion(self.Lista_Frames_Fase_p,self.Lista_Frames_Tierra_p,self.Lista_Frames_Tensiones_p,\
                            Proteccion_Cabecera,self.Nombre_Directorio_Protecciones_p,\
                                self.Diccionario_Curvas_PGF_p,Curva_Proyecto)
        import Graficas_Cordinacion
        Graficas_Cordinacion.Funcion(self.Lista_Frames_Fase_p,self.Lista_Frames_Tierra_p,\
                                    Proteccion_Cabecera,self.Nombre_Directorio_Protecciones_p,\
                                        self.Diccionario_Curvas_PGF_p)


            

if __name__ == "__main__":
    root = tk.Tk()
    Aplicacion = App(root)
    root.mainloop()
