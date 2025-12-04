# 📋 Guía de Migraciones de Campos - DELIA

## 🎯 Propósito

Esta guía documenta cómo realizar migraciones de campos en el sistema DELIA cuando necesitamos:
- Agregar nuevos campos
- Modificar campos existentes
- Eliminar campos obsoletos
- Cambiar tipos de datos
- Reestructurar datos anidados

## 📊 Arquitectura del Sistema

El sistema DELIA tiene tres fuentes de datos principales que deben mantenerse sincronizadas:

1. **Supabase (Base de Datos PostgreSQL)**
   - Tabla principal: `obras`
   - Tabla de cambios pendientes: `cambios_pendientes`
   - Tabla de validaciones: `validaciones`

2. **Google Sheets**
   - Hoja principal con todas las obras
   - Sincronización bidireccional con Supabase

3. **Frontend (index.html)**
   - Visualización y edición de datos
   - Validación de permisos (editor/admin)
   - Guardado de cambios pendientes

## 🔄 Proceso de Migración

### Paso 1: Planificar la Migración

Antes de hacer cambios, documenta:

```markdown
## Migración: [Nombre descriptivo]

**Fecha:** YYYY-MM-DD
**Motivo:** [Razón del cambio]
**Campos afectados:**
- Campo: [nombre] | Tipo actual: [tipo] | Tipo nuevo: [tipo]
- Campo: [nombre] | Acción: [agregar/eliminar/modificar]

**Impacto:**
- Frontend: [Sí/No] - [Descripción]
- Backend: [Sí/No] - [Descripción]
- Google Sheets: [Sí/No] - [Descripción]
```

### Paso 2: Actualizar el Schema de Supabase

#### 2.1. Agregar Nuevo Campo

```sql
-- Ejemplo: Agregar campo "subtitulo"
ALTER TABLE obras 
ADD COLUMN IF NOT EXISTS subtitulo TEXT;

-- Agregar índice si es necesario para búsquedas
CREATE INDEX IF NOT EXISTS idx_obras_subtitulo 
ON obras USING gin(to_tsvector('spanish', subtitulo));

-- Actualizar comentario del campo
COMMENT ON COLUMN obras.subtitulo IS 'Subtítulo de la obra';
```

#### 2.2. Modificar Campo Existente

```sql
-- Ejemplo: Cambiar tipo de texto a varchar con límite
ALTER TABLE obras 
ALTER COLUMN titulo TYPE VARCHAR(500);

-- Ejemplo: Cambiar nombre de columna
ALTER TABLE obras 
RENAME COLUMN titulo_antiguo TO titulo_nuevo;
```

#### 2.3. Eliminar Campo

```sql
-- ⚠️ ADVERTENCIA: Solo eliminar si estás seguro
-- Primero verifica que no haya datos importantes

-- Ver cuántos registros tienen datos en este campo
SELECT COUNT(*) FROM obras WHERE campo_a_eliminar IS NOT NULL;

-- Si estás seguro, eliminar
ALTER TABLE obras DROP COLUMN IF EXISTS campo_obsoleto;
```

#### 2.4. Actualizar RLS (Row Level Security)

Si el nuevo campo requiere políticas de seguridad específicas:

```sql
-- Ejemplo: Permitir que editores modifiquen el nuevo campo
-- (Las políticas existentes ya cubren UPDATE para editores/admin)
-- Solo necesitas actualizar si hay restricciones especiales
```

### Paso 3: Actualizar el Frontend (index.html)

#### 3.1. Agregar Campo al Modal

Busca la función `mostrarDetalleObra()` y agrega el campo en la sección correspondiente:

```javascript
// Ejemplo: Agregar campo "subtitulo" en Información Básica
html += renderField(
    'Subtítulo', 
    obtenerValorCampo(obra, 'subtitulo'), 
    '📝', 
    'subtitulo'  // ← Este parámetro habilita la edición
);
```

#### 3.2. Actualizar Función de Obtención de Valores

La función `obtenerValorCampo()` ya maneja campos anidados automáticamente. Solo necesitas asegurarte de usar el nombre correcto del campo.

#### 3.3. Manejar Tipos Especiales

Si el campo es booleano, actualiza `editarCampoObra()`:

