# 👑 Hacer Admin a Múltiples Usuarios

## 🎯 Cambiar rol a "admin" para:
- **f.saez@filol.ucm.es**
- **delia.gavela@gmail.com**

---

## ⚡ Método Rápido: SQL (Recomendado)

### Paso 1: Ejecutar SQL

1. Ve a Supabase Dashboard → **SQL Editor**
2. Copia y pega este SQL:

```sql
UPDATE perfiles_usuarios
SET rol = 'admin'
WHERE id IN (
    SELECT id FROM auth.users 
    WHERE email IN ('f.saez@filol.ucm.es', 'delia.gavela@gmail.com')
);
```

3. Haz clic en **"Run"** o presiona `Ctrl+Enter` (o `Cmd+Enter` en Mac)
4. Deberías ver: `Success. No rows returned`

### Paso 2: Verificar

Ejecuta este SQL para verificar que ambos usuarios ahora son admin:

```sql
SELECT 
    pu.id,
    au.email,
    pu.nombre_completo,
    pu.rol
FROM perfiles_usuarios pu
JOIN auth.users au ON pu.id = au.id
WHERE au.email IN ('f.saez@filol.ucm.es', 'delia.gavela@gmail.com')
ORDER BY au.email;
```

Deberías ver ambos usuarios con `rol = 'admin'`

---

## 🖱️ Método Alternativo: Desde Table Editor

Si prefieres usar la interfaz visual:

1. Ve a Supabase Dashboard → **Table Editor**
2. Selecciona la tabla **`perfiles_usuarios`**
3. Busca cada usuario:
   - Busca `f.saez@filol.ucm.es`
   - Busca `delia.gavela@gmail.com`
4. Para cada uno:
   - Haz clic en la fila
   - Haz clic en el campo **`rol`**
   - Cambia a **`admin`**
   - Guarda (`Ctrl+S` o `Cmd+S`)

---

## ✅ Después de Cambiar los Roles

Ambos usuarios deben:

1. **Cerrar sesión** en la aplicación
2. **Volver a iniciar sesión**
3. Los cambios de rol se aplican al iniciar sesión

Después de iniciar sesión, deberían ver:
- El botón **"⚙️ Panel Admin"** (morado) en la interfaz
- Acceso a funciones administrativas

---

## 👑 ¿Qué Puede Hacer un Usuario con Rol "admin"?

- ✅ **Todas las funciones de colaborador y editor**
- ✅ **Aprobar cambios pendientes** de otros usuarios
- ✅ **Gestionar usuarios** (cambiar roles, ver perfiles)
- ✅ **Persistir cambios directamente** sin necesidad de aprobación
- ✅ **Acceso completo** a todas las funciones del sistema
- ✅ **Ver estadísticas y reportes** administrativos

---

## 🔍 Verificar Todos los Admins

Para ver todos los usuarios con rol "admin":

```sql
SELECT 
    pu.id,
    au.email,
    pu.nombre_completo,
    pu.rol,
    pu.created_at
FROM perfiles_usuarios pu
JOIN auth.users au ON pu.id = au.id
WHERE pu.rol = 'admin'
ORDER BY pu.created_at DESC;
```

---

## 🚨 Troubleshooting

### Los usuarios no existen

Si alguno de los usuarios no existe, verifica:

```sql
-- Verificar si los usuarios existen en auth.users
SELECT id, email, created_at 
FROM auth.users 
WHERE email IN ('f.saez@filol.ucm.es', 'delia.gavela@gmail.com');
```

Si falta algún usuario:
1. El usuario debe registrarse primero en la aplicación
2. O créalo manualmente desde **Authentication** → **Users** → **Add user**

### Los perfiles no existen

Si los usuarios existen pero no tienen perfil:

```sql
-- Verificar perfiles
SELECT * FROM perfiles_usuarios 
WHERE id IN (
    SELECT id FROM auth.users 
    WHERE email IN ('f.saez@filol.ucm.es', 'delia.gavela@gmail.com')
);
```

Si falta algún perfil, créalo:

```sql
INSERT INTO perfiles_usuarios (id, nombre_completo, rol)
SELECT id, email, 'admin'
FROM auth.users
WHERE email IN ('f.saez@filol.ucm.es', 'delia.gavela@gmail.com')
ON CONFLICT (id) DO UPDATE SET rol = 'admin';
```

### Los cambios no se aplican en la aplicación

1. **Los usuarios deben cerrar sesión y volver a iniciar sesión**
2. Limpia la caché del navegador (`Ctrl+Shift+R` o `Cmd+Shift+R`)
3. Verifica que el cambio se guardó en Supabase:
   ```sql
   SELECT email, rol FROM perfiles_usuarios pu
   JOIN auth.users au ON pu.id = au.id
   WHERE au.email IN ('f.saez@filol.ucm.es', 'delia.gavela@gmail.com');
   ```

### Error de permisos

Si ves un error de permisos al ejecutar el SQL:
- Asegúrate de estar usando el SQL Editor de Supabase (no desde la aplicación)
- Verifica que tienes permisos de administrador en el proyecto de Supabase

---

## 📝 Archivo SQL Listo

También puedes usar el archivo `cambiar_rol_admin.sql` que incluye el SQL completo con verificaciones.

---

## 🎯 Resumen Rápido

**Para hacer admin rápidamente:**

1. Ve a **SQL Editor** en Supabase
2. Ejecuta:
   ```sql
   UPDATE perfiles_usuarios
   SET rol = 'admin'
   WHERE id IN (
       SELECT id FROM auth.users 
       WHERE email IN ('f.saez@filol.ucm.es', 'delia.gavela@gmail.com')
   );
   ```
3. Verifica con el SELECT de arriba
4. Los usuarios deben cerrar sesión y volver a iniciar sesión

¡Listo! 🎉
