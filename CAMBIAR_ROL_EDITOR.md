# ✏️ Cambiar Rol a "editor" - Guía Rápida

## 🎯 Cambiar rol de f.saez@filol.ucm.es a "editor"

### Método 1: Usando SQL (Más Rápido) ⚡

1. Ve a Supabase Dashboard → **SQL Editor**
2. Copia y pega este SQL:

```sql
UPDATE perfiles_usuarios
SET rol = 'editor'
WHERE id IN (
    SELECT id FROM auth.users WHERE email = 'f.saez@filol.ucm.es'
);
```

3. Haz clic en **"Run"** o presiona `Ctrl+Enter` (o `Cmd+Enter` en Mac)
4. Deberías ver: `Success. No rows returned`

5. **Verificar** que funcionó:

```sql
SELECT 
    pu.id,
    au.email,
    pu.nombre_completo,
    pu.rol
FROM perfiles_usuarios pu
JOIN auth.users au ON pu.id = au.id
WHERE au.email = 'f.saez@filol.ucm.es';
```

Deberías ver `rol = 'editor'`

---

### Método 2: Desde Table Editor (Interfaz Visual) 🖱️

1. Ve a Supabase Dashboard → **Table Editor**
2. Selecciona la tabla **`perfiles_usuarios`**
3. Busca el usuario con email `f.saez@filol.ucm.es`
   - Puedes usar el filtro de búsqueda si hay muchos usuarios
4. Haz clic en la fila del usuario
5. Haz clic en el campo **`rol`**
6. Cambia el valor a **`editor`**
7. Guarda los cambios (`Ctrl+S` o `Cmd+S`)

---

## ✅ Después de Cambiar el Rol

El usuario **f.saez@filol.ucm.es** debe:

1. **Cerrar sesión** en la aplicación
2. **Volver a iniciar sesión**
3. Los cambios de rol se aplican al iniciar sesión

---

## 🎭 ¿Qué Puede Hacer un Usuario con Rol "editor"?

- ✅ Ver todas las obras
- ✅ Filtrar y buscar obras
- ✅ Exportar datos
- ✅ Agregar comentarios
- ✅ **Editar datos de obras** (los cambios requieren aprobación de un admin)
- ✅ Ver historial de validaciones
- ❌ No puede aprobar cambios pendientes
- ❌ No puede gestionar usuarios
- ❌ No puede persistir cambios directamente

---

## 🔍 Verificar Todos los Editores

Para ver todos los usuarios con rol "editor":

```sql
SELECT 
    pu.id,
    au.email,
    pu.nombre_completo,
    pu.rol,
    pu.created_at
FROM perfiles_usuarios pu
JOIN auth.users au ON pu.id = au.id
WHERE pu.rol = 'editor'
ORDER BY pu.created_at DESC;
```

---

## 🚨 Troubleshooting

### El cambio no se aplica

1. **Verifica que el usuario existe:**
   ```sql
   SELECT * FROM auth.users WHERE email = 'f.saez@filol.ucm.es';
   ```

2. **Verifica que el perfil existe:**
   ```sql
   SELECT * FROM perfiles_usuarios 
   WHERE id IN (
       SELECT id FROM auth.users WHERE email = 'f.saez@filol.ucm.es'
   );
   ```

3. **Si el perfil no existe**, créalo primero:
   ```sql
   INSERT INTO perfiles_usuarios (id, nombre_completo, rol)
   SELECT id, email, 'editor'
   FROM auth.users
   WHERE email = 'f.saez@filol.ucm.es'
   ON CONFLICT (id) DO UPDATE SET rol = 'editor';
   ```

### El usuario no ve los cambios

- Debe **cerrar sesión y volver a iniciar sesión**
- El rol se carga al iniciar sesión
- Limpia la caché del navegador si es necesario (`Ctrl+Shift+R` o `Cmd+Shift+R`)

---

## 📝 Archivo SQL Listo

También puedes usar el archivo `cambiar_rol_editor.sql` que incluye el SQL completo con verificaciones.
