# Sistema de Validación de Análisis de IA

## Descripción

Sistema completo para que investigadores revisen, validen o rechacen análisis generados por IA antes de integrarlos a la base de datos.

## Flujo de Trabajo

### 1. Generar Síntesis para Validación

```bash
python data/fuentesix/generar_sintesis_validacion.py \
    "data/fuentesix/extraccion_part_001_con_metadata_con_referencias_paginas.json"
```

Esto genera un archivo `*_sintesis_validacion.json` con síntesis legibles en frases.

### 2. Revisar Síntesis en la Interfaz Web

Los investigadores acceden a:
- `/obras/validacion-analisis/` - Lista de archivos de síntesis disponibles
- `/obras/validacion-analisis/<nombre_archivo>/` - Detalle de síntesis para validar

### 3. Validar o Rechazar Items

Cada síntesis muestra:
- **Frases legibles** con la información extraída
- **Referencia a página PDF** para verificar en el documento original
- **Texto original** extraído del PDF
- **Datos JSON** completos (colapsable)
- **Botones de acción**: Validar / Rechazar

### 4. Integración Automática a la DB

Cuando un investigador valida un item:
- Se marca como validado en el archivo JSON
- Se integra automáticamente a la base de datos Django
- Se crean/actualizan registros en las tablas correspondientes

## Estructura de Síntesis

```json
{
  "tipo": "representacion",
  "id_temporal": "temp_...",
  "sintesis": "Texto completo de síntesis",
  "frases": [
    "Frase 1",
    "Frase 2",
    ...
  ],
  "datos_json": { /* datos completos */ },
  "metadata": { /* metadata del registro */ },
  "confianza": "medio",
  "pagina_pdf": 134,
  "texto_original": "...",
  "validacion": {
    "estado": "validado|rechazado",
    "fecha": "2025-01-27T...",
    "usuario": "nombre_usuario",
    "comentario": "..."
  }
}
```

## Características

### Para Investigadores

1. **Síntesis legibles**: Información en frases naturales, no solo JSON
2. **Referencias a PDF**: Enlaces directos a páginas del PDF original
3. **Contexto completo**: Texto original y datos estructurados disponibles
4. **Validación individual o por lotes**: Validar items uno por uno o en grupo
5. **Comentarios**: Añadir comentarios al validar/rechazar

### Integración Automática

Cuando se valida:
- **Representaciones**: Se crean en la tabla `representaciones`
- **Obras**: Se crean en la tabla `obras` (si no existen)
- **Lugares**: Se crean en la tabla `lugares` (si no existen)
- **Relaciones**: Se establecen automáticamente (obra-lugar, etc.)

## Vistas Django

- `validacion_analisis_list`: Lista archivos de síntesis
- `validacion_analisis_detail`: Muestra síntesis detalladas
- `validar_item`: Valida/rechaza un item individual
- `validar_lote`: Valida múltiples items a la vez

## Templates

- `validacion_analisis_list.html`: Lista de archivos
- `validacion_analisis_detail.html`: Vista detallada con síntesis

## Seguridad

- Requiere autenticación (`@login_required`)
- Registra usuario y fecha de validación
- Transacciones atómicas para integración a DB

## Próximos Pasos

- [ ] Añadir filtros por nivel de confianza
- [ ] Búsqueda dentro de síntesis
- [ ] Exportar reportes de validación
- [ ] Historial de cambios de validación
- [ ] Notificaciones cuando se validan items






