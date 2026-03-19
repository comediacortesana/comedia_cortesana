# 👤 Crear Usuario Manualmente en Supabase

## 🎯 Objetivo

Crear el usuario "paco" con contraseña "12345678" directamente en Supabase.

## 📋 Método 1: Desde el Dashboard de Supabase (Más Fácil)

### Paso 1: Acceder a Users

1. Ve a tu proyecto en Supabase: https://supabase.com/dashboard
2. En el menú lateral izquierdo, ve a **Authentication**
3. Haz clic en **Users**

### Paso 2: Crear Nuevo Usuario

1. Haz clic en el botón **"Add user"** o **"Invite user"** (arriba a la derecha)
2. Se abrirá un formulario con las siguientes opciones:

   **Opción A: Invite user (Recomendado)**
   - **Email:** `paco@example.com` (o el email que quieras)
   - **Auto Confirm:** ✅ **Marca esta casilla** (esto confirma el email automáticamente)
   - Haz clic en **"Send invitation"**
   - El usuario recibirá un email para establecer su contraseña
   - **Desventaja:** El usuario debe establecer su contraseña desde el email

   **Opción B: Add user (Mejor para crear usuario con contraseña)**
   - Si no ves esta opción, ve a **Authentication** → **Settings** → busca **"Enable email confirmations"** y desactívala temporalmente
   - Luego vuelve a **Users** → **Add user**
   - **Email:** `paco@example.com`
   - **Password:** `12345678`
   - **Auto Confirm User:** ✅ **Marca esta casilla**
   - Haz clic en **"Create user"**

### Paso 3: Verificar que el Perfil se Creó

1. Ve a **Table Editor** → **perfiles_usuarios**
2. Busca el usuario que acabas de crear
3. Debería tener:
   - **id:** (UUID del usuario)
   - **nombre_completo:** `paco` (o el email si no se configuró)
   - **rol:** `colaborador`

Si el perfil no se creó automáticamente, ve al **Método 3** para crearlo manualmente.

## 📋 Método 2: Usando el Script Python (Recomendado)

### Paso 1: Obtener la Service Role Key

1. Ve a Supabase Dashboard → **Settings** → **API**
2. Busca la sección **"Project API keys"**
3. Copia la **"service_role"** key (⚠️ NO la "anon" key)
4. Esta key tiene permisos de administrador, mantenla segura

### Paso 2: Configurar la Variable de Entorno

En tu terminal:

```bash
export SUPABASE_SERVICE_ROLE_KEY='tu-service-role-key-aqui'
```

O si prefieres, puedes editar el script y ponerla directamente (solo para desarrollo).

### Paso 3: Ejecutar el Script

```bash
cd /Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO
python3 scripts/crear_usuario_supabase.py
```

El script creará:
- **Email:** `paco@example.com`
- **Contraseña:** `12345678`
- **Nombre completo:** `paco`
- **Email confirmado:** Sí (puede iniciar sesión inmediatamente)
- **Perfil:** Se crea automáticamente con rol "colaborador"

### Personalizar el Script

Si quieres cambiar el email o nombre, edita estas líneas en el script:

```python
email = 'paco@example.com'  # Cambia esto
password = '12345678'
nombre_completo = 'paco'  # Cambia esto
```

## 📋 Método 3: Crear Usuario y Perfil Manualmente con SQL

Si los métodos anteriores no funcionan, puedes crear el usuario y perfil directamente con SQL:

### Paso 1: Crear el Usuario (desde Dashboard)

1. Ve a **Authentication** → **Users** → **Add user**
2. Crea el usuario con:
   - Email: `paco@example.com`
   - Password: `12345678`
   - Auto Confirm: ✅ Marcado
3. **Copia el UUID** del usuario que se creó

### Paso 2: Crear el Perfil (SQL)

1. Ve a **SQL Editor** en Supabase
2. Ejecuta este SQL (reemplaza `USUARIO_UUID` con el UUID que copiaste):

```sql
-- Crear perfil para el usuario "paco"
INSERT INTO public.perfiles_usuarios (id, nombre_completo, rol)
VALUES (
    'USUARIO_UUID',  -- ⚠️ Reemplaza con el UUID del usuario
    'paco',
    'colaborador'
)
ON CONFLICT (id) DO NOTHING;
```

### Paso 3: Verificar

```sql
-- Verificar que el perfil se creó
SELECT * FROM public.perfiles_usuarios 
WHERE nombre_completo = 'paco';
```

## ✅ Verificar que Funciona

1. Ve a tu aplicación: https://comediacortesana.github.io/comedia_cortesana/
2. Haz clic en "Iniciar sesión"
3. Ingresa:
   - **Email:** `paco@example.com` (o el email que usaste)
   - **Contraseña:** `12345678`
4. Deberías poder iniciar sesión correctamente

## 🔧 Troubleshooting

### El usuario no puede iniciar sesión

1. **Verifica que el email esté confirmado:**
   - Ve a **Authentication** → **Users**
   - Busca el usuario
   - Verifica que tenga un check verde en "Confirmed"

2. **Si no está confirmado:**
   - Haz clic en el usuario
   - Busca el botón **"Confirm email"** o **"Send confirmation email"**

### El perfil no se creó automáticamente

1. **Verifica que el trigger esté activo:**
   - Ve a **SQL Editor**
   - Ejecuta: `SELECT * FROM pg_trigger WHERE tgname = 'on_auth_user_created';`
   - Si no aparece, ejecuta el archivo `supabase_trigger_fix.sql`

2. **Crea el perfil manualmente:**
   - Usa el Método 3 para crear el perfil con SQL

### Error: "User already exists"

- El usuario ya existe con ese email
- Puedes:
  - Usar otro email
  - O eliminar el usuario existente y crearlo de nuevo

## 📝 Notas Importantes

1. **Service Role Key:** Mantén esta key segura, nunca la compartas ni la subas a GitHub
2. **Contraseñas:** En producción, usa contraseñas más seguras
3. **Emails:** Asegúrate de usar un email válido si quieres recibir notificaciones
4. **Perfiles:** El trigger debería crear el perfil automáticamente, pero si no funciona, créalo manualmente

## 🎯 Crear Usuario "paco" Rápido

**Opción más rápida:**

1. Ve a Supabase → **Authentication** → **Users** → **Add user**
2. Email: `paco@example.com`
3. Password: `12345678`
4. ✅ Marca **"Auto Confirm User"**
5. Haz clic en **"Create user"**
6. Verifica en **Table Editor** → **perfiles_usuarios** que se creó el perfil

¡Listo! Ya puedes iniciar sesión con ese usuario.
