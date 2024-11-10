import pandas as pd

# Leer los archivos
products_with_differences = pd.read_excel("src/costs_comp/docs/products_with_differences.xlsx")
rentabilidad_df = pd.read_excel("src/costs_comp/docs/RENTABILIDAD.xlsx", skiprows=2)

# Eliminar columnas innecesarias en rentabilidad_df
columns_to_drop = ["Bodega", "Grupo Uno", "Grupo Dos"]
rentabilidad_df.drop(columns=columns_to_drop, axis=1, inplace=True)

# Separar el prefijo 'FC' del número en la columna DocumentoNúmero
products_with_differences[['Prefix', 'DocNumber']] = products_with_differences['DocumentoNúmero'].str.extract(r'(\D+)\s*(\d+)')
products_with_differences['DocNumber'] = products_with_differences['DocNumber'].astype(int)

# Obtener el valor único de cada producto basado en el DocumentoNúmero más alto
unique_products = products_with_differences.loc[products_with_differences.groupby('Producto')['DocNumber'].idxmax()]

# Eliminar las columnas auxiliares 'Prefix' y 'DocNumber'
unique_products = unique_products.drop(columns=['Prefix', 'DocNumber'])

# Realizar un merge para obtener los valores de 'Valor Unitario Neto' en 'rentabilidad_df'
# Nos aseguramos de que 'Descripcion' en rentabilidad_df coincida con 'Producto' en unique_products
updated_rentabilidad_df = rentabilidad_df.merge(unique_products[['Producto', 'Valor Unitario Neto']], left_on='Descripcion', right_on='Producto', how='left')

# Actualizar la columna 'Costo' con los valores de 'Valor Unitario Neto' donde haya coincidencia de Descripcion
updated_rentabilidad_df['Costo'] = updated_rentabilidad_df['Valor Unitario Neto'].combine_first(updated_rentabilidad_df['Costo'])

# Eliminar las columnas auxiliares 'Producto' y 'Valor Unitario Neto'
updated_rentabilidad_df = updated_rentabilidad_df.drop(columns=['Producto', 'Valor Unitario Neto'])

# Calcular la columna 'Rentabilidad' como la diferencia entre 'Precio 1' y 'Costo'
updated_rentabilidad_df['Rentabilidad'] = updated_rentabilidad_df['Precio 1'] - updated_rentabilidad_df['Costo']

# Calcular la columna '%' como (1 - Costo / Precio 1) * 100
updated_rentabilidad_df['%'] = (1 - updated_rentabilidad_df['Costo'] / updated_rentabilidad_df['Precio 1']) * 100

updated_rentabilidad_df.dropna(subset=['Descripcion'], inplace=True)
# Guardar el resultado actualizado en un nuevo archivo Excel
updated_rentabilidad_df.to_excel("src/costs_comp/docs/salida_updated_rentabilidad.xlsx", index=False)


# Ver el resultado
print(updated_rentabilidad_df)

