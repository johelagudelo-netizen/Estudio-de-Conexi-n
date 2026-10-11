# Aplicativo de EDC

Aplicativo de escritorio (Python / Tkinter) para agilizar Estudios de Conexión
Simplificados con DIgSILENT PowerFactory: construcción de la red desde Excel,
flujo de carga, cortocircuito y coordinación de protecciones de sobrecorriente.

## Requisitos
- DIgSILENT PowerFactory 2024.
- Python 3.10, 3.11 o 3.12 (debe existir en `<instalación>\Python\<versión>`).
- `pip install -r requirements.txt`

## Configuración de PowerFactory
`config_powerfactory.py` busca la instalación en este orden:
1. Variable de entorno `POWERFACTORY_PATH` (carpeta que contiene `PowerFactory.exe`).
2. `D:\Digsilent\Sofware`
3. `C:\Program Files\DIgSILENT\PowerFactory 20xx`

## Ejecución
```
py -3.11 Aplicacion_Principal.py
```
