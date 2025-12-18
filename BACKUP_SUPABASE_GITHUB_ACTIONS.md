# 🔄 Automatización de Backup de Supabase con GitHub Actions

## 📋 Resumen

Este sistema automatiza las copias de seguridad de tu base de datos Supabase usando GitHub Actions. El backup se ejecuta automáticamente todos los días y guarda los datos en formato JSON o SQLite.

## 🎯 Características

- ✅ **Backup automático diario** a las 2:00 AM UTC
- ✅ **Ejecución manual** desde GitHub Actions cuando necesites
- ✅ **Múltiples formatos**: JSON (por defecto) o SQLite (.db)
- ✅ **Backup completo**: Incluye todas las tablas importantes:
  - `obras`
  - `comentarios`
  - `validaciones`
  - `historial_validaciones`
  - `perfiles_usuarios`
- ✅ **Guardado en el repositorio**: Los backups se guardan directamente en GitHub como commits
- ✅ **Historial completo**: Puedes ver todos los cambios de los usuarios en el historial de Git
- ✅ **Limpieza automática**: Mantiene solo los últimos 30 backups para no llenar el repositorio
- ✅ **Sin costo adicional**: Usa los minutos gratuitos de GitHub Actions

---

## 🚀 Configuración Inicial

### Paso 1: Configurar Secrets de GitHub

Para que el workflow funcione, necesitas configurar los secrets de GitHub con tus credenciales de Supabase:

1. **Ve a tu repositorio en GitHub**
2. **Click en:** Settings → Secrets and variables → Actions
3. **Click en:** "New repository secret"
4. **Agrega estos dos secrets:**

   | Nombre del Secret | Valor | Dónde encontrarlo |
   |-------------------|-------|-------------------|
   | `SUPABASE_URL` | Tu URL de Supabase | Supabase Dashboard → Settings → API → Project URL |
   | `SUPABASE_KEY` | Tu Service Role Key | Supabase Dashboard → Settings → API → Service Role Key (⚠️ secreto) |

   **⚠️ IMPORTANTE:** Usa el **Service Role Key**, NO el Anon Key. El Service Role Key tiene permisos completos para leer todas las tablas.

### Paso 2: Verificar que el Workflow Está Activo

1. **Ve a la pestaña "Actions"** en tu repositorio
2. Deberías ver el workflow **"Backup Supabase Database"**
3. Puedes ejecutarlo manualmente haciendo click en "Run workflow"

---

## 📅 Programación

El backup se ejecuta automáticamente:
- **Frecuencia:** Diariamente
- **Hora:** 2:00 AM UTC
- **Zonas horarias equivalentes:**
  - 3:00 AM CET (Europa Central)
  - 9:00 PM PST (día anterior, Pacífico)
  - 10:00 PM EST (día anterior, Este)

### Cambiar la Frecuencia

Si quieres cambiar cuándo se ejecuta el backup, edita el archivo `.github/workflows/backup-supabase.yml`:

```yaml
schedule:
  # Ejemplo: Cada 12 horas
  - cron: '0 */12 * * *'
  
  # Ejemplo: Semanalmente (lunes a las 2 AM)
  - cron: '0 2 * * 1'
  
  # Ejemplo: Mensualmente (día 1 a las 2 AM)
  - cron: '0 2 1 * *'
```

**Formato cron:** `minuto hora día mes día-semana`
- `0 2 * * *` = Todos los días a las 2:00 AM
- `0 */6 * * *` = Cada 6 horas
- `0 2 * * 1` = Todos los lunes a las 2:00 AM

---

## 🎮 Ejecución Manual

Puedes ejecutar el backup manualmente en cualquier momento:

1. **Ve a:** Actions → Backup Supabase Database
2. **Click en:** "Run workflow"
3. **Selecciona:**
   - Rama: `main` (o la que uses)
   - Formato: `json` o `db`
4. **Click en:** "Run workflow"

---

## 📥 Acceder a los Backups

Los backups se guardan **directamente en el repositorio** en la carpeta `backups/`:

### Ver backups en GitHub

1. **Ve a tu repositorio** en GitHub
2. **Navega a la carpeta** `backups/`
3. **Verás todos los backups** con nombres como:
   - `backup_supabase_20250115_020000.json`
   - `backup_supabase_20250116_020000.json`

### Ver historial de cambios

Cada backup se guarda como un **commit separado**, así que puedes:

1. **Ve a:** Commits (en la página principal del repositorio)
2. **Busca commits** con el mensaje "🔄 Backup automático de Supabase"
3. **Click en el commit** para ver qué cambió
4. **Click en el archivo** para ver el contenido del backup

### Descargar un backup específico

1. **Ve a la carpeta** `backups/`
2. **Click en el archivo** que quieres descargar
3. **Click en "Download"** (botón de descarga)

### Ver diferencias entre backups

1. **Ve a:** Commits
2. **Selecciona dos commits** de backup consecutivos
3. **GitHub mostrará las diferencias** entre los backups

**Retención:** Se mantienen automáticamente los **últimos 30 backups**. Los más antiguos se eliminan automáticamente para no llenar el repositorio.

---

## 📊 Formato de los Backups

