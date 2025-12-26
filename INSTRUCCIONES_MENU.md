# Sistema de Menú Modular

Se ha implementado un sistema de menú modular que permite mantener un solo archivo HTML para el menú de navegación, evitando tener que modificar todos los archivos HTML individualmente.

## Archivos Creados

1. **`menu.html`** - Contiene la estructura completa del menú de navegación
2. **`load-menu.js`** - Script JavaScript que carga el menú dinámicamente y ajusta las rutas automáticamente

## Cómo Usar

### Para archivos HTML nuevos o existentes:

1. **Reemplazar el header del menú** con un contenedor vacío:
   ```html
   <div id="menu-container"></div>
   ```

2. **Agregar el script** antes del cierre de `</body>`:
   ```html
   <script src="../../load-menu.js"></script>
   ```
   
   **Nota:** Ajusta la ruta según la profundidad del archivo:
   - Si está en la raíz: `./load-menu.js`
   - Si está en `Informes/`: `../load-menu.js`
   - Si está en `Informes/Modalidad de ejemplo/`: `../../load-menu.js`
   - Y así sucesivamente...

3. **Eliminar el código JavaScript del menú** que ya no es necesario (el script `load-menu.js` lo maneja automáticamente)

## Ejemplo de Modificación

### Antes:
```html
<body>
    <header class="fixed-header">
        <div class="header-content">
            <!-- Todo el código del menú aquí -->
        </div>
    </header>
    <!-- Resto del contenido -->
    <script>
        // Código JavaScript del menú
    </script>
</body>
```

### Después:
```html
<body>
    <div id="menu-container"></div>
    <!-- Resto del contenido -->
    <script src="../../load-menu.js"></script>
</body>
```

## Modificar el Menú

Para modificar el menú, solo necesitas editar el archivo **`menu.html`** en la raíz del proyecto. Los cambios se aplicarán automáticamente a todos los archivos HTML que usen el sistema.

## Características

- ✅ Ajuste automático de rutas según la ubicación del archivo
- ✅ Detección automática de la página activa
- ✅ Soporte para menús desplegables anidados
- ✅ Compatible con dispositivos móviles
- ✅ Funciona con archivos en cualquier nivel de profundidad

## Archivo de Ejemplo Modificado

El archivo `Informes/Modalidad de ejemplo/informe_valida_ejemplo3.html` ha sido modificado como ejemplo. Puedes usarlo como referencia para modificar los demás archivos HTML.

