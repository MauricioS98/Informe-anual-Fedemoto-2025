import pandas as pd
import sys

excel_path = "Informes/Valida de ejemplo/valejempo.xlsx"

print("Analizando estructura del Excel...")
excel_file = pd.ExcelFile(excel_path)

for sheet_name in excel_file.sheet_names:
    print(f"\n{'='*80}")
    print(f"Hoja: {sheet_name}")
    print(f"{'='*80}")
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    
    print(f"\nDimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
    print(f"\nNombres de columnas:")
    for i, col in enumerate(df.columns):
        print(f"  {i}: {col}")
    
    print(f"\nPrimeras 10 filas:")
    print(df.head(10).to_string())
    
    print(f"\nTipos de datos:")
    print(df.dtypes)

