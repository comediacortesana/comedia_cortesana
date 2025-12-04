# 🔄 Guía de Recuperación Completa de Supabase

**Situación**: Se ha borrado todo en Supabase (solo queda la API key)  
**Objetivo**: Recuperar schema completo + todos los datos  
**Tiempo estimado**: 10-15 minutos

---

## 📋 Resumen del Proceso

1. ✅ **Recrear schema** (tablas, índices, RLS, triggers) → 5 minutos
2. ✅ **Restaurar datos** (obras desde backup) → 5 minutos
3. ✅ **Verificar** que todo funciona → 2 minutos

---

## 🔧 PASO 1: Recrear el Schema en Supabase

### 1.1 Acceder a Supabase SQL Editor

1. Ve a tu proyecto en [Supabase Dashboard](https://supabase.com/dashboard)
2. En el menú lateral, haz clic en **"SQL Editor"**
3. Haz clic en **"+ New query"**

### 1.2 Ejecutar el Script de Recuperación

1. Abre el archivo: `RECUPERACION_SUPABASE_COMPLETA.sql`
2. **Copia TODO el contenido** del archivo
3. **Pega** en el SQL Editor de Supabase
4. Haz clic en el botón **"Run"** (esquina inferior derecha)

⏱️ **El script tardará unos 10-30 segundos en ejecutarse**

### 1.3 Verificar que el Schema se Creó Correctamente

En el SQL Editor, ejecuta esta consulta de verificación:

```sql
-- Verificar tablas creadas
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;
```

**Deberías ver estas tablas:**
- ✅ `comentarios`
- ✅ `historial_validaciones`
- ✅ `logs_errores`
- ✅ `obras`
- ✅ `perfiles_usuarios`
- ✅ `validaciones`

**Y estas vistas:**
- ✅ `comentarios_pendientes`
- ✅ `logs_errores_pendientes`

### 1.4 Verificar Columnas de la Tabla `obras`

```sql
-- Verificar columnas de obras
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'obras' 
ORDER BY ordinal_position;
```

**Deberías ver aprox. 30+ columnas**, incluyendo:
- `id`, `titulo`, `titulo_original`, `titulo_alternativo`
- `autor` (JSONB), `autor_nombre`
- `genero`, `subgenero`, `tema`
- `actos`, `versos`
- `musica_conservada`, `compositor`
- `representaciones` (JSONB)
- Y muchas más...

---

## 📦 PASO 2: Restaurar los Datos

### 2.1 Preparar el Entorno

Abre una terminal y navega al directorio del proyecto:

```bash
cd /Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO/comedia_cortesana
```

### 2.2 Verificar los Backups Disponibles

```bash
ls -lh datos_obras*.json
```

**Backups disponibles:**
- `datos_obras_backup_20251114_132718.json` (2.3MB) - **Recomendado** ✅
- `datos_obras_backup.json` (2.4MB)
- `datos_obras.json` (2.3MB)

### 2.3 Hacer un Dry-Run (Simulación)

Primero, verifica que el script funciona sin hacer cambios reales:

```bash
python scripts/sync_to_supabase.py \
  --file datos_obras_backup_20251114_132718.json \
  --dry-run
```

**Esto mostrará:**
- ✅ Número de obras válidas
- ❌ Número de obras con errores (si las hay)
- 🔍 Resumen de lo que se sincronizaría

### 2.4 Restaurar los Datos (Sincronización Real)

Si el dry-run se ve bien, ejecuta la sincronización real:

```bash
python scripts/sync_to_supabase.py \
  --file datos_obras_backup_20251114_132718.json \
  --batch-size 100
```

**Progreso esperado:**
```
📂 Cargando datos desde datos_obras_backup_20251114_132718.json...
📊 Total de obras cargadas: 1755
🔍 Validando datos...
✅ Válidas: 1755
❌ Inválidas: 0
📤 Sincronizando 1755 obras a Supabase...
✅ Sincronización completada: 1755 obras procesadas
```

⏱️ **Tiempo estimado: 2-5 minutos** (depende de tu conexión)

---

## ✅ PASO 3: Verificar la Recuperación

### 3.1 Verificar Número de Obras en Supabase

En el SQL Editor de Supabase:

```sql
-- Contar obras
SELECT COUNT(*) as total_obras FROM obras;

-- Ver una muestra de obras
SELECT id, titulo, autor_nombre, fuente, fecha_creacion 
FROM obras 
LIMIT 10;
```

**Deberías ver ~1755 obras**

### 3.2 Verificar Campos JSONB (autor y representaciones)

```sql
-- Ver obras con autor como JSONB
SELECT 
    id, 
    titulo, 
    autor->>'nombre' as autor_nombre,
    autor->>'nombre_completo' as autor_completo,
    autor->>'epoca' as epoca
FROM obras 
WHERE autor IS NOT NULL
LIMIT 10;
```

### 3.3 Verificar RLS (Row Level Security)

```sql
-- Verificar que RLS está habilitado
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public';
```

**Todas las tablas deberían tener `rowsecurity = true`**

### 3.4 Verificar en tu Aplicación Web

1. Abre tu aplicación web (index.html)
2. Verifica que las obras se cargan correctamente
3. Intenta hacer una búsqueda
4. Verifica que los filtros funcionan

---

## 🎯 Checklist de Recuperación Completa

Marca cuando completes cada paso:

### Schema
- [ ] Tablas creadas (obras, comentarios, validaciones, etc.)
- [ ] Columnas adicionales agregadas a `obras`
- [ ] Índices creados
- [ ] Triggers configurados
- [ ] RLS habilitado
- [ ] Políticas RLS creadas
- [ ] Vistas creadas

### Datos
- [ ] Obras restauradas (~1755)
- [ ] Datos JSONB correctos (autor, representaciones)
- [ ] Sin errores de validación

### Funcionalidad
- [ ] Aplicación web carga obras
- [ ] Búsqueda funciona
- [ ] Filtros funcionan
- [ ] Usuarios pueden registrarse
- [ ] Comentarios funcionan (si hay usuarios)

---

## 🆘 Solución de Problemas

### Error: "permission denied for schema auth"

**Solución**: Estás usando un usuario que no tiene permisos suficientes. 
- Ve a Settings > API en Supabase
- Usa el **service_role key** (con cuidado, tiene permisos completos)

### Error: "relation obras already exists"

**Solución**: El schema ya existe parcialmente.
- Ejecuta el script de todas formas, tiene `IF NOT EXISTS` en todos los CREATE
- O elimina las tablas existentes antes de ejecutar el script

### Error durante sync_to_supabase.py: "Invalid API key"

**Solución**: 
1. Verifica que tienes las credenciales correctas en `.env`
2. Verifica que usas la URL correcta del proyecto

### Algunas obras no se sincronizan

**Solución**:
1. Revisa los errores que muestra el script
2. Usa otro backup si es necesario:
   ```bash
   python scripts/sync_to_supabase.py --file datos_obras.json
   ```

---

## 📊 Archivos de Backup Disponibles

Por si necesitas más opciones:

| Archivo | Tamaño | Fecha | Uso |
|---------|--------|-------|-----|
| `datos_obras_backup_20251114_132718.json` | 2.3MB | Nov 14, 13:27 | ✅ **Recomendado** |
| `datos_obras_backup.json` | 2.4MB | Nov 14, 12:13 | Alternativa |
| `datos_obras.json` | 2.3MB | Nov 14, 13:27 | Alternativa |
| `CATCOM_backup/all_works.json` | - | - | Backup original CATCOM |

---

## 🔐 Configurar el Primer Usuario Admin

Después de restaurar, necesitarás crear un usuario admin:

### Opción 1: Crear Usuario Admin desde Supabase Dashboard

1. Ve a **Authentication > Users** en Supabase
2. Crea un nuevo usuario (o usa uno existente)
3. Copia el UUID del usuario
4. En SQL Editor, ejecuta:

```sql
-- Reemplaza 'UUID-DEL-USUARIO' con el UUID real
UPDATE perfiles_usuarios 
SET rol = 'admin' 
WHERE id = 'UUID-DEL-USUARIO';
```

### Opción 2: Usar el Script SQL

Usa el archivo `supabase_make_admin.sql` que ya tienes:

```sql
-- Ver el contenido del archivo y adaptarlo con tu usuario
```

---

## 📝 Notas Importantes

1. **Backups**: Los backups son del 14 de noviembre (hace unas semanas)
   - Si tenías datos más recientes, se habrán perdido
   - Considera hacer backups periódicos en el futuro

2. **Usuarios**: Los usuarios de auth.users se mantienen en Supabase
   - Si se borraron, necesitarás recrearlos
   - Los perfiles_usuarios se recrean con el trigger automáticamente

3. **Comentarios**: Los comentarios antiguos se perdieron
   - Solo las obras se pueden restaurar desde el backup
   - Los comentarios se crean cuando los usuarios interactúan

4. **Validaciones**: El historial de validaciones se perdió
   - Es información de auditoría que no se puede recuperar

---

## 🎉 ¡Listo!

Una vez completados todos los pasos, tu sistema Supabase estará completamente recuperado y funcionando.

**¿Necesitas ayuda?** Revisa la sección de solución de problemas o contacta al equipo.

---

**Fecha de creación**: Diciembre 4, 2025  
**Autor**: Sistema de recuperación automática

