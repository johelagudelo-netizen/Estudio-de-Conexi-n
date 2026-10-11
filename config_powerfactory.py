# -*- coding: utf-8 -*-
"""
Localiza DIgSILENT PowerFactory y deja listo `import powerfactory`.

Orden de búsqueda de la carpeta de instalación (la que contiene PowerFactory.exe):
  1. Variable de entorno POWERFACTORY_PATH (ej. D:\\Digsilent\\Sofware)
  2. D:\\Digsilent\\Sofware
  3. Instalaciones estándar en C:\\Program Files\\DIgSILENT\\PowerFactory 2025/2024/2023/2022/2021*

Dentro de la instalación se usa la carpeta Python\\<versión> que coincida con el
Python que ejecuta el aplicativo (ej. Python\\3.11). Si no existe, se informa
cuáles hay disponibles.

Basta con importar este módulo antes de `import powerfactory`.
"""
import glob
import os
import sys

RUTA_POR_DEFECTO = r'D:\Digsilent\Sofware'
_CARPETAS_ESTANDAR = r'C:\Program Files\DIgSILENT\PowerFactory 20*'


def _instalaciones_candidatas():
    candidatas = []
    ruta_entorno = os.environ.get('POWERFACTORY_PATH')
    if ruta_entorno:
        candidatas.append(ruta_entorno)
    candidatas.append(RUTA_POR_DEFECTO)
    # Versiones más nuevas primero
    candidatas.extend(sorted(glob.glob(_CARPETAS_ESTANDAR), reverse=True))
    return [c for c in candidatas if os.path.isdir(c)]


def _versiones_python(instalacion):
    carpeta = os.path.join(instalacion, 'Python')
    if not os.path.isdir(carpeta):
        return []
    return sorted(d for d in os.listdir(carpeta)
                  if os.path.isfile(os.path.join(carpeta, d, 'powerfactory.pyd')))


def preparar_powerfactory():
    """Agrega PowerFactory a sys.path / DLLs y devuelve la ruta usada."""
    mi_version = '%d.%d' % sys.version_info[:2]
    revisadas = []
    for instalacion in _instalaciones_candidatas():
        disponibles = _versiones_python(instalacion)
        revisadas.append('%s (Python disponible: %s)' % (instalacion, ', '.join(disponibles) or 'ninguno'))
        if mi_version not in disponibles:
            continue
        ruta_pyd = os.path.join(instalacion, 'Python', mi_version)
        if ruta_pyd not in sys.path:
            sys.path.append(ruta_pyd)
        # Python >= 3.8 en Windows ya no busca DLL en PATH: PowerFactory lo exige.
        if hasattr(os, 'add_dll_directory'):
            os.add_dll_directory(instalacion)
        return ruta_pyd
    raise RuntimeError(
        'No se encontró un PowerFactory compatible con Python %s.\n'
        'Defina la variable de entorno POWERFACTORY_PATH con la carpeta de instalación '
        '(la que contiene PowerFactory.exe) o ejecute el aplicativo con una versión de '
        'Python que exista en <instalación>\\Python.\n\nRevisado:\n%s'
        % (mi_version, '\n'.join(revisadas) or '(ninguna instalación encontrada)'))


RUTA_PYD = preparar_powerfactory()
