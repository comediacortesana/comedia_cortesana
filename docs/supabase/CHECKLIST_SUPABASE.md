# ✅ Checklist Rápido: Integración Supabase

## 📋 Resumen de Pasos

### ✅ PARTE 1: Supabase (15 min)
- [ ] Crear cuenta en https://supabase.com
- [ ] Crear nuevo proyecto (Free tier)
- [ ] Anotar credenciales:
  - [ ] Project URL: `https://xxxxx.supabase.co`
  - [ ] anon public key: `eyJhbGc...`
  - [ ] service_role key: `eyJhbGc...` ⚠️ SECRETO

### ✅ PARTE 2: Base de Datos (10 min)
- [ ] Abrir SQL Editor en Supabase
- [ ] Ejecutar `supabase_schema.sql` completo
- [ ] Verificar que se crearon 5 tablas:
  - [ ] obras
  - [ ] comentarios
  - [ ] validaciones
  - [ ] historial_validaciones
  - [ ] perfiles_usuarios

### ✅ PARTE 3: Frontend HTML (20 min)
- [ ] Añadir script de Supabase en `<head>`
- [ ] Añadir configuración (URL y anon key)
- [ ] Añadir funciones de autenticación
- [ ] Añadir UI de login (HTML)
- [ ] Añadir funciones de comentarios
- [ ] Modificar `mostrarDetalleObra()` para incluir comentarios
- [ ] Añadir estilos CSS para comentarios
- [ ] Modificar `window.onload` para verificar sesión

### ✅ PARTE 4: Apps Script (10 min)
- [ ] Añadir funciones de sincronización Supabase
- [ ] Ejecutar `setSupabaseServiceKey()` con tu service_role key
- [ ] (Opcional) Modificar `syncToGitHub()` para incluir Supabase

### ✅ PARTE 5: Probar (10 min)
- [ ] Abrir sitio en GitHub Pages
- [ ] Registrar un usuario
- [ ] Confirmar email
- [ ] Iniciar sesión
- [ ] Abrir una obra y dejar un comentario
- [ ] Verificar comentario en Supabase Table Editor
- [ ] Ejecutar `syncToSupabase()` en Apps Script
- [ ] Verificar obras en Supabase Table Editor

---

## 📁 Archivos Creados

1. **GUIA_SUPABASE_PASO_A_PASO.md** - Guía completa detallada
2. **supabase_schema.sql** - Script SQL completo para ejecutar
3. **supabase_frontend_code.js** - Código JavaScript para el HTML
4. **supabase_apps_script_code.gs** - Código para Apps Script

---

## 🔑 Credenciales Necesarias

### Para Frontend (index.html):
- `SUPABASE_URL`: Tu Project URL
- `SUPABASE_ANON_KEY`: Tu anon public key

### Para Apps Script:
- `SUPABASE_SERVICE_KEY`: Tu service_role key (SECRETO)

---

## ⚠️ Recordatorios Importantes

1. **NUNCA** subas las keys a GitHub (especialmente service_role)
2. **Usa anon key** en el frontend (público, seguro con RLS)
3. **Usa service_role key** solo en Apps Script (privado)
4. **Ejecuta el SQL completo** en Supabase antes de probar
5. **Verifica las políticas RLS** están activas

---

## 🆘 Si Algo Falla

### Error: "Invalid API key"
- Verifica que copiaste correctamente las keys
- Asegúrate de usar anon key en frontend, service_role en Apps Script

### Error: "Row Level Security policy violation"
- Verifica que ejecutaste todas las políticas RLS
- Asegúrate de estar autenticado para crear comentarios

### Los comentarios no aparecen
- Abre consola del navegador (F12) y revisa errores
- Verifica que el `obra_id` coincide con el ID de la obra

### La sincronización falla
- Verifica que configuraste `setSupabaseServiceKey()` correctamente
- Revisa los logs en Apps Script

---

## 📚 Documentación Completa

Ver **GUIA_SUPABASE_PASO_A_PASO.md** para instrucciones detalladas paso a paso.

---

**¡Éxito! 🎉**

