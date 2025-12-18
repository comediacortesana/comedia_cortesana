# 📧 Personalizar Plantillas de Email en Supabase

## 🎯 Objetivo

Personalizar los emails de confirmación de Supabase para que:
- Tengan un diseño más atractivo
- Redirijan a tu sitio web: https://comediacortesana.github.io/comedia_cortesana/
- Incluyan tu branding

## 📋 Paso 1: Acceder a las Plantillas de Email

1. Ve a tu proyecto en Supabase: https://supabase.com/dashboard
2. Abre **Authentication** → **Email Templates** (o **Plantillas de Email**)
3. Verás varias plantillas disponibles:
   - **Confirm signup** (Confirmar registro)
   - **Magic Link** (Enlace mágico)
   - **Change Email Address** (Cambiar email)
   - **Reset Password** (Restablecer contraseña)

## 📝 Paso 2: Personalizar la Plantilla "Confirm signup"

### Plantilla HTML Personalizada

Copia y pega este HTML en la plantilla "Confirm signup":

```html
<h2 style="color: #2c3e50; font-family: Arial, sans-serif;">
  🎭 Confirma tu registro en Teatro Español del Siglo de Oro
</h2>

<p style="color: #555; font-family: Arial, sans-serif; font-size: 16px;">
  ¡Hola!
</p>

<p style="color: #555; font-family: Arial, sans-serif; font-size: 16px;">
  Gracias por registrarte en nuestro sistema de filtrado de obras del teatro español del Siglo de Oro.
</p>

<p style="color: #555; font-family: Arial, sans-serif; font-size: 16px;">
  Para completar tu registro, haz clic en el siguiente enlace:
</p>

<div style="text-align: center; margin: 30px 0;">
  <a href="{{ .ConfirmationURL }}" 
     style="background-color: #3498db; 
            color: white; 
            padding: 12px 24px; 
            text-decoration: none; 
            border-radius: 5px; 
            display: inline-block;
            font-weight: bold;
            font-family: Arial, sans-serif;">
    ✅ Confirmar mi cuenta
  </a>
</div>

<p style="color: #555; font-family: Arial, sans-serif; font-size: 14px;">
  O copia y pega este enlace en tu navegador:
</p>

<p style="color: #3498db; font-family: monospace; font-size: 12px; word-break: break-all;">
  {% raw %}{{ .ConfirmationURL }}{% endraw %}
</p>

<hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">

<p style="color: #999; font-family: Arial, sans-serif; font-size: 12px;">
  Si no te registraste en este sitio, puedes ignorar este email de forma segura.
</p>

<p style="color: #999; font-family: Arial, sans-serif; font-size: 12px;">
  Este email fue enviado por <strong>Teatro Español del Siglo de Oro</strong><br>
  <a href="https://comediacortesana.github.io/comedia_cortesana/" style="color: #3498db;">
    https://comediacortesana.github.io/comedia_cortesana/
  </a>
</p>
```

### Plantilla de Texto Plano (Alternativa)

Si prefieres texto simple, usa esta versión:

```
🎭 Confirma tu registro en Teatro Español del Siglo de Oro

¡Hola!

Gracias por registrarte en nuestro sistema de filtrado de obras del teatro español del Siglo de Oro.

Para completar tu registro, visita este enlace:

{{ .ConfirmationURL }}

Si no te registraste en este sitio, puedes ignorar este email de forma segura.

---
Teatro Español del Siglo de Oro
https://comediacortesana.github.io/comedia_cortesana/
```

## 🔗 Paso 3: Configurar URL de Redirección

### En el código (ya está configurado)

El código en `index.html` ya está configurado para usar:
- **Producción:** `https://comediacortesana.github.io/comedia_cortesana/`
- **Desarrollo local:** URL local actual

### En Supabase Dashboard

1. Ve a **Authentication** → **URL Configuration**
2. En **Site URL**, pon: `https://comediacortesana.github.io/comedia_cortesana/`
3. En **Redirect URLs**, añade:
   - `https://comediacortesana.github.io/comedia_cortesana/**`
   - `http://localhost:5500/**` (para desarrollo local)
   - `http://127.0.0.1:5500/**` (para desarrollo local)

## 📝 Variables Disponibles en las Plantillas

Supabase proporciona estas variables que puedes usar:

- `{% raw %}{{ .ConfirmationURL }}{% endraw %}` - URL de confirmación completa
- `{% raw %}{{ .Token }}{% endraw %}` - Token de confirmación
- `{% raw %}{{ .TokenHash }}{% endraw %}` - Hash del token
- `{% raw %}{{ .SiteURL }}{% endraw %}` - URL de tu sitio
- `{% raw %}{{ .Email }}{% endraw %}` - Email del usuario
- `{% raw %}{{ .Data }}{% endraw %}` - Datos adicionales del usuario

## 🎨 Plantilla HTML Avanzada (Más Bonita)

Si quieres algo más elaborado:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
    .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
              color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }
    .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }
    .button { background-color: #3498db; color: white; padding: 12px 24px; 
              text-decoration: none; border-radius: 5px; display: inline-block; 
              margin: 20px 0; font-weight: bold; }
    .footer { text-align: center; color: #999; font-size: 12px; margin-top: 30px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1 style="margin: 0;">🎭 Teatro Español del Siglo de Oro</h1>
    </div>
    <div class="content">
      <h2 style="color: #2c3e50;">Confirma tu registro</h2>
      <p>¡Hola!</p>
      <p>Gracias por registrarte en nuestro sistema de filtrado de obras del teatro español del Siglo de Oro.</p>
      <p>Para completar tu registro, haz clic en el siguiente botón:</p>
      <div style="text-align: center;">
        <a href="{% raw %}{{ .ConfirmationURL }}{% endraw %}" class="button">
          ✅ Confirmar mi cuenta
        </a>
      </div>
      <p style="font-size: 12px; color: #666;">
        O copia este enlace: <br>
        <span style="word-break: break-all;">{% raw %}{{ .ConfirmationURL }}{% endraw %}</span>
      </p>
    </div>
    <div class="footer">
      <p>Si no te registraste, ignora este email.</p>
      <p>
        <a href="https://comediacortesana.github.io/comedia_cortesana/" 
           style="color: #3498db;">
          Teatro Español del Siglo de Oro
        </a>
      </p>
    </div>
  </div>
</body>
</html>
```

## ✅ Paso 4: Probar

1. Guarda los cambios en Supabase
2. Regístrate con un email de prueba
3. Revisa el email recibido
4. Verifica que el enlace redirija correctamente a tu sitio

## 🔧 Personalizar Otras Plantillas

Puedes personalizar también:
- **Magic Link** - Para login sin contraseña
- **Reset Password** - Para recuperar contraseña
- **Change Email** - Para cambiar email

Usa el mismo formato HTML y las mismas variables.

## 📚 Referencias

- [Documentación oficial de Supabase - Email Templates](https://supabase.com/docs/guides/auth/auth-email-templates)
- [Variables disponibles en plantillas](https://supabase.com/docs/guides/auth/auth-email-templates#available-variables)

