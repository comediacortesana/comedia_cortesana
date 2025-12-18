# 🔐 Cómo Activar el Sistema de Creación de Usuarios en Supabase

## 🎯 Objetivo

Activar el sistema de confirmación de email para que los usuarios reciban un mensaje de activación cuando se registren en la aplicación.

## 📋 Pasos para Activar

### Paso 1: Acceder a la Configuración de Autenticación

1. Ve a tu proyecto en Supabase: https://supabase.com/dashboard
2. Selecciona tu proyecto
3. En el menú lateral izquierdo, ve a **Authentication**
4. Haz clic en **Settings** (o **Configuración**)

### Paso 2: Habilitar Confirmación de Email

1. En la sección **"Email Auth"** o **"Email Authentication"**
2. Busca la opción **"Enable email confirmations"** o **"Confirm email"**
3. **Activa** esta opción (debe estar marcada/enabled)
4. Haz clic en **Save** (Guardar)

### Paso 3: Configurar la Plantilla de Email de Confirmación

1. En el mismo menú de **Authentication**, ve a **Email Templates** (Plantillas de Email)
2. Selecciona la plantilla **"Confirm signup"** (Confirmar registro)
3. Abre el archivo `email_activacion_usuario.html` de este proyecto
4. Copia todo el contenido HTML
5. Pégalo en la plantilla de Supabase
6. Haz clic en **Save** (Guardar)

**Nota:** Las variables `{% raw %}{{ .ConfirmationURL }}{% endraw %}` son automáticamente reemplazadas por Supabase con la URL real de confirmación.

### Paso 4: Configurar URLs de Redirección

1. En **Authentication** → **URL Configuration**
2. Configura las siguientes URLs:

   **Site URL:**
   ```
   https://comediacortesana.github.io/comedia_cortesana/
   ```

   **Redirect URLs** (añade todas estas):
   ```
   https://comediacortesana.github.io/comedia_cortesana/**
   http://localhost:5500/**
   http://127.0.0.1:5500/**
   http://localhost:8000/**
   ```

3. Haz clic en **Save**

### Paso 5: Configurar Servicio de Email (Opcional pero Recomendado)

#### Opción A: Usar el Servicio de Supabase (Limitado)

- **Ventaja:** No requiere configuración adicional
- **Desventaja:** Solo 3 emails por hora en el plan gratuito
- **Uso:** Ideal para desarrollo o proyectos pequeños

No necesitas hacer nada adicional, ya está activado por defecto.

#### Opción B: Configurar SMTP Personalizado (Recomendado para Producción)

1. Ve a **Project Settings** → **Auth** → **SMTP Settings**
2. Activa **"Enable Custom SMTP"**
3. Configura según tu proveedor:

   **Para Gmail:**
   - SMTP Host: `smtp.gmail.com`
   - SMTP Port: `587`
   - SMTP User: `tu-email@gmail.com`
   - SMTP Password: (usa una contraseña de aplicación de Google)
   - From email: `tu-email@gmail.com`
   - From name: `Teatro Español del Siglo de Oro`

   **Para SendGrid:**
   - SMTP Host: `smtp.sendgrid.net`
   - SMTP Port: `587`
   - SMTP User: `apikey`
   - SMTP Password: (tu API key de SendGrid)
   - From email: `noreply@tudominio.com`

4. Haz clic en **Save**
5. Prueba el envío con el botón **"Send test email"**

## ✅ Verificar que Está Funcionando

### Prueba Rápida

1. Ve a tu aplicación: https://comediacortesana.github.io/comedia_cortesana/
2. Intenta registrarte con un email de prueba
3. Revisa tu bandeja de entrada (y spam)
4. Deberías recibir un email con el diseño personalizado
5. Haz clic en el botón de confirmación
6. Deberías ser redirigido a la aplicación y poder iniciar sesión

### Verificar en Supabase

1. Ve a **Authentication** → **Users**
2. Busca el usuario que acabas de crear
3. Verifica que el estado sea:
   - **"Unconfirmed"** antes de confirmar el email
   - **"Confirmed"** después de hacer clic en el enlace

## 🔧 Troubleshooting

### Los emails no llegan

1. **Revisa la carpeta de spam/correo no deseado**
2. **Verifica que el email esté correcto** (sin typos)
3. **Revisa los logs de Supabase:**
   - Ve a **Logs** → **Auth Logs**
   - Busca errores relacionados con email
4. **Verifica el límite de emails:**
   - En el plan gratuito solo puedes enviar 3 emails por hora
   - Si excedes el límite, espera 1 hora o configura SMTP personalizado

### Error: "Email rate limit exceeded"

- **Causa:** Has excedido el límite de 3 emails por hora del plan gratuito
- **Solución:** 
  - Espera 1 hora
  - O configura SMTP personalizado (Opción B del Paso 5)

### El usuario puede iniciar sesión sin confirmar

- **Causa:** La confirmación de email está deshabilitada
- **Solución:** Sigue el Paso 2 para habilitarla

### El enlace de confirmación no funciona

- **Causa:** Las URLs de redirección no están configuradas correctamente
- **Solución:** Verifica el Paso 4 y asegúrate de que todas las URLs estén añadidas

### El diseño del email no se ve bien

- **Causa:** Algunos clientes de email no soportan ciertos estilos CSS
- **Solución:** El HTML está diseñado con estilos inline para máxima compatibilidad. Si necesitas ajustes, edita `email_activacion_usuario.html`

## 📝 Notas Importantes

1. **Variables de Supabase:** El HTML usa `{% raw %}{{ .ConfirmationURL }}{% endraw %}` que Supabase reemplaza automáticamente. No cambies esta variable.

2. **Estilo:** El email está diseñado para coincidir con el estilo académico y elegante de la aplicación, usando los mismos colores y fuentes.

3. **Responsive:** El diseño es responsive y se adapta a dispositivos móviles.

4. **Seguridad:** Los usuarios solo pueden usar la aplicación después de confirmar su email, lo que ayuda a prevenir registros falsos.

## 🎨 Personalizar el Email

Si quieres modificar el diseño del email:

1. Edita el archivo `email_activacion_usuario.html`
2. Mantén las variables de Supabase (`{% raw %}{{ .ConfirmationURL }}{% endraw %}`, etc.)
3. Copia el contenido actualizado a Supabase → Email Templates → Confirm signup
4. Guarda los cambios

## 📚 Referencias

- [Documentación de Supabase - Email Auth](https://supabase.com/docs/guides/auth/auth-email)
- [Documentación de Supabase - Email Templates](https://supabase.com/docs/guides/auth/auth-email-templates)
- [Configurar SMTP en Supabase](https://supabase.com/docs/guides/auth/auth-smtp)
