# read two excel files and save the data in two dataframes
# compare the dataframes and save the differences in a new dataframe
# save the differences in a new excel file

import numpy as np
import pandas as pd

actual = pd.read_excel("docs/Actual.xlsx", skiprows=2)
anterior = pd.read_excel("docs/Anterior.xlsx", skiprows=2)

# delete de columns 0, 1, 5 ,6 ,7 y 8 from the dataframes
actual = actual.drop(actual.columns[[0, 1, 5, 6, 8]], axis=1)
anterior = anterior.drop(anterior.columns[[0, 1, 5, 6, 8]], axis=1)

# elimina las casillas en blanco
actual = actual.dropna()
anterior = anterior.dropna()

# agrega una columna que sea la divicion entre la columna Total y la columna Cantidad en ambos dataframes
actual["Costo Unitario IVA"] = actual["Total"] / actual["Cantidad"]
anterior["Costo Unitario IVA"] = anterior["Total"] / anterior["Cantidad"]

actual["Costo Unitario"] = actual["Neto"] / actual["Cantidad"]
anterior["Costo Unitario"] = anterior["Neto"] / anterior["Cantidad"]


# print the dataframes
print(actual)
print(anterior)


# compare the dataframes actual and anterior, looking for differences on column Costo Unitario and save the differences between rows in a new dataframe
merged_df = pd.merge(
    actual, anterior, on="Descripcion_", suffixes=("_actual", "_anterior")
)

# Find rows where 'Costo Unitario' values differ
merged_df["diff"] = (
    np.isclose(
        merged_df["Costo Unitario_actual"],
        merged_df["Costo Unitario_anterior"],
        atol=0.01,  # Tolerancia absoluta, ajusta este valor según sea necesario
    )
    == False
)  # Usamos 'False' para encontrar donde NO son cercanos

# agrega una columna que sea la resta entre el costo unitario actual y el costo unitario anterior
merged_df["Diferencia(act - ant)"] = (
    merged_df["Costo Unitario_actual"] - merged_df["Costo Unitario_anterior"]
)

# redondea la columna que acabamos de crear a dos decimales
merged_df["Diferencia(act - ant)"] = merged_df["Diferencia(act - ant)"].round(2)

differences = merged_df[merged_df["diff"]]

# elimina la columna diff
differences = differences.drop(
    columns=[
        "diff",
        "Neto_actual",
        "Total_actual",
        "Neto_anterior",
        "Total_anterior",
        "Costo Unitario IVA_actual",
        "Costo Unitario IVA_anterior",
        "Medida_anterior",
    ]
)
# cambia el nombre de la columna Medida_actual a Medida
differences = differences.rename(columns={"Medida_actual": "Medida"})

# print the differences
print(differences)

# save the differences in a new excel file
differences.to_excel("differences.xlsx", index=False)
