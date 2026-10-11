def Funcion(Fichero):
    import sys
    sys.path.append(r'C:\Program Files\DIgSILENT\PowerFactory 2021 SP2\Python\3.9')
    import powerfactory as pf
    import pandas as pd
    app = pf.GetApplication()
    Zonas = pd.read_excel(Fichero, sheet_name='Zonas')
    Zonas = Zonas.dropna(axis=1, how='all')
    Folder_Zonas = app.GetDataFolder('ElmZone')
    for i, Zona in Zonas.iterrows():
        Nombre=Zona['Nombre']
        Zona_pf=Folder_Zonas.GetContents(Nombre + '.ElmZone')            
        if not Zona_pf:
            Zona_pf=Folder_Zonas.CreateObject('ElmZone',Nombre)
            Zona_pf.curscale=Zona['Factor']
        else:
             Zona_pf=Zona_pf[0]
               
    Nodos=app.GetCalcRelevantObjects('*.ElmTerm')
    Cuenta=0
    for i in Nodos:
            app.PrintPlain(i)
            Nodo=i
            Nodo.cpZone=Zona_pf 
            Cuenta=Cuenta+1
