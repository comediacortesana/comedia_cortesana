# 🤖 Automatización: Mantener Supabase Activo

## 📋 ¿Qué hace esto?

Este sistema **automáticamente hace consultas a Supabase** 2 veces al día para mantenerlo activo y evitar que se pause por inactividad.

### ⏰ Schedule
- **Primera consulta**: 9:00 UTC (10:00 CET / 11:00 CEST)
- **Segunda consulta**: 21:00 UTC (22:00 CET / 23:00 CEST)

### 🔍 Consultas realizadas
Cada ejecución hace consultas simples a:
- Tabla `obras` (1 registro)
- Tabla `comentarios` (1 registro)
- Tabla `perfiles_usuarios` (1 registro)

**Total**: ~3 consultas ligeras, 2 veces al día = **6 consultas diarias**

---

## 🚀 Configuración (Paso a Paso)

### Paso 1: Subir los archivos al repositorio

Los archivos ya están creados:
- `.github/workflows/keep-supabase-active.yml` - Configuración de GitHub Actions
- `comedia_cortesana/scripts/keep_supabase_active.py` - Script de consultas

Súbelos a tu repositorio:

```bash
cd /Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO

# Añadir archivos
git add .github/workflows/keep-supabase-active.yml
git add comedia_cortesana/scripts/keep_supabase_active.py

# Commit
git commit -m "feat: Agregar automatización para mantener Supabase activo"

# Push
git push origin main
```

### Paso 2: Configurar Secrets en GitHub

Las credenciales de Supabase deben guardarse de forma segura en GitHub Secrets.

1. **Ve a tu repositorio en GitHub**
   - URL: `https://github.com/TU-USUARIO/TU-REPO`

2. **Accede a Settings**
   - Haz clic en la pestaña **"Settings"** (arriba)

3. **Ve a Secrets and variables > Actions**
   - En el menú lateral: **"Secrets and variables"** → **"Actions"**

4. **Añade los secrets** (haz clic en "New repository secret"):

   **Secret 1: SUPABASE_URL**
   ```
   Name: SUPABASE_URL
   Value: https://kyxxpoewwjixbpcezays.supabase.co
   ```

   **Secret 2: SUPABASE_KEY**
   ```
   Name: SUPABASE_KEY
   Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt5eHhwb2V3d2ppeGJwY2V6YXlzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI0MjAzMDksImV4cCI6MjA3Nzk5NjMwOX0.sIw7flVHQ00r3VwrhU7tvohVzKpb7LGtXVzG43FAP10
   ```
   
   ⚠️ **IMPORTANTE**: Usa el `anon public key` aquí, NO el `service_role key`
   
   El `anon public key` es suficiente para consultas de lectura y es más seguro.

5. **Verificar que se crearon**
   - Deberías ver ambos secrets listados
   - No podrás ver los valores (son secretos), solo los nombres

### Paso 3: Activar GitHub Actions

1. **Ve a la pestaña "Actions"** en tu repositorio

2. **Si está desactivado**, verás un botón verde que dice:
   - **"I understand my workflows, go ahead and enable them"**
   - Haz clic en él

3. **Busca el workflow**
   - En el menú lateral izquierdo verás: **"Keep Supabase Active"**
   - Haz clic en él

### Paso 4: Ejecutar manualmente (prueba)

Para probar que funciona antes de esperar al schedule:

1. **Ve a Actions > Keep Supabase Active**

2. **Haz clic en "Run workflow"** (botón en la derecha)
   - Branch: `main`
   - Haz clic en el botón verde **"Run workflow"**

3. **Espera unos segundos** y actualiza la página
   - Verás una nueva ejecución en curso (círculo amarillo 🟡)
   - Cuando termine será verde ✅ (éxito) o rojo ❌ (error)

4. **Haz clic en la ejecución** para ver los logs
   - Podrás ver cada paso:
     - ✅ Checkout repository
     - ✅ Setup Python
     - ✅ Install dependencies
     - ✅ Query Supabase
     - ✅ Log completion

5. **Verifica el output**
   - En "Query Supabase" verás:
     ```
     ✅ Obras: OK (1 registros)
     ✅ Comentarios: OK (1 registros)
     ✅ Perfiles: OK (1 registros)
     ```

---

## ✅ Verificación

### ¿Cómo saber si está funcionando?

1. **Ver historial de ejecuciones**
   - Ve a **Actions** en GitHub
   - Verás una lista de ejecuciones pasadas
   - Cada ejecución exitosa tiene ✅ verde

2. **Verificar logs**
   - Haz clic en cualquier ejecución
   - Haz clic en "query-supabase"
   - Verás los logs detallados

3. **Recibir notificaciones** (opcional)
   - GitHub puede enviarte emails si una ejecución falla
   - Ve a Settings > Notifications en tu perfil

### Schedule de ejecuciones

Las ejecuciones automáticas aparecerán a las:
- **9:00 UTC** todos los días
- **21:00 UTC** todos los días

