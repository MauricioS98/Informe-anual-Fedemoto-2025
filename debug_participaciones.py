import pandas as pd
import unicodedata

def normalizar_liga(nombre):
    if pd.isna(nombre) or nombre == '':
        return None
    nombre = str(nombre).strip()
    nombre = unicodedata.normalize('NFD', nombre)
    nombre = ''.join(c for c in nombre if unicodedata.category(c) != 'Mn')
    nombre = nombre.upper()
    return nombre

excel_path = "Informes/Valida de ejemplo/valejempo.xlsx"
excel_file = pd.ExcelFile(excel_path)
df = pd.read_excel(excel_file, sheet_name='Hoja1')

columnas_info = ['Consecutivo', 'Licencia', 'TX', 'Nombre', 'Apellido', 'Liga', 
                'Club', 'FN', 'RH', 'MOTO', 'Documento', 'EPS', 'Pago Licencia', 
                'Poliza', 'Celular', 'Mail', 'Formatos']

columnas_categorias = []
for col in df.columns:
    if col not in columnas_info and str(col) != 'nan':
        if df[col].notna().any():
            valores_unicos = df[col].dropna().unique()
            if any(str(v).upper().strip() in ['X', 'x', 'X ', ' x'] for v in valores_unicos):
                columnas_categorias.append(col)

print(f"Categorías encontradas: {columnas_categorias}")

total_participaciones = 0
participaciones_detalle = {}

for idx, row in df.iterrows():
    licencia = row.get('Licencia', None)
    liga = row.get('Liga', None)
    
    if pd.isna(licencia) or pd.isna(liga):
        continue
    
    licencia = int(licencia) if isinstance(licencia, (int, float)) else licencia
    
    for categoria in columnas_categorias:
        valor_categoria = row.get(categoria, None)
        
        if pd.notna(valor_categoria):
            valor_str = str(valor_categoria).upper().strip()
            # Probar diferentes variaciones de "x"
            if valor_str in ['X', 'x', 'X ', ' x', 'X  ']:
                total_participaciones += 1
                if categoria not in participaciones_detalle:
                    participaciones_detalle[categoria] = 0
                participaciones_detalle[categoria] += 1
                
                # Debug: mostrar valores que no se detectan como "x"
                if valor_str not in ['X', 'x']:
                    print(f"DEBUG: Licencia {licencia}, Categoría {categoria}, Valor: '{valor_categoria}' (repr: {repr(valor_categoria)})")

print(f"\nTotal participaciones: {total_participaciones}")
print("\nParticipaciones por categoría:")
for cat, count in sorted(participaciones_detalle.items()):
    print(f"  {cat}: {count}")

