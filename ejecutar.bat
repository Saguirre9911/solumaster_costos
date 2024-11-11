:: Crear entorno virtual con Python 3.11 si no está creado
if not exist "solumaster-costos-3.11" (
    python -m venv solumaster-costos-3.11
)

:: Activar entorno virtual
call solumaster-costos-3.11\Scripts\activate.bat

:: Instalar dependencias
pip install -r requirements.txt

:: Ejecutar scripts
python src/costs_comp/costs_variation.py
python src/costs_comp/rentability.py

:: Desactivar entorno virtual
deactivate
