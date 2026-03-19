# 🏗️ Arquitectura: Supabase como Fuente Principal

## 📋 Resumen

El sistema ahora usa **Supabase como fuente principal de datos** y **JSON como respaldo/fallback**. Esto garantiza que los cambios se persistan inmediatamente sin depender de GitHub.

## 🔄 Flujo de Datos

### Carga de Datos (Al iniciar la aplicación)

```
1. Intenta cargar desde Supabase (fuente principal)
   ↓
2. Si Supabase falla o está vacío → Carga desde JSON (fallback)
   ↓
3. Muestra datos y actualiza UI
```

### Edición y Aprobación

```
1. Editor hace cambio → Se guarda en cambios_pendientes (Supabase)
   ↓
2. Admin aprueba cambio → 
   ✅ Se aplica inmediatamente a tabla obras (Supabase)
   ✅ Se actualiza visualización local
   ✅ Cambio visible para todos los usuarios
   ↓
3. (Opcional) Backup periódico Supabase → JSON
```

## 📊 Estructura de Datos

### Tabla `obras` en Supabase

La tabla `obras` debe contener todos los campos de las obras. Para campos complejos (autor, representaciones), se pueden usar:

- **Opción 1: JSONB** (recomendado para flexibilidad)
  ```sql
  ALTER TABLE obras ADD COLUMN IF NOT EXISTS autor JSONB;
  ALTER TABLE obras ADD COLUMN IF NOT EXISTS representaciones JSONB;
  ```

- **Opción 2: Campos individuales** (más estructurado pero menos flexible)

### Campos Actuales en Supabase

Según `supabase_schema.sql`, la tabla tiene:
- `id` (INTEGER PRIMARY KEY)
- `titulo` (TEXT)
- `titulo_original` (TEXT)
- `tipo_obra` (TEXT)
- `autor_nombre` (TEXT)
- `fuente` (TEXT)
- `fecha_creacion` (TEXT)
- `created_at`, `updated_at`, `synced_from_sheet_at`

### Campos Faltantes

Para que funcione completamente, necesitas agregar todos los campos del JSON. Puedes hacerlo de dos formas:

#### Opción A: Agregar todos los campos como TEXT/JSONB

```sql
-- Ejecutar en Supabase SQL Editor
ALTER TABLE obras ADD COLUMN IF NOT EXISTS titulo_alternativo TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS genero TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS subgenero TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS tema TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS idioma TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS actos INTEGER;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS versos INTEGER;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS musica_conservada BOOLEAN;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS compositor TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS bibliotecas_musica TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS bibliografia_musica TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS mecenas TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS edicion_principe TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS notas_bibliograficas TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS manuscritos_conocidos TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS ediciones_conocidas TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS origen_datos TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS pagina_pdf TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS texto_original_pdf TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS notas TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS observaciones TEXT;

-- Campos complejos como JSONB
ALTER TABLE obras ADD COLUMN IF NOT EXISTS autor JSONB;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS representaciones JSONB;
```

#### Opción B: Usar un campo JSONB para todo (más flexible)

```sql
-- Agregar un campo JSONB para datos adicionales
ALTER TABLE obras ADD COLUMN IF NOT EXISTS datos_adicionales JSONB;
```

## 🔧 Scripts Disponibles

### 1. Sincronizar JSON → Supabase (Inicialización)

```bash
# Sincronizar datos del JSON a Supabase (primera vez)
python scripts/sync_to_supabase.py --file datos_obras.json
```

### 2. Backup Supabase → JSON

```bash
# Hacer backup de Supabase a JSON
python scripts/backup_from_supabase.py --output datos_obras_backup.json

# Dry run primero
python scripts/backup_from_supabase.py --dry-run
```

### 3. Sincronizar con Google Sheets

```bash
# Sincronizar Supabase → Google Sheets
python scripts/sync_to_sheets.py --spreadsheet-id TU_ID
```

## 📝 Proceso de Migración

### Paso 1: Actualizar Schema de Supabase

Ejecuta el SQL para agregar todos los campos necesarios (ver Opción A arriba).

### Paso 2: Sincronizar Datos Existentes

Si ya tienes datos en `datos_obras.json`, sincronízalos a Supabase:

```bash
python scripts/sync_to_supabase.py --file datos_obras.json
```

### Paso 3: Verificar

1. Recarga la aplicación
2. Verifica que los datos se cargan desde Supabase
3. El subtítulo debería mostrar "(Supabase)" en lugar de "(JSON (respaldo))"

### Paso 4: Configurar Backup Automático (Opcional)

Puedes configurar un cron job o GitHub Actions para hacer backup periódico:

```bash
# Ejemplo de cron job (diario a las 2 AM)
0 2 * * * cd /ruta/al/proyecto && python scripts/backup_from_supabase.py
```

## ✅ Ventajas de esta Arquitectura

1. **Persistencia inmediata**: Los cambios se guardan en Supabase al instante
2. **Sin dependencia de GitHub**: No necesitas hacer push para que los cambios se vean
3. **Respaldo automático**: JSON sirve como respaldo si Supabase falla
4. **Escalable**: Supabase puede manejar grandes volúmenes de datos
5. **Colaborativo**: Múltiples usuarios pueden editar simultáneamente

## 🔐 Seguridad

- Los cambios requieren aprobación de admin (sistema de `cambios_pendientes`)
- Row Level Security (RLS) activado en Supabase
- Solo usuarios autenticados pueden crear cambios
- Solo admins pueden aprobar cambios

## 📚 Referencias

- [CAMPO_MIGRACIONES.md](./CAMPO_MIGRACIONES.md) - Guía de migraciones de campos
- [scripts/README.md](./scripts/README.md) - Documentación de scripts
- [GUIA_SUPABASE_PASO_A_PASO.md](./GUIA_SUPABASE_PASO_A_PASO.md) - Guía de Supabase

---

**Última actualización:** 2025-01-XX