### Formato JSON (por defecto)

```json
{
  "metadata": {
    "fecha_backup": "2025-01-15T02:00:00",
    "fuente": "Supabase",
    "version": "1.0",
    "total_registros": 1234,
    "resumen": {
      "obras": 500,
      "comentarios": 300,
      "validaciones": 200,
      "historial_validaciones": 150,
      "perfiles_usuarios": 84
    }
  },
  "tables": {
    "obras": [...],
    "comentarios": [...],
    "validaciones": [...],
    "historial_validaciones": [...],
    "perfiles_usuarios": [...]
  }
}
```

### Formato SQLite (.db)

El archivo SQLite contiene:
- Tabla `backup_metadata` con información del backup
- Una tabla por cada tabla de Supabase con todos sus datos

**Para ver el contenido:**
```bash
# Instalar sqlite3 si no lo tienes
sqlite3 backup_supabase_20250115_020000.db

# Ver tablas
.tables

# Ver datos de una tabla
SELECT * FROM obras LIMIT 10;
```

---

## 🔧 Ejecutar Backup Localmente

También puedes ejecutar el script manualmente desde tu máquina:

```bash
# Backup en formato JSON (por defecto)
python scripts/backup_supabase_completo.py --output backup.json

# Backup en formato SQLite
python scripts/backup_supabase_completo.py --output backup.db --format sqlite

# Dry run (simular sin guardar)
python scripts/backup_supabase_completo.py --dry-run
```

**Requisitos:**
- Python 3.11+
- Variables de entorno `SUPABASE_URL` y `SUPABASE_KEY` configuradas
- O un archivo `.env` con estas variables

---

## 🛠️ Solución de Problemas

### Error: "SUPABASE_URL y SUPABASE_KEY deben estar definidos"

**Causa:** Los secrets de GitHub no están configurados correctamente.

**Solución:**
1. Verifica que los secrets existen en Settings → Secrets and variables → Actions
2. Verifica que los nombres son exactamente `SUPABASE_URL` y `SUPABASE_KEY`
3. Verifica que los valores son correctos (sin espacios al inicio/final)

### Error: "Permission denied" o "RLS policy violation"

**Causa:** Estás usando el Anon Key en lugar del Service Role Key.

**Solución:**
- Usa el **Service Role Key** (secreto) en el secret `SUPABASE_KEY`
- El Anon Key tiene restricciones de RLS que pueden bloquear el acceso

### El workflow no se ejecuta automáticamente

**Causa:** Los workflows programados solo funcionan en repositorios públicos o en repositorios privados con GitHub Pro/Team.

**Solución:**
- Si tu repositorio es privado y no tienes GitHub Pro, ejecuta el workflow manualmente
- O haz el repositorio público (solo el código, no los secrets)

### El commit no se crea o el push falla

**Causa:** El workflow no tiene permisos de escritura o hay un problema con Git.

**Solución:**
1. Verifica que el workflow tiene `permissions: contents: write` (ya está configurado)
2. Si el repositorio es privado y usas GitHub Free, los workflows pueden tener limitaciones
3. Revisa los logs del workflow para ver el error específico
4. Asegúrate de que la rama existe y el workflow puede hacer push a ella

### Los backups no aparecen en el repositorio

**Causa:** El workflow falló antes de hacer commit o el archivo está en `.gitignore`.

**Solución:**
1. Verifica que la carpeta `backups/` no está en `.gitignore` (ya está configurado para permitirlo)
2. Ve a la ejecución del workflow y revisa los logs
3. Verifica que el commit se creó correctamente en los logs del workflow

---

## 📝 Archivos Creados

- `scripts/backup_supabase_completo.py` - Script de backup completo
- `.github/workflows/backup-supabase.yml` - Workflow de GitHub Actions
- `BACKUP_SUPABASE_GITHUB_ACTIONS.md` - Esta documentación

---

## 🔐 Seguridad

- ✅ Los secrets de GitHub están encriptados y solo son accesibles durante la ejecución del workflow
- ✅ El Service Role Key nunca se expone en los logs
- ✅ Los backups se guardan en el repositorio, así que ten en cuenta:
  - ⚠️ Si el repositorio es público, los backups serán públicos también
  - ✅ Si el repositorio es privado, solo los colaboradores pueden ver los backups
  - ✅ Los backups contienen datos de usuarios (comentarios, validaciones), asegúrate de que el acceso al repositorio esté controlado

---

## 💡 Mejoras Futuras

Posibles mejoras que puedes implementar:

- [ ] Subir backups a Google Drive o Dropbox automáticamente
- [ ] Enviar notificaciones por email cuando se complete el backup
- [ ] Backup incremental (solo cambios desde el último backup)
- [ ] Compresión automática de backups grandes
- [ ] Backup a múltiples ubicaciones (redundancia)

---

## ✅ Checklist de Configuración

- [ ] Secrets `SUPABASE_URL` y `SUPABASE_KEY` configurados en GitHub
- [ ] Workflow visible en la pestaña Actions
- [ ] Primera ejecución manual exitosa
- [ ] Backup descargado y verificado
- [ ] Documentación leída y entendida

---

**Última actualización:** 2025-01-15