Nota: GitHub Actions puede tener un retraso de 5-15 minutos en el schedule.

---

## 🔧 Personalización

### Cambiar la frecuencia

Edita `.github/workflows/keep-supabase-active.yml`:

```yaml
schedule:
  # Cada 6 horas (4 veces al día)
  - cron: '0 */6 * * *'
  
  # Cada hora
  - cron: '0 * * * *'
  
  # Solo una vez al día (mediodía UTC)
  - cron: '0 12 * * *'
  
  # Cada día laborable a las 9:00 UTC
  - cron: '0 9 * * 1-5'
```

**Referencia de sintaxis cron**:
```
┌───────────── minuto (0 - 59)
│ ┌───────────── hora (0 - 23)
│ │ ┌───────────── día del mes (1 - 31)
│ │ │ ┌───────────── mes (1 - 12)
│ │ │ │ ┌───────────── día de la semana (0 - 6) (domingo = 0)
│ │ │ │ │
* * * * *
```

### Agregar más consultas

Edita `comedia_cortesana/scripts/keep_supabase_active.py`:

```python
queries = [
    {
        'name': 'Obras',
        'endpoint': '/rest/v1/obras',
        'params': {'select': 'id', 'limit': '1'}
    },
    {
        'name': 'Validaciones',
        'endpoint': '/rest/v1/validaciones',
        'params': {'select': 'id', 'limit': '1'}
    },
    # Agregar más aquí...
]
```

---

## 💰 Costos

### GitHub Actions (Gratis)
- **Repos públicos**: Ilimitado ✅
- **Repos privados**: 2,000 minutos/mes gratis
- Este workflow usa ~1 minuto por ejecución
- 2 ejecuciones/día × 30 días = 60 minutos/mes

### Supabase (Plan gratuito)
- Este sistema genera **6 consultas ligeras/día**
- Supabase Free tier: 500MB base de datos, 2GB transferencia
- Las consultas son extremadamente ligeras (1 registro)
- **No afecta tu cuota mensual**

---

## 🔒 Seguridad

### ✅ Buenas prácticas implementadas:
- ✅ Credenciales guardadas en GitHub Secrets (encriptadas)
- ✅ Uso de `anon public key` (no `service_role`)
- ✅ Solo consultas de lectura (SELECT)
- ✅ Límite de 1 registro por consulta
- ✅ Timeout de 10 segundos por request
- ✅ No se exponen credenciales en logs

### ⚠️ Advertencias:
- NO subas las credenciales al código
- NO uses el `service_role key` en GitHub Actions
- NO hagas consultas pesadas (límite de 1 registro)

---

## 🆘 Solución de Problemas

### Error: "Resource not accessible by integration"

**Problema**: GitHub Actions no tiene permisos.

**Solución**:
1. Ve a Settings > Actions > General
2. En "Workflow permissions", selecciona:
   - ✅ "Read and write permissions"
3. Guarda los cambios

### Error: "Invalid API key"

**Problema**: Los secrets no están configurados correctamente.

**Solución**:
1. Verifica que SUPABASE_URL y SUPABASE_KEY están en GitHub Secrets
2. Verifica que los valores son correctos
3. Asegúrate de usar el `anon public key`

### Error: "HTTP 406" o "HTTP 404"

**Problema**: Tabla no existe o RLS bloquea la consulta.

**Solución**:
1. Verifica que las tablas existen en Supabase
2. Verifica las políticas RLS:
   - Las tablas deben tener políticas de lectura pública
   - O usa el `service_role key` (menos seguro)

### El workflow no se ejecuta automáticamente

**Problema**: GitHub puede pausar workflows en repos inactivos.

**Solución**:
1. Haz un commit al repo al menos una vez al mes
2. O ejecuta el workflow manualmente una vez al mes
3. GitHub avisa por email antes de pausar

---

## 📊 Monitoreo

### Ver estadísticas

Puedes ver cuántas veces se ha ejecutado:

1. **Insights > Actions**
   - Ve a la pestaña "Insights"
   - Luego "Actions" en el menú lateral
   - Verás gráficos de ejecuciones

2. **Actions > Workflows**
   - Lista de todas las ejecuciones
   - Filtra por fecha, estado, etc.

### Notificaciones por email

GitHub te enviará un email si:
- ❌ Una ejecución falla
- ⚠️ Un workflow está deshabilitado por inactividad

---

## 🎯 Checklist Final

- [ ] Archivos subidos al repositorio
- [ ] Secrets configurados en GitHub
- [ ] GitHub Actions habilitado
- [ ] Prueba manual exitosa
- [ ] Primera ejecución automática completada
- [ ] Notificaciones configuradas (opcional)

---

## 📚 Referencias

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Cron syntax](https://crontab.guru/)
- [Supabase API Docs](https://supabase.com/docs/guides/api)
- [GitHub Actions pricing](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions)

---

**Fecha de creación**: Diciembre 4, 2025  
**Última actualización**: Diciembre 4, 2025