```javascript
// En la función editarCampoObra, agregar manejo para el nuevo campo booleano
if (campo === 'nuevo_campo_booleano') {
    const esVerdadero = valorAnterior === true || valorAnterior === 'true' || valorAnterior === 'Sí';
    promptText = `Editar ${campo}:\n\nValor actual: ${esVerdadero ? 'Sí' : 'No'}\n\nNuevo valor (Sí/No):`;
    defaultValue = esVerdadero ? 'Sí' : 'No';
    // ... conversión del valor
}
```

### Paso 4: Actualizar Google Sheets

#### 4.1. Agregar Columna Nueva

1. Abre Google Sheets
2. Agrega la nueva columna en la posición adecuada
3. Actualiza el script de sincronización (`sheets-github-sync.gs`) si es necesario

#### 4.2. Actualizar Script de Sincronización

En `sheets-github-sync.gs`, actualiza el mapeo de columnas:

```javascript
// Ejemplo: Agregar nuevo campo al mapeo
const COLUMN_MAPPING = {
  // ... campos existentes
  'Subtítulo': 'subtitulo',  // Nombre en Sheets: Nombre en DB
};
```

### Paso 5: Actualizar Scripts de Python

#### 5.1. Actualizar Schema en `scripts/schema.py`

```python
# En scripts/schema.py, actualizar la definición de campos
OBRA_FIELDS = {
    # ... campos existentes
    'subtitulo': {
        'type': 'text',
        'required': False,
        'description': 'Subtítulo de la obra',
        'editable': True
    }
}
```

#### 5.2. Actualizar Validaciones

En `scripts/validate.py`, agregar validaciones específicas si es necesario:

```python
def validate_subtitulo(value):
    """Valida que el subtítulo no exceda 500 caracteres"""
    if value and len(value) > 500:
        raise ValueError("El subtítulo no puede exceder 500 caracteres")
    return value
```

### Paso 6: Migrar Datos Existentes

Si necesitas migrar datos existentes:

#### 6.1. Script de Migración SQL

```sql
-- Ejemplo: Migrar datos de un campo antiguo a uno nuevo
UPDATE obras 
SET subtitulo = titulo_alternativo 
WHERE subtitulo IS NULL AND titulo_alternativo IS NOT NULL;

-- Verificar resultados
SELECT COUNT(*) FROM obras WHERE subtitulo IS NOT NULL;
```

#### 6.2. Script de Migración Python

```python
# scripts/migrate_data.py
import asyncio
from scripts.supabase_client import get_supabase_client

async def migrate_subtitulo():
    """Migra datos de titulo_alternativo a subtitulo"""
    supabase = get_supabase_client()
    
    # Obtener obras que necesitan migración
    obras = supabase.table('obras').select('id, titulo_alternativo').is_('subtitulo', 'null').execute()
    
    for obra in obras.data:
        if obra.get('titulo_alternativo'):
            supabase.table('obras').update({
                'subtitulo': obra['titulo_alternativo']
            }).eq('id', obra['id']).execute()
            print(f"Migrado obra {obra['id']}")

if __name__ == '__main__':
    asyncio.run(migrate_subtitulo())
```

### Paso 7: Actualizar Documentación

1. Actualizar `CAMPOS_COMPLETOS.md` con el nuevo campo
2. Actualizar esta guía si el proceso cambió
3. Documentar cualquier breaking change

### Paso 8: Probar la Migración

#### Checklist de Pruebas

- [ ] El campo aparece en el modal del frontend
- [ ] El campo es editable (si aplica) con permisos de editor/admin
- [ ] Los cambios se guardan correctamente en Supabase
- [ ] Los cambios aparecen en Google Sheets (si aplica)
- [ ] Las búsquedas funcionan con el nuevo campo (si tiene índice)
- [ ] Los scripts de Python pueden leer/escribir el nuevo campo
- [ ] No hay errores en la consola del navegador
- [ ] Los permisos RLS funcionan correctamente

## 📝 Ejemplos de Migraciones Comunes

### Ejemplo 1: Agregar Campo de Texto Simple

**Campo:** `notas_publicacion` (TEXT)

```sql
-- SQL
ALTER TABLE obras ADD COLUMN IF NOT EXISTS notas_publicacion TEXT;
```

```javascript
// Frontend - en mostrarDetalleObra()
html += renderField(
    'Notas de Publicación', 
    obtenerValorCampo(obra, 'notas_publicacion'), 
    '📄', 
    'notas_publicacion'
);
```

### Ejemplo 2: Agregar Campo Anidado (Autor)

