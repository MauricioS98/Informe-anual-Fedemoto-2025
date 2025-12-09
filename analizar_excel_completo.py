import pandas as pd
import unicodedata
import re
import json
from collections import defaultdict

def normalizar_liga(nombre):
    """
    Normaliza el nombre de la liga: quita tildes, convierte a mayúsculas,
    y limpia espacios extra.
    """
    if pd.isna(nombre) or nombre == '':
        return None
    
    # Convertir a string y limpiar
    nombre = str(nombre).strip()
    
    # Quitar tildes
    nombre = unicodedata.normalize('NFD', nombre)
    nombre = ''.join(c for c in nombre if unicodedata.category(c) != 'Mn')
    
    # Convertir a mayúsculas para unificar
    nombre = nombre.upper()
    
    return nombre

def extraer_datos_excel(excel_path):
    """
    Extrae todos los datos del Excel, procesando todas las hojas.
    """
    excel_file = pd.ExcelFile(excel_path)
    
    resultados = {
        'modalidades': {},
        'total_pilotos_unicos': set(),
        'total_participaciones': 0,  # Total de participaciones (incluyendo repetidos)
        'pilotos_por_categoria': defaultdict(set),
        'deportistas_por_liga_total': defaultdict(set),
        'deportistas_por_liga_categoria': defaultdict(lambda: defaultdict(set))
    }
    
    print(f"Procesando {len(excel_file.sheet_names)} modalidades...")
    
    for sheet_name in excel_file.sheet_names:
        print(f"\nProcesando modalidad: {sheet_name}")
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        
        modalidad_data = {
            'pilotos_unicos': set(),
            'total_participaciones': 0,  # Participaciones en esta modalidad (incluyendo repetidos)
            'pilotos_por_categoria': defaultdict(set),
            'deportistas_por_liga': defaultdict(set),
            'deportistas_por_liga_categoria': defaultdict(lambda: defaultdict(set))
        }
        
        # Identificar pares de columnas (número + departamento)
        categorias = []
        i = 0
        while i < len(df.columns):
            col_num = df.columns[i]
            col_dep = df.columns[i + 1] if i + 1 < len(df.columns) else None
            
            # Si la columna de número tiene un nombre válido (no "Unnamed")
            if not str(col_num).startswith('Unnamed'):
                categoria = str(col_num)
                categorias.append((categoria, i, i + 1 if col_dep else None))
                i += 2
            else:
                i += 1
        
        # Procesar cada categoría
        for categoria, idx_num, idx_dep in categorias:
            if idx_dep is None:
                continue
                
            col_num = df.columns[idx_num]
            col_dep = df.columns[idx_dep]
            
            print(f"  - Categoría: {categoria}")
            
            # Extraer datos de esta categoría
            for idx, row in df.iterrows():
                numero = row[col_num]
                departamento = row[col_dep]
                
                # Validar que ambos valores existan
                if pd.notna(numero) and pd.notna(departamento):
                    numero = int(numero) if isinstance(numero, (int, float)) else numero
                    liga_normalizada = normalizar_liga(departamento)
                    
                    if liga_normalizada:
                        # Agregar a totales
                        resultados['total_pilotos_unicos'].add(numero)
                        resultados['total_participaciones'] += 1  # Contar todas las participaciones
                        resultados['pilotos_por_categoria'][categoria].add(numero)
                        resultados['deportistas_por_liga_total'][liga_normalizada].add(numero)
                        resultados['deportistas_por_liga_categoria'][categoria][liga_normalizada].add(numero)
                        
                        # Agregar a modalidad específica
                        modalidad_data['pilotos_unicos'].add(numero)
                        modalidad_data['total_participaciones'] += 1  # Contar participaciones en esta modalidad
                        modalidad_data['pilotos_por_categoria'][categoria].add(numero)
                        modalidad_data['deportistas_por_liga'][liga_normalizada].add(numero)
                        modalidad_data['deportistas_por_liga_categoria'][categoria][liga_normalizada].add(numero)
        
        resultados['modalidades'][sheet_name] = modalidad_data
    
    return resultados

