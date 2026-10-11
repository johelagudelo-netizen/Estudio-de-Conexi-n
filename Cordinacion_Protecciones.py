import tkinter as tk
import random
import pandas as pd
from tkinter import messagebox
from tkinter import filedialog
#from pandastable import Table
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import sys
import config_powerfactory  # ruta de PowerFactory: ver config_powerfactory.py
import powerfactory as pf
app = pf.GetApplication()

app.Show()


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


     def Actualizar_Cabecera(self,RTC,Curva51F,Curva51N,Pick_up51F,\
        Pick_up51N,Dial51F,Dial51N,Pick_up50F,Pick_up50N,Delay_Instantaneo_T,\
            Delay_Instantaneo_F,Nodo,Sensado):
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
    def __init__(self, root4):
        self.root4 = root4
        self.root4.title("Frames en Frame con Scrollbar")
        self.Diccionario_Resultados_p={}
        self.Diccionario_Tensiones_p={}

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
        Curvas=["VI_IEC","NI_IEC","EI_IEC","NI_IEEE","VI_IEEE","EI_IEEE"]
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
        Curvas=["VI_IEC","NI_IEC","EI_IEC","NI_IEEE","VI_IEEE","EI_IEEE"]
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



        frame_Sobrecorriente_PGF = tk.Frame(self.frame_general_p,bd=2, relief=tk.GROOVE, width=600, height=250)
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

        radio4 = tk.Radiobutton(frame_Sobrecorriente_PGF, text="External Grid",\
                                 variable=self.opcion2_p, value=".ElmXnet")
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
        GButton_6.place(x=100, y=180, width=200, height=30)

        

        GButton_7 = tk.Button(frame_Sobrecorriente_PGF, text="Generar Resultados", \
                    bg="#d9841d", fg="#000000", command=self.GButton_7_command_p)
        GButton_7.place(x=300, y=180, width=200, height=30)


        self.Direccion_Entrada_Protecciones_p = tk.StringVar()
        # Crear el campo de texto con la variable de texto asociada
        self.Direccion1_Entry_Protecciones_p = tk.Entry(frame_Sobrecorriente_PGF, textvariable=self.Direccion_Entrada_Protecciones_p, state="readonly")
        self.Direccion1_Entry_Protecciones_p.place(x=100, y=220, width=200, height=25)

        GButton_10_P = tk.Button(frame_Sobrecorriente_PGF, text="Guardar Cordinación", \
                    bg="#d9841d", fg="#000000", command=self.GButton_10_P_command_p)
        GButton_10_P.place(x=300, y=220, width=175, height=30)
        
       

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
        Proteccion_Cabecera.Actualizar_Cabecera(RTC,Curva51F,Curva51N,Pick_up51F,\
        Pick_up51N,Dial51F,Dial51N,Pick_up50F,Pick_up50N,Delay_Instantaneo_T,\
            Delay_Instantaneo_F,Nodo,Sensado)
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
        
        import Corto_2
        self.Lista_Frames_Fase_p,self.Lista_Frames_Tierra_p,self.Diccionario_Curvas_PGF_p,\
            self.Lista_Frames_Tensiones_p=Corto_2.Funcion(Proteccion_Cabecera,Curva_Proyecto,Nodos_Corto)

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


        
    



 #---------------------------


# Crear la ventana principal y ejecutar la aplicación
root4 = tk.Tk()
aplicacion = App(root4)
root4.mainloop()
