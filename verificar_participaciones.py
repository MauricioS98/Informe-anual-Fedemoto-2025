import pandas as pd

excel_path = "Informes/Valida de ejemplo/valejempo.xlsx"
print("Analizando Excel para verificar participaciones...")

excel_file = pd.ExcelFile(excel_path)
df = pd.read_excel(excel_file, sheet_name='Hoja1')

print(f"\nTotal de filas: {len(df)}")

# Identificar columnas de categorías
columnas_info = ['Consecutivo', 'Licencia', 'TX', 'Nombre', 'Apellido', 'Liga', 
                'Club', 'FN', 'RH', 'MOTO', 'Documento', 'EPS', 'Pago Licencia', 
                'Poliza', 'Celular', 'Mail', 'Formatos']

columnas_categorias = []
for col in df.columns:
    if col not in columnas_info and str(col) != 'nan':
        columnas_categorias.append(col)

print(f"\nColumnas de categorías encontradas: {columnas_categorias}")

# Contar participaciones (cada "x" cuenta como una participación)
total_participaciones = 0
participaciones_por_categoria = {}

for categoria in columnas_categorias:
    # Contar cuántas "x" hay en esta categoría
    count = 0
    for idx, row in df.iterrows():
        valor = row.get(categoria, None)
        if pd.notna(valor):
            valor_str = str(valor).upper().strip()
            if valor_str in ['X', 'X ', ' X']:
                count += 1
                total_participaciones += 1
    
    if count > 0:
        participaciones_por_categoria[categoria] = count
        print(f"{categoria}: {count} participaciones")

print(f"\nTotal de participaciones contadas: {total_participaciones}")

# Verificar fila por fila para debugging
print("\nVerificando primeras 10 filas:")
for idx in range(min(10, len(df))):
    row = df.iloc[idx]
    licencia = row.get('Licencia', 'N/A')
    participaciones_fila = 0
    categorias_fila = []
    
    for categoria in columnas_categorias:
        valor = row.get(categoria, None)
        if pd.notna(valor):
            valor_str = str(valor).upper().strip()
            if valor_str in ['X', 'X ', ' X']:
                participaciones_fila += 1
                categorias_fila.append(categoria)
    
    if participaciones_fila > 0:
        print(f"  Licencia {licencia}: {participaciones_fila} participaciones en {categorias_fila}")

