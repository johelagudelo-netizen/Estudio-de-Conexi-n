@echo off
rem Genera dist\AplicativoEDC\AplicativoEDC.exe (modo carpeta: abre mucho mas rapido que un solo archivo).
rem Requisito: Python 3.11 instalado (debe existir en <instalacion de PowerFactory>\Python\3.11).
setlocal
cd /d "%~dp0"

if not exist .venv-build (
    py -3.11 -m venv .venv-build || goto :error
)
call .venv-build\Scripts\activate.bat || goto :error
python -m pip install --upgrade pip || goto :error
pip install -r requirements.txt pyinstaller || goto :error

rem powerfactory.pyd NO se empaqueta: se carga en tiempo de ejecucion desde la instalacion de DIgSILENT.
pyinstaller --noconfirm --clean --onedir --name AplicativoEDC ^
    --hidden-import openpyxl ^
    --hidden-import matplotlib.backends.backend_tkagg ^
    --collect-data pyproj ^
    --exclude-module powerfactory ^
    Aplicacion_Principal.py || goto :error

echo.
echo Listo: dist\AplicativoEDC\AplicativoEDC.exe
echo Copie TODA la carpeta dist\AplicativoEDC para distribuirlo.
goto :fin

:error
echo.
echo Hubo un error. Revise los mensajes de arriba.
exit /b 1

:fin
endlocal
