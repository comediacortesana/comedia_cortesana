# 📧 Guía Rápida: Configurar Email de Activación

## 🎯 Pasos Exactos (Basado en tu Pantalla Actual)

### Paso 1: Haz clic en "Confirm sign up"
En la pantalla que estás viendo ahora, en la lista de opciones bajo "Authentication", haz clic en la primera opción que dice:

**"Confirm sign up"** → "Ask users to confirm their email address after signing up."

### Paso 2: Se abrirá el editor de plantilla
Al hacer clic, se abrirá un editor con dos pestañas:
- **Subject** (Asunto del email)
- **Body** (Cuerpo del email - aquí va el HTML)

### Paso 3: Configurar el Asunto (Subject)
En la pestaña **Subject**, escribe:
```
Confirma tu registro - Teatro Español del Siglo de Oro
```

### Paso 4: Configurar el Cuerpo (Body)
1. Ve a la pestaña **Body**
2. Asegúrate de que esté seleccionado **"HTML"** (no "Plain text")
3. Abre el archivo `email_activacion_usuario.html` de este proyecto
4. **Copia TODO el contenido** del archivo (desde `<!DOCTYPE html>` hasta `</html>`)
5. **Pega** el contenido en el editor de Supabase
6. Haz clic en **"Save"** (Guardar)

### Paso 5: Activar la Confirmación de Email
1. Ve a la pestaña **"SMTP Settings"** (al lado de "Templates")
2. O ve a **Authentication** → **Settings** (Configuración)
3. Busca la opción **"Enable email confirmations"** o **"Confirm email"**
4. **Actívala** (debe estar marcada/enabled)
5. Guarda los cambios

## 📋 Contenido a Copiar

El contenido completo está en el archivo `email_activacion_usuario.html`. Solo necesitas copiarlo y pegarlo en Supabase.

**Importante:** NO cambies la variable `{% raw %}{{ .ConfirmationURL }}{% endraw %}` - Supabase la reemplazará automáticamente con el enlace real.

## ✅ Verificar que Funciona

1. Regístrate con un email de prueba en tu aplicación
2. Revisa tu bandeja de entrada (y spam)
3. Deberías recibir un email con el diseño personalizado
4. Haz clic en el botón "Confirmar mi cuenta"
5. Deberías ser redirigido a la aplicación

## 🚨 Si No Ves la Opción "Confirm sign up"

Si no aparece la opción "Confirm sign up" en la lista:

1. Ve a **Authentication** → **Settings** (Configuración)
2. Busca **"Enable email confirmations"**
3. Actívala primero
4. Luego vuelve a **Email** → **Templates**
5. Ahora debería aparecer "Confirm sign up"

## 📸 Ubicación Visual

```
Supabase Dashboard
└── Authentication (menú lateral izquierdo)
    └── Email (bajo NOTIFICATIONS) ← ESTÁS AQUÍ
        └── Templates (pestaña superior) ← ESTÁS AQUÍ
            └── Confirm sign up ← HAZ CLIC AQUÍ
```
