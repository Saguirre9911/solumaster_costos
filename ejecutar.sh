#has un codigo en sh que cree un entorno virutal en windows , lo active y ejecute dos script en python el de src/costs_comp/costs_variation.py y después el de src/costs_comp/rentability.py

# Crear entorno virtual con python 3.11 si no está creado
if [ ! -d "solumaster-costos-3.11" ]; then
    python -m venv env
fi

# Activar entorno virtual
source env/Scripts/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar scripts
python src/costs_comp/costs_variation.py
python src/costs_comp/rentability.py

# Desactivar entorno virtual
deactivate