from PIL import Image
import numpy as np
from collections import Counter

# Abrir la imagen
img = Image.open('fedemoto-logo.png')

# Convertir a RGB si tiene transparencia
if img.mode != 'RGB':
    img = img.convert('RGB')

# Convertir a array numpy
pixels = np.array(img)

# Aplanar el array para obtener todos los píxeles
pixels_flat = pixels.reshape(-1, 3)

# Contar colores únicos
colors = [tuple(p) for p in pixels_flat]
color_counts = Counter(colors)

print("=" * 60)
print("COLORES PRINCIPALES DEL LOGO FEDEMOTO")
print("=" * 60)
print("\nTop 15 colores más frecuentes (RGB):\n")

for i, (color, count) in enumerate(color_counts.most_common(15), 1):
    r, g, b = color
    hex_color = f"#{r:02x}{g:02x}{b:02x}"
    print(f"{i:2d}. RGB({r:3d}, {g:3d}, {b:3d}) - {hex_color.upper()} - {count:6d} píxeles")

# Identificar colores principales basándose en los más frecuentes
print("\n" + "=" * 60)
print("COLORES PRINCIPALES IDENTIFICADOS")
print("=" * 60)

# Filtrar colores que no sean blanco, negro o grises
def is_colorful(r, g, b):
    # Excluir blancos, negros y grises
    if r == g == b:
        return False
    # Excluir casi negros
    if r < 30 and g < 30 and b < 30:
        return False
    # Excluir casi blancos
    if r > 240 and g > 240 and b > 240:
        return False
    return True

colorful_colors = [(color, count) for color, count in color_counts.most_common(30) 
                   if is_colorful(*color)]

print("\n🟡 AMARILLO (Yellow) - Colores amarillos/dorados:")
yellow_colors = [(c, count) for c, count in colorful_colors if c[0] > c[1] and c[0] > c[2] and c[0] > 200]
for color, count in yellow_colors[:5]:
    r, g, b = color
    hex_color = f"#{r:02x}{g:02x}{b:02x}"
    print(f"   RGB({r:3d}, {g:3d}, {b:3d}) - {hex_color.upper()} - {count:6d} píxeles")

print("\n🔵 AZUL (Blue) - Colores azules:")
blue_colors = [(c, count) for c, count in colorful_colors if c[2] > c[0] and c[2] > c[1] and c[2] > 100]
for color, count in blue_colors[:5]:
    r, g, b = color
    hex_color = f"#{r:02x}{g:02x}{b:02x}"
    print(f"   RGB({r:3d}, {g:3d}, {b:3d}) - {hex_color.upper()} - {count:6d} píxeles")

print("\n🔴 ROJO (Red) - Colores rojos:")
red_colors = [(c, count) for c, count in colorful_colors if c[0] > 150 and c[1] < 100 and c[2] < 100]
for color, count in red_colors[:5]:
    r, g, b = color
    hex_color = f"#{r:02x}{g:02x}{b:02x}"
    print(f"   RGB({r:3d}, {g:3d}, {b:3d}) - {hex_color.upper()} - {count:6d} píxeles")

print("\n⚫ NEGRO (Black):")
black_colors = [(c, count) for c, count in color_counts.most_common(10) if c[0] < 10 and c[1] < 10 and c[2] < 10]
for color, count in black_colors[:3]:
    r, g, b = color
    hex_color = f"#{r:02x}{g:02x}{b:02x}"
    print(f"   RGB({r:3d}, {g:3d}, {b:3d}) - {hex_color.upper()} - {count:6d} píxeles")

print("\n⚪ BLANCO (White):")
white_colors = [(c, count) for c, count in color_counts.most_common(10) if c[0] > 240 and c[1] > 240 and c[2] > 240]
for color, count in white_colors[:3]:
    r, g, b = color
    hex_color = f"#{r:02x}{g:02x}{b:02x}"
    print(f"   RGB({r:3d}, {g:3d}, {b:3d}) - {hex_color.upper()} - {count:6d} píxeles")

