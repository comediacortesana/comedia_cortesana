# 📋 Cómo Copiar el Workflow al Repositorio Público

## Situación Actual

- ✅ Workflow creado en: `iccmu/DELIA_DJANGO`
- ⚠️ Necesitas copiarlo a: `comediacortesana/comedia_cortesana`

## Pasos para Copiar el Workflow

### Opción A: Desde GitHub Desktop (Más Fácil)

1. **Abre GitHub Desktop**
2. **Cambia al repositorio** `comedia_cortesana` (si lo tienes clonado)
3. **Crea la carpeta** `.github/workflows/` si no existe
4. **Copia el archivo** `.github/workflows/backup-supabase.yml` desde `DELIA_DJANGO`
5. **Haz commit y push** al repositorio `comediacortesana/comedia_cortesana`

### Opción B: Desde Terminal

```bash
# 1. Clonar el repositorio público (si no lo tienes)
cd /Users/ivansimo/Documents/2025/ITEM
git clone https://github.com/comediacortesana/comedia_cortesana.git

# 2. Crear la carpeta de workflows
cd comedia_cortesana
mkdir -p .github/workflows

# 3. Copiar el workflow desde DELIA_DJANGO
cp ../DELIA_DJANGO/.github/workflows/backup-supabase.yml .github/workflows/

# 4. Copiar también el script de backup
cp ../DELIA_DJANGO/scripts/backup_supabase_completo.py scripts/

# 5. Hacer commit y push
git add .github/workflows/backup-supabase.yml scripts/backup_supabase_completo.py
git commit -m "🔄 Agregar automatización de backup de Supabase"
git push origin main
```

### Opción C: Desde GitHub Web

1. **Ve a:** https://github.com/comediacortesana/comedia_cortesana
2. **Click en:** "Add file" → "Create new file"
3. **Ruta:** `.github/workflows/backup-supabase.yml`
4. **Copia el contenido** del archivo desde `iccmu/DELIA_DJANGO`
5. **Click en:** "Commit new file"

## Después de Copiar

1. **Configurar Secrets** en `comediacortesana/comedia_cortesana`:
   - Ve a Settings → Secrets and variables → Actions
   - Agrega `SUPABASE_URL` y `SUPABASE_KEY`

2. **Probar el workflow**:
   - Ve a Actions → Backup Supabase Database
   - Click en "Run workflow"

3. **Verificar que funciona**:
   - Después de ejecutarse, deberías ver la carpeta `backups/` en el repositorio
   - Y un commit nuevo con el backup

## Importante

- El workflow funcionará en el repositorio donde lo copies
- Los backups se guardarán en ese repositorio
- Necesitas configurar los secrets en cada repositorio donde uses el workflow
