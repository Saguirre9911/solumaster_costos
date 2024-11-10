import numpy as np
import pandas as pd

# Cargar los datos
rentabilidad_df = pd.read_excel("src/costs_comp/docs/RENTABILIDAD.xlsx", skiprows=2)
inventarios_compras_df = pd.read_excel("src/costs_comp/docs/INVENTARIOS-COMPRAS.xlsx", skiprows=2)

# Eliminar columnas innecesarias en rentabilidad_df
columns_to_drop = ["Bodega", "Grupo Uno", "Grupo Dos"]
rentabilidad_df.drop(columns=columns_to_drop, axis=1, inplace=True)

# Eliminar columnas innecesarias en inventarios_compras_df
columns_to_drop = ["Cantidad", "Valor Unitario", "Iva", "IvaTotal", "Dcto", "Descuento", "Valor Neto"]
inventarios_compras_df.drop(columns=columns_to_drop, axis=1, inplace=True)

# Convertir la columna de fecha a tipo datetime en inventarios_compras_df
inventarios_compras_df['Fecha'] = pd.to_datetime(inventarios_compras_df['Fecha'], format='%d/%m/%Y')

# Obtener la última fecha de compra por producto
latest_purchase_per_product = inventarios_compras_df.groupby('Producto')['Fecha'].max().reset_index()

# Extraer el año y el mes de la última compra
latest_purchase_per_product['LastPurchaseMonth'] = latest_purchase_per_product['Fecha'].dt.to_period('M')

# Merge para añadir el mes de la última compra a cada producto en inventarios_compras_df
inventarios_compras_df = inventarios_compras_df.merge(latest_purchase_per_product[['Producto', 'LastPurchaseMonth']], on='Producto', how='left')

# Crear un DataFrame vacío para almacenar los productos con diferencias
products_with_differences = pd.DataFrame()

# Iterar sobre cada producto para buscar diferencias en el 'Valor Unitario Neto'
for producto in inventarios_compras_df['Producto'].unique():
    # Obtener las compras del producto en orden cronológico descendente
    product_data = inventarios_compras_df[inventarios_compras_df['Producto'] == producto].sort_values(by='Fecha', ascending=False)

    # Guardar el valor del precio más reciente para comparar con compras anteriores
    latest_price = None
    
    # Iterar sobre cada compra (desde la más reciente hacia atrás) y verificar diferencias en el 'Valor Unitario Neto'
    for idx, row in product_data.iterrows():
        current_price = row['Valor Unitario Neto']
        
        # Si es la primera iteración, asignar el precio más reciente y continuar
        if latest_price is None:
            latest_price = current_price
            continue
        
        # Comparar con el último precio guardado (más reciente)
        if current_price != latest_price:
            # Si hay una diferencia, agregar las filas correspondientes al DataFrame
            latest_difference = product_data[(product_data['Fecha'] == row['Fecha']) | (product_data['Fecha'] == product_data.iloc[0]['Fecha'])]
            products_with_differences = pd.concat([products_with_differences, latest_difference])
            break  # Salir del bucle si se encuentra una diferencia entre meses
        
        # Actualizar el precio de comparación
        latest_price = current_price

# Organizar el DataFrame final por Producto y Fecha en orden ascendente
products_with_differences = products_with_differences.sort_values(by=['Producto', 'Fecha']).reset_index(drop=True)

# Ver el resultado
print(products_with_differences[['Producto', 'Fecha', 'DocumentoNúmero', 'Proveedores', 'UnidadDeMedida', 'Valor Unitario Neto']])

# guarda products_with_differences en un archivo excel
products_with_differences.to_excel("src/costs_comp/docs/salida_products_with_differences.xlsx", index=False)