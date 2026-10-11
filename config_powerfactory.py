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


# ---------------------------------------------------------------------------
# Utilidades de velocidad
# ---------------------------------------------------------------------------
import contextlib
import time


def indexar_por_nombre(objetos):
    """{loc_name: objeto}. Si hay nombres repetidos queda el primero (igual que [0])."""
    indice = {}
    for objeto in objetos:
        indice.setdefault(objeto.loc_name, objeto)
    return indice


def buscar(indice, nombre, descripcion):
    """Objeto por nombre, con un mensaje claro si no existe."""
    try:
        return indice[nombre]
    except KeyError:
        raise KeyError("No existe %s '%s' en el modelo de PowerFactory" % (descripcion, nombre)) from None


def siguiente_cubiculo(bus, contadores):
    """Nombre 'Cub_N' del siguiente cubículo del nodo sin releer su contenido cada vez."""
    clave = bus.loc_name
    if clave not in contadores:
        contadores[clave] = len(bus.GetContents())
    contadores[clave] += 1
    return 'Cub_' + str(contadores[clave])


@contextlib.contextmanager
def modo_rapido(app, nombre='Proceso'):
    """Silencia el eco de comandos y la actualización de pantalla mientras dura el bloque.

    Cada llamada es opcional: si esa versión de PowerFactory no la tiene se omite.
    Al terminar imprime el tiempo total en la ventana de salida.
    """
    reversas = []
    for activar, desactivar in (('EchoOff', 'EchoOn'),):
        try:
            getattr(app, activar)()
            reversas.append((desactivar,))
        except Exception:
            pass
    try:
        app.SetGuiUpdateEnabled(0)
        reversas.append(('SetGuiUpdateEnabled', 1))
    except Exception:
        pass
    inicio = time.perf_counter()
    try:
        yield
    finally:
        for paso in reversas:
            try:
                getattr(app, paso[0])(*paso[1:])
            except Exception:
                pass
        try:
            app.PrintPlain('%s: %.1f s' % (nombre, time.perf_counter() - inicio))
        except Exception:
            pass
