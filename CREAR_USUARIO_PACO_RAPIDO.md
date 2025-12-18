# 👤 Crear Usuario "paco" Rápido

## 🚀 Método Más Rápido: Desde Supabase Dashboard

### Paso 1: Ir a Users
1. Ve a https://supabase.com/dashboard
2. Selecciona tu proyecto
3. Ve a **Authentication** → **Users** (menú lateral izquierdo)

### Paso 2: Crear Usuario
1. Haz clic en el botón **"Add user"** o **"Invite user"** (arriba a la derecha)
2. Si ves **"Add user"**, úsalo directamente:
   - **Email:** `paco@example.com` (o el email que quieras)
   - **Password:** `12345678`
   - ✅ **Marca "Auto Confirm User"** (importante: esto permite iniciar sesión inmediatamente)
   - Haz clic en **"Create user"**

3. Si solo ves **"Invite user"**:
   - **Email:** `paco@example.com`
   - ✅ **Marca "Auto Confirm"**
   - Haz clic en **"Send invitation"**
   - El usuario recibirá un email para establecer su contraseña
   - **Nota:** Tendrás que establecer la contraseña desde el email o usar el método alternativo

### Paso 3: Verificar Perfil
1. Ve a **Table Editor** → **perfiles_usuarios**
2. Busca el usuario recién creado
3. Si no aparece el perfil, ve al **Paso 4**

### Paso 4: Crear Perfil Manualmente (si es necesario)
1. Ve a **SQL Editor** en Supabase
2. Primero, obtén el UUID del usuario:
   - Ve a **Authentication** → **Users**
   - Haz clic en el usuario "paco"
   - Copia el **UUID** (es un string largo como `a1b2c3d4-e5f6-7890-abcd-ef1234567890`)

3. Ejecuta este SQL (reemplaza `USUARIO_UUID` con el UUID que copiaste):

```sql
INSERT INTO public.perfiles_usuarios (id, nombre_completo, rol)
VALUES (
    'USUARIO_UUID',  -- ⚠️ Pega aquí el UUID del usuario
    'paco',
    'colaborador'
)
ON CONFLICT (id) DO NOTHING;
```

### Paso 5: Probar Login
1. Ve a tu aplicación
2. Haz clic en "Iniciar sesión"
3. Ingresa:
   - **Email:** `paco@example.com`
   - **Contraseña:** `12345678`
4. Deberías poder iniciar sesión

---

## 🔧 Método Alternativo: Usar Script Python

Si prefieres usar el script automatizado:

### Instalar dependencias:
```bash
pip3 install requests
```

### Configurar Service Role Key:
```bash
export SUPABASE_SERVICE_ROLE_KEY='tu-service-role-key'
```

Para obtener la Service Role Key:
1. Ve a Supabase → **Settings** → **API**
2. Copia la **"service_role"** key (NO la "anon" key)

### Ejecutar script:
```bash
cd /Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO
python3 scripts/crear_usuario_supabase.py
```

---

## ⚠️ Si el Usuario No Puede Iniciar Sesión

1. **Verifica que el email esté confirmado:**
   - Ve a **Authentication** → **Users**
   - Busca el usuario "paco"
   - Debe tener un check verde en "Confirmed"
   - Si no, haz clic en el usuario y busca **"Confirm email"**

2. **Verifica la contraseña:**
   - Si usaste "Invite user", el usuario debe establecer la contraseña desde el email
   - O puedes cambiar la contraseña desde **Authentication** → **Users** → Click en el usuario → **"Reset password"**

---

## 📝 Notas

- El email puede ser cualquier email válido (no tiene que existir realmente)
- La contraseña debe tener al menos 6 caracteres
- Si el trigger está activo, el perfil se crea automáticamente
- Si no se crea el perfil, créalo manualmente con SQL