**Campo:** `autor.nacionalidad` (TEXT)

```sql
-- Los campos anidados se almacenan como JSONB en Supabase
-- O en una tabla separada si es necesario normalizar
-- Para este ejemplo, asumimos que autor es JSONB
ALTER TABLE obras 
ALTER COLUMN autor TYPE JSONB USING autor::jsonb;

-- Luego actualizar con estructura: {"nombre": "...", "nacionalidad": "..."}
```

```javascript
// Frontend - en mostrarDetalleObra()
html += renderField(
    'Nacionalidad del Autor', 
    obtenerValorCampo(obra, 'autor.nacionalidad'), 
    '🌍', 
    'autor.nacionalidad'  // ← Notación con punto para campos anidados
);
```

### Ejemplo 3: Cambiar Tipo de Campo

**Campo:** `fecha_creacion` de TEXT a DATE

```sql
-- Paso 1: Crear columna temporal
ALTER TABLE obras ADD COLUMN fecha_creacion_new DATE;

-- Paso 2: Migrar datos (ajustar formato según tus datos)
UPDATE obras 
SET fecha_creacion_new = TO_DATE(fecha_creacion, 'YYYY-MM-DD')
WHERE fecha_creacion IS NOT NULL;

-- Paso 3: Eliminar columna antigua
ALTER TABLE obras DROP COLUMN fecha_creacion;

-- Paso 4: Renombrar nueva columna
ALTER TABLE obras RENAME COLUMN fecha_creacion_new TO fecha_creacion;
```

```javascript
// Frontend - puede requerir cambios en el formato de visualización
// La función obtenerValorCampo() seguirá funcionando igual
```

## ⚠️ Advertencias Importantes

1. **Siempre haz backup antes de migraciones**
   ```sql
   -- Crear backup de la tabla
   CREATE TABLE obras_backup_YYYYMMDD AS SELECT * FROM obras;
   ```

2. **Prueba en desarrollo primero**
   - Nunca ejecutes migraciones directamente en producción
   - Usa un entorno de staging

3. **Mantén sincronización**
   - Asegúrate de que Supabase, Google Sheets y el frontend estén sincronizados
   - Los scripts de Python ayudan a mantener esta sincronización

4. **Documenta todo**
   - Cada migración debe estar documentada
   - Incluye el motivo, los cambios y los resultados

5. **Considera el impacto en usuarios**
   - Si eliminas un campo, los usuarios pueden perder datos
   - Si cambias tipos, puede haber problemas de compatibilidad

## 🔧 Herramientas Útiles

### Scripts de Python

- `scripts/sync_to_supabase.py` - Sincronizar datos locales → Supabase
- `scripts/sync_to_sheets.py` - Sincronizar datos locales → Google Sheets
- `scripts/validate_data.py` - Validar datos antes de sincronizar
- `scripts/migrate_data.py` - Ejecutar migraciones de datos

### Scripts SQL

- `supabase_schema.sql` - Schema completo de la base de datos
- `supabase_cambios_pendientes.sql` - Estructura de cambios pendientes

## 📚 Referencias

- [Documentación de Supabase ALTER TABLE](https://supabase.com/docs/guides/database/tables)
- [CAMPOS_COMPLETOS.md](./CAMPOS_COMPLETOS.md) - Lista completa de campos
- [GUIA_SUPABASE_PASO_A_PASO.md](./GUIA_SUPABASE_PASO_A_PASO.md) - Guía de Supabase

## 🆘 Troubleshooting

### Problema: Campo no aparece en el frontend

**Solución:**
1. Verifica que el campo existe en Supabase
2. Verifica que el campo está en `mostrarDetalleObra()`
3. Verifica que usas `obtenerValorCampo()` correctamente
4. Limpia caché del navegador

### Problema: No puedo editar el campo

**Solución:**
1. Verifica que tienes permisos de editor/admin
2. Verifica que activaste el modo edición
3. Verifica que pasaste el parámetro `campoNombre` a `renderField()`
4. Verifica la consola del navegador para errores

### Problema: Cambios no se guardan

**Solución:**
1. Verifica que estás autenticado
2. Verifica la tabla `cambios_pendientes` en Supabase
3. Verifica los permisos RLS
4. Verifica la consola del navegador para errores

---

**Última actualización:** 2025-01-XX
**Mantenido por:** Equipo DELIA

