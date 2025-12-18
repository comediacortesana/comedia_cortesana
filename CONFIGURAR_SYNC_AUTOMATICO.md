# 🔄 Configurar Sincronización Automática a Repositorio Público

## 📋 Objetivo

Cuando `iccmu` hace push a `iccmu/DELIA_DJANGO` desde GitHub Desktop, los cambios se sincronizan automáticamente a `comediacortesana/comedia_cortesana` sin necesidad de Pull Requests.

## ⚙️ Configuración Requerida

### Paso 1: Crear Personal Access Token (PAT)

1. **Ve a:** https://github.com/settings/tokens
2. **Click en:** "Generate new token" → "Generate new token (classic)"
3. **Configuración:**
   - **Note:** `Sync DELIA_DJANGO to comedia_cortesana`
   - **Expiration:** Elige una fecha (o "No expiration" si prefieres)
   - **Scopes:** Marca `repo` (acceso completo a repositorios)
4. **Click en:** "Generate token"
5. **⚠️ COPIA EL TOKEN INMEDIATAMENTE** (solo se muestra una vez)

### Paso 2: Agregar Token como Secret en GitHub

1. **Ve a:** https://github.com/iccmu/DELIA_DJANGO
2. **Click en:** Settings → Secrets and variables → Actions
3. **Click en:** "New repository secret"
4. **Configuración:**
   - **Name:** `SYNC_PAT`
   - **Secret:** Pega el token que copiaste
5. **Click en:** "Add secret"

### Paso 3: Actualizar el Workflow

El workflow ya está creado en `.github/workflows/sync-to-public-repo.yml`, pero necesitamos actualizarlo para usar el PAT:

```yaml
name: Sync to Public Repository

on:
  push:
    branches:
      - main

permissions:
  contents: write

jobs:
  sync:
    runs-on: ubuntu-latest
    
    steps:
      - name: 📥 Checkout código actual
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: 🔧 Configurar Git
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
      
      - name: 🔄 Agregar remote del repositorio público
        run: |
          git remote add public https://x-access-token:${{ secrets.SYNC_PAT }}@github.com/comediacortesana/comedia_cortesana.git || git remote set-url public https://x-access-token:${{ secrets.SYNC_PAT }}@github.com/comediacortesana/comedia_cortesana.git
      
      - name: 📤 Push al repositorio público
        run: |
          BRANCH=$(git rev-parse --abbrev-ref HEAD)
          echo "📌 Sincronizando rama: $BRANCH"
          git push public $BRANCH:main --force
          echo "✅ Sincronización completada"
```

### Paso 4: Hacer Commit y Push del Workflow

1. **Abre GitHub Desktop**
2. **Verás el archivo nuevo:** `.github/workflows/sync-to-public-repo.yml`
3. **Haz commit** con el mensaje: "🔄 Agregar sincronización automática a repositorio público"
4. **Haz push** a `iccmu/DELIA_DJANGO`

## ✅ Cómo Funciona

1. **Haces push** desde GitHub Desktop a `iccmu/DELIA_DJANGO`
2. **GitHub Actions detecta** el push a la rama `main`
3. **El workflow se ejecuta automáticamente**
4. **Sincroniza los cambios** a `comediacortesana/comedia_cortesana`
5. **Los cambios aparecen** en el repositorio público sin PR

## 🔍 Verificar que Funciona

1. **Haz un cambio pequeño** en cualquier archivo
2. **Haz commit y push** desde GitHub Desktop
3. **Ve a:** https://github.com/iccmu/DELIA_DJANGO/actions
4. **Verás el workflow** "Sync to Public Repository" ejecutándose
5. **Espera a que termine** (1-2 minutos)
6. **Verifica en:** https://github.com/comediacortesana/comedia_cortesana
7. **Deberías ver** el cambio reflejado

## ⚠️ Importante

- El workflow usa `--force` para sobrescribir cualquier cambio en el repositorio público
- Si hay cambios en `comediacortesana/comedia_cortesana` que no están en `iccmu/DELIA_DJANGO`, se perderán
- Asegúrate de que `iccmu/DELIA_DJANGO` siempre tenga la versión más actualizada antes de hacer push

## 🛠️ Solución de Problemas

### El workflow no se ejecuta

- Verifica que el archivo `.github/workflows/sync-to-public-repo.yml` existe
- Verifica que hiciste push a la rama `main`
- Ve a Actions y revisa los logs

### Error de permisos

- Verifica que el PAT tiene el scope `repo`
- Verifica que el secret `SYNC_PAT` está configurado correctamente
- Verifica que `iccmu` tiene permisos de escritura en `comediacortesana/comedia_cortesana`

### Los cambios no aparecen en el repositorio público

- Revisa los logs del workflow en Actions
- Verifica que el push fue exitoso
- Espera unos minutos (puede haber delay)
