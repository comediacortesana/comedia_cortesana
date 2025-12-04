# 📧 Configurar Email en Supabase

## 🔍 Problema: No llegan emails de confirmación

Si los usuarios se registran pero no reciben el email de confirmación, puede ser porque:

1. **La confirmación de email está deshabilitada** (más común)
2. **El servicio de email no está configurado** en Supabase
3. **Los emails van a spam**

## ✅ Solución 1: Deshabilitar confirmación de email (Recomendado para desarrollo)

Si no necesitas confirmación de email (útil para desarrollo o proyectos internos):

1. Ve a tu proyecto en Supabase: https://supabase.com/dashboard
2. Abre **Authentication** → **Settings** (o **Configuración**)
3. Busca la sección **"Email Auth"** o **"Email Authentication"**
4. Desactiva **"Enable email confirmations"** o **"Confirm email"**
5. Guarda los cambios

**Ventajas:**
- Los usuarios pueden usar la app inmediatamente después de registrarse
- No necesitas configurar un servicio de email
- Ideal para desarrollo y pruebas

**Desventajas:**
- Cualquiera puede registrarse con cualquier email (sin verificar)

## ✅ Solución 2: Configurar servicio de email (Para producción)

Si quieres confirmación de email en producción:

### Opción A: Usar el servicio de email de Supabase (limitado)

1. Ve a **Authentication** → **Email Templates**
2. Configura las plantillas de email
3. Los emails se enviarán desde `noreply@mail.app.supabase.io`
4. **Limitación:** Solo 3 emails por hora en el plan gratuito

### Opción B: Configurar SMTP personalizado (Recomendado)

1. Ve a **Project Settings** → **Auth** → **SMTP Settings**
2. Configura tu proveedor de email:
   - **Gmail:** smtp.gmail.com (puerto 587)
   - **SendGrid:** smtp.sendgrid.net
   - **Mailgun:** smtp.mailgun.org
   - **Otro:** Configura según tu proveedor

3. Ingresa las credenciales:
   - SMTP Host
   - SMTP Port
   - SMTP User
   - SMTP Password
   - From email (remitente)

4. Guarda y prueba

## 🔧 Verificar configuración actual

Para verificar si la confirmación está habilitada:

1. Ve a **Authentication** → **Settings**
2. Busca **"Enable email confirmations"**
3. Si está desactivado, los usuarios pueden iniciar sesión sin confirmar

## 📝 Código para reenviar confirmación

Ya está implementado en `index.html`:

```javascript
// Reenviar email de confirmación
await reenviarConfirmacionEmail('usuario@ejemplo.com');
```

O desde la UI, hay un botón "📧 Reenviar confirmación" en el formulario de login.

## 🚨 Troubleshooting

### Los emails no llegan

1. **Revisa spam/correo no deseado**
2. **Verifica que el email esté correcto** (sin typos)
3. **Revisa los logs de Supabase:**
   - Ve a **Logs** → **Auth Logs**
   - Busca errores relacionados con email

### Error: "Email rate limit exceeded"

- En el plan gratuito de Supabase solo puedes enviar 3 emails por hora
- Solución: Configura SMTP personalizado o espera 1 hora

### El usuario puede iniciar sesión sin confirmar

- Esto significa que la confirmación está deshabilitada
- Si quieres habilitarla, sigue la Solución 2

## 💡 Recomendación

Para desarrollo y proyectos internos:
- ✅ **Deshabilita** la confirmación de email
- ✅ Los usuarios pueden usar la app inmediatamente

Para producción pública:
- ✅ **Habilita** la confirmación de email
- ✅ Configura SMTP personalizado
- ✅ Añade validación adicional si es necesario

