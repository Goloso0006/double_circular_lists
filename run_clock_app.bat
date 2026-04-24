@echo off
setlocal

cd /d "%~dp0"

set "PYTHON_EXE=%~dp0.clock_env\Scripts\python.exe"
if not exist "%PYTHON_EXE%" (
  echo [ERROR] No se encontro el entorno en .clock_env\Scripts\python.exe
  echo Crea o selecciona el entorno correcto antes de ejecutar.
  pause
  exit /b 1
)

echo Iniciando Clock App con Streamlit...
echo URL local: http://localhost:8501
start "" "http://localhost:8501"
"%PYTHON_EXE%" -m streamlit run presentation/streamlit_app.py --server.headless true

if errorlevel 1 (
  echo.
  echo [ERROR] La app termino con errores.
  pause
)

endlocal
