# Funcionalidad de Páginas PDF - FUENTES IX 1

## Descripción

Se ha implementado un sistema completo para referenciar y mostrar las páginas del PDF "FUENTES IX 1" (Varey & Shergold) en la base de datos del catálogo de teatro español del Siglo de Oro.

## Características Implementadas

### 1. Base de Datos

#### Nuevos Campos en el Modelo `Obra`:
- `origen_datos`: Indica si los datos provienen de 'web', 'pdf' o 'manual'
- `pagina_pdf`: Número de página del PDF donde aparece la información
- `texto_original_pdf`: Texto original extraído del PDF para esta obra

#### Nuevos Campos en el Modelo `Representacion`:
- `pagina_pdf`: Número de página del PDF donde aparece esta representación
- `texto_original_pdf`: Texto original extraído del PDF para esta representación

#### Nuevo Modelo `PaginaPDF`:
- `numero_pagina`: Número de página en el PDF (1-252)
- `texto_extraido`: Texto extraído de esta página
- `archivo_imagen`: Nombre del archivo de imagen (page_XXX.png)
- `part_file`: Archivo de texto del que proviene (part_001, part_002, etc.)

### 2. Procesamiento de Datos

#### Script `process_pdf_pages.py`:
- Procesa los 11 archivos de texto extraído del PDF
- Extrae el texto de cada página (252 páginas total)
- Copia las imágenes correspondientes a `/media/pdf_pages/`
- Crea registros en la base de datos para cada página

#### Script `associate_obras_with_pages.py`:
- Asocia automáticamente las 376 obras de FUENTESXI con sus páginas correspondientes
- Busca coincidencias de títulos en el texto extraído
- Actualiza los campos `pagina_pdf`, `origen_datos` y `texto_original_pdf`

### 3. Interfaz de Usuario

#### Vistas Nuevas:
- `/obras/pagina-pdf/<numero>/`: Vista completa de una página del PDF
- `/obras/pagina-pdf-modal/<numero>/`: Vista modal para mostrar páginas

#### Templates:
- `pagina_pdf.html`: Template para mostrar página completa
- `pagina_pdf_modal.html`: Template para modal de página

#### Funcionalidades:
- Visualización de imágenes de páginas del PDF
- Texto extraído de cada página
- Información de metadatos (número de página, archivo origen, etc.)
- Enlaces desde la edición de obras a las páginas correspondientes

### 4. Administración

#### Admin de Django:
- Nuevos campos visibles en la administración de obras
- Filtros por origen de datos
- Administración de páginas PDF
- Campos de referencia a páginas en representaciones

## Estructura de Archivos

```
/media/pdf_pages/          # Imágenes de páginas (page_001.png, page_002.png, etc.)
/data/pdf_page_mapping.json # Mapeo de páginas para referencia
/scripts/
  ├── process_pdf_pages.py           # Procesar páginas del PDF
  ├── associate_obras_with_pages.py  # Asociar obras con páginas
  └── test_pdf_pages.py              # Probar funcionalidad
/templates/obras/
  ├── pagina_pdf.html                # Template de página completa
  └── pagina_pdf_modal.html          # Template de modal
```

## Estadísticas Actuales

- **Total de páginas procesadas**: 252
- **Obras asociadas con páginas**: 376
- **Imágenes disponibles**: 252 (100%)
- **Páginas más populares**:
  - Página 4: 92 obras
  - Página 1: 84 obras
  - Página 6: 32 obras

## Uso

### Para Desarrolladores:

1. **Procesar páginas del PDF**:
   ```bash
   python scripts/process_pdf_pages.py
   ```

2. **Asociar obras con páginas**:
   ```bash
   python scripts/associate_obras_with_pages.py
   ```

3. **Probar funcionalidad**:
   ```bash
   python scripts/test_pdf_pages.py
   ```

### Para Usuarios:

1. **Ver una página del PDF**:
   - Ir a la edición de una obra
   - Hacer clic en el enlace "📄 Página X" en la información de la obra
   - Se abrirá la página completa del PDF

2. **Buscar obras por página**:
   - En el admin de Django, filtrar por `pagina_pdf`
   - Ver todas las obras que aparecen en una página específica

## Beneficios

1. **Trazabilidad**: Cada obra puede referenciar exactamente dónde aparece en el PDF original
2. **Verificación**: Los usuarios pueden contrastar la información extraída con el texto original
3. **Investigación**: Facilita la investigación académica al proporcionar acceso directo a las fuentes
4. **Calidad**: Permite verificar y corregir errores en la extracción de datos
5. **Transparencia**: Muestra claramente el origen de cada dato (web, pdf, manual)

## Tecnologías Utilizadas

- **Django**: Framework web
- **Python**: Scripts de procesamiento
- **Bootstrap**: Interfaz de usuario
- **PNG**: Formato de imágenes de páginas
- **JSON**: Mapeo y metadatos

## Próximos Pasos Sugeridos

1. **Búsqueda avanzada**: Implementar búsqueda de texto dentro de las páginas
2. **Anotaciones**: Permitir anotaciones en las páginas del PDF
3. **Comparación**: Herramientas para comparar versiones de obras
4. **Exportación**: Exportar páginas específicas como PDF
5. **API**: Endpoints REST para acceder a las páginas programáticamente
