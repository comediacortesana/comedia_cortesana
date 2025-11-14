# 👤 Cambiar Rol de Usuario en Supabase

## 🎯 Hacer Admin a un Usuario

Hay dos formas de cambiar el rol de un usuario a 'admin':

---

## 📋 Método 1: Desde la Interfaz de Supabase (Más Fácil)

### Paso 1: Encontrar el Usuario

1. Ve a tu proyecto en Supabase: https://supabase.com/dashboard
2. Abre **Table Editor** (o **Editor de Tablas**)
3. Selecciona la tabla **`perfiles_usuarios`**
4. Busca el usuario que quieres hacer admin (por email o nombre)

### Paso 2: Editar el Rol

1. Haz clic en la fila del usuario
2. Haz clic en el campo **`rol`**
3. Cambia el valor de `colaborador` o `editor` a **`admin`**
4. Guarda los cambios (Ctrl+S o Cmd+S)

### Paso 3: Verificar

1. Recarga la página de tu aplicación
2. Inicia sesión con ese usuario
3. Deberías ver el botón **"⚙️ Panel Admin"** (morado)

---

## 📋 Método 2: Usando SQL (Más Rápido)

### Opción A: Cambiar por Email

1. Ve a **SQL Editor** en Supabase
2. Ejecuta este SQL (reemplaza el email):

```sql
UPDATE perfiles_usuarios
SET rol = 'admin'
WHERE id IN (
    SELECT id FROM auth.users WHERE email = 'isimosanchez@gmail.com'
);
```

### Opción B: Cambiar por UUID (Más Preciso)

1. Primero obtén el UUID del usuario:
   - Ve a **Authentication** → **Users**
   - Busca el usuario y copia su UUID

2. Ejecuta este SQL (reemplaza el UUID):

```sql
UPDATE perfiles_usuarios
SET rol = 'admin'
WHERE id = 'TU-UUID-AQUI';
```

### Opción C: Cambiar por Nombre Completo

```sql
UPDATE perfiles_usuarios
SET rol = 'admin'
WHERE nombre_completo = 'isimosanchez@gmail.com';
```

---

## 🔍 Verificar que Funcionó

Después de cambiar el rol, ejecuta este SQL para verificar:

```sql
SELECT id, nombre_completo, rol, created_at
FROM perfiles_usuarios
WHERE rol = 'admin';
```

Deberías ver tu usuario con `rol = 'admin'`.

---

## 🎭 Roles Disponibles

- **`colaborador`** - Por defecto. Puede ver, filtrar, exportar y comentar
- **`editor`** - Puede editar datos (cambios requieren aprobación)
- **`admin`** - Acceso completo: gestionar usuarios, aprobar cambios, persistir datos

---

## 🚨 Troubleshooting

### No veo el botón Admin después de cambiar el rol

1. **Cierra sesión y vuelve a iniciar sesión**
   - El rol se carga al iniciar sesión
   - Los cambios no se aplican hasta que recargas la sesión

2. **Verifica que el cambio se guardó**
   ```sql
   SELECT * FROM perfiles_usuarios WHERE id = 'TU-UUID';
   ```

3. **Limpia la caché del navegador**
   - Ctrl+Shift+R (Windows/Linux)
   - Cmd+Shift+R (Mac)

4. **Ejecuta diagnóstico desde la consola**
   ```javascript
   diagnosticarUsuario()
   ```

### Error: "No se puede editar"

- Verifica que tienes permisos en Supabase
- Si usas RLS, asegúrate de que las políticas permiten editar

---

## 💡 Consejo Rápido

**Para hacer admin rápidamente:**

1. Ve a **Table Editor** → **perfiles_usuarios**
2. Busca tu usuario
3. Cambia `rol` a `admin`
4. Guarda
5. Recarga la página y vuelve a iniciar sesión

¡Listo! 🎉

