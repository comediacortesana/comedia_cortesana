# 🗑️ Cómo Eliminar un Usuario de Supabase

## Para probar registro/confirmación de nuevo

Si quieres probar el flujo completo de registro y confirmación de cuenta, necesitas eliminar el usuario primero.

## ✅ Método 1: Desde Supabase Dashboard (RECOMENDADO - Más fácil)

1. **Ve a Supabase Dashboard:** https://supabase.com/dashboard
2. **Selecciona tu proyecto**
3. **Ve a:** Authentication → Users
4. **Busca el usuario** por email: `isimo@ucm.es`
5. **Click en los tres puntos** (...) junto al usuario
6. **Click en:** "Delete user"
7. **Confirma** la eliminación

**Ventajas:**
- ✅ Más fácil y visual
- ✅ Elimina automáticamente todos los datos relacionados por CASCADE
- ✅ No requiere permisos SQL especiales

## 🔧 Método 2: Desde SQL Editor

Si prefieres usar SQL:

1. **Ve a:** SQL Editor en Supabase
2. **Abre el archivo:** `supabase_eliminar_usuario_completo.sql`
3. **Ejecuta el script** (ya tiene el email `isimo@ucm.es` configurado)
4. **Verifica** que se eliminó ejecutando la consulta de verificación al final del script

## 📋 Qué se elimina

Cuando eliminas un usuario, se eliminan automáticamente:
- ✅ Usuario de `auth.users`
- ✅ Perfil de `perfiles_usuarios` (por CASCADE)
- ✅ Comentarios del usuario
- ✅ Cambios pendientes del usuario

## 🔍 Verificar eliminación

Después de eliminar, verifica que se eliminó:

```sql
-- Verificar que no existe en auth.users
SELECT id, email FROM auth.users WHERE email = 'isimo@ucm.es';
-- Debería retornar 0 filas

-- Verificar que el perfil también se eliminó
SELECT * FROM perfiles_usuarios 
WHERE id IN (SELECT id FROM auth.users WHERE email = 'isimo@ucm.es');
-- Debería retornar 0 filas
```

## 🧪 Después de eliminar

Una vez eliminado el usuario:

1. **Ve a tu aplicación** en GitHub Pages
2. **Regístrate de nuevo** con `isimo@ucm.es`
3. **Confirma el email** desde tu correo
4. **Deberías ser redirigido** a GitHub Pages (no localhost)
5. **La sesión se establecerá automáticamente**

## ⚠️ Nota Importante

Si el usuario tiene datos importantes (comentarios, cambios aprobados, etc.), considera hacer un backup antes de eliminar, o simplemente usa un email diferente para las pruebas.

