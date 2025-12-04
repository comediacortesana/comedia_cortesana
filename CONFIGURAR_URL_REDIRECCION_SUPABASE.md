# 🔧 Configurar URL de Redirección en Supabase

## Problema

Cuando confirmas tu cuenta por email, Supabase te redirige a `localhost:3000` pero tu aplicación está en GitHub Pages.

## Solución

### Paso 1: Ir a Configuración de Supabase

1. Ve a tu proyecto en Supabase: https://supabase.com/dashboard
2. Ve a **Authentication** → **URL Configuration** (o **Settings** → **Auth** → **URL Configuration`)

### Paso 2: Configurar URLs de Redirección

En la sección **"Redirect URLs"**, agrega estas URLs:

#### URLs de Producción (GitHub Pages):
```
https://comediacortesana.github.io/comedia_cortesana/
https://comediacortesana.github.io/comedia_cortesana/index.html
```

#### URLs de Desarrollo (Local):
```
http://localhost:8000/
http://localhost:8000/index.html
http://localhost:3000/
http://localhost:3000/index.html
```

#### URL con Wildcard (si quieres permitir cualquier ruta):
```
https://comediacortesana.github.io/comedia_cortesana/**
```

### Paso 3: Configurar Site URL

En **"Site URL"**, pon tu URL de producción:
```
https://comediacortesana.github.io/comedia_cortesana/
```

### Paso 4: Guardar

Click en **"Save"** y espera unos segundos para que se apliquen los cambios.

## ✅ Verificación

Después de configurar:

1. Intenta registrarte con un nuevo email
2. Confirma el email desde tu correo
3. Deberías ser redirigido a GitHub Pages (no a localhost)
4. La sesión se establecerá automáticamente

## 🔍 Troubleshooting

### Si sigue redirigiendo a localhost:

1. Verifica que guardaste los cambios en Supabase
2. Espera 1-2 minutos (puede haber caché)
3. Intenta con un nuevo email de registro
4. Revisa la consola del navegador para ver errores

### Si el hash no se procesa:

1. Abre la consola del navegador (F12)
2. Busca mensajes que empiecen con "🔍 Hash detectado" o "🔑 Token de acceso"
3. Si no aparecen, el código de procesamiento puede no estar ejecutándose

## 📝 Nota

El código en `index.html` ahora procesa automáticamente los tokens del hash de la URL, así que una vez que configures las URLs de redirección en Supabase, todo debería funcionar automáticamente.

