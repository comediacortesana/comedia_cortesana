# Sistema de Referencias a Páginas PDF

## Descripción

Este sistema añade referencias precisas a las páginas del PDF original donde se encontraron las informaciones extraídas. Esto permite a los usuarios:

1. **Verificar la información**: Abrir el PDF original y contrastar los datos extraídos
2. **Trazabilidad completa**: Saber exactamente dónde se encontró cada dato
3. **Contexto adicional**: Ver el texto original alrededor de la información extraída

## Componentes

### 1. Script de Mejora de Referencias

**Archivo**: `mejorar_referencias_paginas.py`

Mejora archivos de extracción añadiendo referencias completas a páginas PDF.

**Uso**:
```bash
python data/fuentesix/mejorar_referencias_paginas.py \
    "data/fuentesix/extraccion_part_001_con_metadata.json" \
    "data/raw/extracted_text/FUENTES IX 1_part_001_ALL_PAGES_texto_extraido.txt"
```

**Funcionalidades**:
- Extrae números de página del texto extraído
- Mapea páginas del texto a páginas del PDF original
- Busca referencias adicionales en el texto (como "(Fuentes V, pág. 187)")
- Crea referencias completas con URLs y rutas de imágenes

### 2. Actualización del Sistema de Análisis

**Archivo**: `actualizar_sistema_analisis_con_paginas.py`

Actualiza análisis de IA para incluir referencias a páginas PDF.

**Uso**:
```bash
python data/fuentesix/actualizar_sistema_analisis_con_paginas.py \
    "data/fuentesix/analisis_part_001.json" \
    "data/fuentesix/extraccion_part_001_con_metadata.json"
```

### 3. Componente de Template

**Archivo**: `templates/obras/includes/referencia_pagina_pdf.html`

Componente reutilizable para mostrar referencias a páginas PDF en la interfaz.

**Uso en templates**:
```django
{% raw %}{% include 'obras/includes/referencia_pagina_pdf.html' with referencia=referencia_pagina_pdf %}{% endraw %}
```

## Estructura de Datos

### Referencia a Página PDF

```json
{
  "pagina_pdf": 134,
  "archivo_fuente": "FUENTES IX 1_part_001_ALL_PAGES_texto_extraido.txt",
  "tipo_referencia": "directa",
  "ruta_imagen": "data/raw/images/FUENTES IX 1_part_001_ALL_PAGES/page_134.png",
  "url_pagina": "/obras/pagina-pdf/134/",
  "url_imagen": "/media/pdf_pages/page_134.png",
  "contexto": "Texto original donde se encontró la información",
  "texto_referencia": "Página 134 del PDF original",
  "enlace_verificacion": "Ver página 134 en PDF original"
}
```

### Tipos de Referencia

- **directa**: La página está explícitamente indicada en los datos
- **inferida**: La página se dedujo del contexto del texto
- **referencia_fuente**: Referencia encontrada en el texto (ej: "(Fuentes V, pág. 187)")

## Mapeo de Páginas

El sistema mapea páginas del texto extraído a páginas del PDF original:

- `part_001`: Páginas 1-25 del PDF (offset: 0)
- `part_002`: Páginas 26-50 del PDF (offset: 25)
- `part_003`: Páginas 51-75 del PDF (offset: 50)
- `part_004`: Páginas 76-100 del PDF (offset: 75)
- `part_005`: Páginas 101-125 del PDF (offset: 100)
- `part_006`: Páginas 126-150 del PDF (offset: 125)
- `part_007`: Páginas 151-175 del PDF (offset: 150)
- `part_008`: Páginas 176-200 del PDF (offset: 175)
- `part_009`: Páginas 201-225 del PDF (offset: 200)
- `part_010`: Páginas 226-250 del PDF (offset: 225)
- `part_011`: Páginas 251-252 del PDF (offset: 250)

## Integración con el Sistema Existente

El sistema se integra con:

1. **Modelo `PaginaPDF`**: Ya existente en `apps/obras/models.py`
2. **Vistas de páginas PDF**: `/obras/pagina-pdf/<numero>/`
3. **Modal de páginas PDF**: Función `openPdfPageModal()` en templates

## Flujo de Trabajo

1. **Extracción inicial**: Se extraen datos del texto del PDF
2. **Mejora de referencias**: Se ejecuta `mejorar_referencias_paginas.py` para añadir referencias
3. **Análisis con IA**: Se ejecuta análisis de IA
4. **Actualización de análisis**: Se ejecuta `actualizar_sistema_analisis_con_paginas.py`
5. **Visualización**: Las referencias se muestran en la interfaz usando el componente de template

## Beneficios

1. **Trazabilidad**: Cada dato puede referenciar su origen exacto
2. **Verificación**: Los usuarios pueden contrastar información con el PDF original
3. **Transparencia**: Se muestra claramente de dónde proviene cada información
4. **Contexto**: Se proporciona contexto adicional para entender mejor los datos

## Próximos Pasos

- [ ] Integrar referencias en la visualización de representaciones
- [ ] Añadir referencias a lugares y autores extraídos
- [ ] Crear vista de resumen de todas las referencias de una obra
- [ ] Añadir estadísticas de páginas más referenciadas
- [ ] Implementar búsqueda por página PDF






