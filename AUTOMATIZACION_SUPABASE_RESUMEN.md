# 🤖 Automatización Supabase - Resumen Rápido

## ✅ ¿Qué se ha creado?

### 1. GitHub Action (`.github/workflows/keep-supabase-active.yml`)
- Ejecuta automáticamente 2 veces al día (9:00 y 21:00 UTC)
- Hace consultas ligeras a Supabase
- **Totalmente gratis** en repos públicos

### 2. Script Python (`scripts/keep_supabase_active.py`)
- Hace 3 consultas simples (obras, comentarios, perfiles)
- 1 registro por consulta = muy ligero
- Registra logs de cada ejecución

### 3. Guía completa (`GUIA_AUTOMATIZACION_SUPABASE.md`)
- Instrucciones paso a paso
- Configuración de GitHub Secrets
- Solución de problemas
- Personalización

### 4. Script de prueba (`scripts/test_keep_active.sh`)
- Para probar localmente antes de subir

---

## 🚀 Próximos Pasos (5 minutos)

### 1️⃣ Subir archivos a GitHub

```bash
cd /Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO

git add .github/workflows/keep-supabase-active.yml
git add comedia_cortesana/scripts/keep_supabase_active.py
git add comedia_cortesana/GUIA_AUTOMATIZACION_SUPABASE.md

git commit -m "feat: Automatización para mantener Supabase activo"
git push origin main
```

### 2️⃣ Configurar Secrets en GitHub

1. Ve a tu repo en GitHub
2. Settings > Secrets and variables > Actions
3. Añade dos secrets:

**SUPABASE_URL**
```
https://kyxxpoewwjixbpcezays.supabase.co
```

**SUPABASE_KEY** (anon public key)
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt5eHhwb2V3d2ppeGJwY2V6YXlzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI0MjAzMDksImV4cCI6MjA3Nzk5NjMwOX0.sIw7flVHQ00r3VwrhU7tvohVzKpb7LGtXVzG43FAP10
```

### 3️⃣ Activar y Probar

1. Ve a Actions en GitHub
2. Habilita los workflows (botón verde)
3. Busca "Keep Supabase Active"
4. Haz clic en "Run workflow" para probar
5. Verifica que sale ✅ verde

---

## 📊 Resultado

Una vez configurado:
- ✅ 2 consultas automáticas al día (6 queries totales)
- ✅ Supabase se mantiene activo
- ✅ Sin costo adicional
- ✅ Logs disponibles en GitHub Actions
- ✅ Notificaciones por email si falla

---

## 📚 Documentación

- **Guía completa**: `GUIA_AUTOMATIZACION_SUPABASE.md`
- **Workflow**: `.github/workflows/keep-supabase-active.yml`
- **Script**: `scripts/keep_supabase_active.py`
- **Test local**: `scripts/test_keep_active.sh`

---

## 💡 Alternativas (si no quieres usar GitHub Actions)

1. **Cron-job.org** (servicio gratuito de cron jobs web)
2. **Uptimerobot.com** (monitoreo gratuito con pings)
3. **Vercel Cron** (si usas Vercel para hosting)
4. **Script local con crontab** (en tu ordenador)

Pero **GitHub Actions es la mejor opción** porque:
- ✅ Gratis e ilimitado (repos públicos)
- ✅ Se ejecuta en la nube (no necesitas tu ordenador encendido)
- ✅ Integrado con tu repo
- ✅ Logs y monitoreo incluidos

---

**¿Dudas?** Lee la guía completa en `GUIA_AUTOMATIZACION_SUPABASE.md`