def generar_informe(resultados, output_file='informe_resultados.txt'):
    """
    Genera un informe detallado con todos los resultados.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("INFORME GENERAL - FEDEMOTO 2025\n")
        f.write("=" * 80 + "\n\n")
        
        # 1. Total de pilotos únicos participantes
        f.write("1. CANTIDAD TOTAL DE PILOTOS ÚNICOS PARTICIPANTES\n")
        f.write("-" * 80 + "\n")
        total_unicos = len(resultados['total_pilotos_unicos'])
        f.write(f"Total: {total_unicos} pilotos únicos\n\n")
        
        # 1.1. Total de participaciones (incluyendo repetidos)
        f.write("1.1. CANTIDAD TOTAL DE PARTICIPACIONES (INCLUYENDO REPETIDOS)\n")
        f.write("-" * 80 + "\n")
        total_participaciones = resultados['total_participaciones']
        f.write(f"Total: {total_participaciones} participaciones\n\n")
        
        # 2. Cantidad de pilotos por cada categoría
        f.write("2. CANTIDAD DE PILOTOS POR CADA CATEGORÍA\n")
        f.write("-" * 80 + "\n")
        for categoria in sorted(resultados['pilotos_por_categoria'].keys()):
            cantidad = len(resultados['pilotos_por_categoria'][categoria])
            f.write(f"{categoria}: {cantidad} pilotos únicos\n")
        f.write("\n")
        
        # 3. Cantidad de deportistas únicos por ligas totales
        f.write("3. CANTIDAD DE DEPORTISTAS ÚNICOS POR LIGAS TOTALES\n")
        f.write("-" * 80 + "\n")
        for liga in sorted(resultados['deportistas_por_liga_total'].keys()):
            cantidad = len(resultados['deportistas_por_liga_total'][liga])
            f.write(f"{liga}: {cantidad} deportistas únicos\n")
        f.write("\n")
        
        # 4. Cantidad de deportistas únicos por ligas por categoría
        f.write("4. CANTIDAD DE DEPORTISTAS ÚNICOS POR LIGAS POR CATEGORÍA\n")
        f.write("-" * 80 + "\n")
        for categoria in sorted(resultados['deportistas_por_liga_categoria'].keys()):
            f.write(f"\n{categoria}:\n")
            for liga in sorted(resultados['deportistas_por_liga_categoria'][categoria].keys()):
                cantidad = len(resultados['deportistas_por_liga_categoria'][categoria][liga])
                f.write(f"  {liga}: {cantidad} deportistas únicos\n")
        f.write("\n")
        
        # Información por modalidad
        f.write("=" * 80 + "\n")
        f.write("DETALLE POR MODALIDAD\n")
        f.write("=" * 80 + "\n\n")
        
        for modalidad, data in resultados['modalidades'].items():
            f.write(f"\nMODALIDAD: {modalidad}\n")
            f.write("-" * 80 + "\n")
            f.write(f"Pilotos únicos en esta modalidad: {len(data['pilotos_unicos'])}\n")
            f.write(f"Total de participaciones en esta modalidad: {data['total_participaciones']}\n\n")
            
            f.write("Pilotos por categoría:\n")
            for cat in sorted(data['pilotos_por_categoria'].keys()):
                cantidad = len(data['pilotos_por_categoria'][cat])
                f.write(f"  {cat}: {cantidad}\n")
            
            f.write("\nDeportistas por liga:\n")
            for liga in sorted(data['deportistas_por_liga'].keys()):
                cantidad = len(data['deportistas_por_liga'][liga])
                f.write(f"  {liga}: {cantidad}\n")
    
    print(f"\nInforme generado en: {output_file}")

def generar_json(resultados, output_file='datos_informe.json'):
    """
    Genera un archivo JSON con los datos estructurados para la página web.
    """
    datos_json = {
        'total_pilotos_unicos': len(resultados['total_pilotos_unicos']),
        'total_participaciones': resultados['total_participaciones'],
        'pilotos_por_categoria': {
            cat: len(pilotos) 
            for cat, pilotos in sorted(resultados['pilotos_por_categoria'].items())
        },
        'deportistas_por_liga_total': {
            liga: len(deportistas) 
            for liga, deportistas in sorted(resultados['deportistas_por_liga_total'].items())
        },
        'deportistas_por_liga_categoria': {
            cat: {
                liga: len(deportistas)
                for liga, deportistas in sorted(ligas.items())
            }
            for cat, ligas in sorted(resultados['deportistas_por_liga_categoria'].items())
        },
        'modalidades': {
            modalidad: {
                'pilotos_unicos': len(data['pilotos_unicos']),
                'total_participaciones': data['total_participaciones'],
                'pilotos_por_categoria': {
                    cat: len(pilotos)
                    for cat, pilotos in sorted(data['pilotos_por_categoria'].items())
                },
                'deportistas_por_liga': {
                    liga: len(deportistas)
                    for liga, deportistas in sorted(data['deportistas_por_liga'].items())
                },
                'deportistas_por_liga_categoria': {
                    cat: {
                        liga: len(deportistas)
                        for liga, deportistas in sorted(ligas.items())
                    }
                    for cat, ligas in sorted(data['deportistas_por_liga_categoria'].items())
                }
            }
            for modalidad, data in resultados['modalidades'].items()
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(datos_json, f, ensure_ascii=False, indent=2)
    
    print(f"JSON generado en: {output_file}")

# Ejecutar análisis
if __name__ == "__main__":
    excel_path = "excel para informe general 2025.xlsx"
    
    print("Iniciando análisis del Excel...")
    resultados = extraer_datos_excel(excel_path)
    
    print("\nGenerando informe...")
    generar_informe(resultados)
    generar_json(resultados)
    
    print("\n¡Análisis completado!")

