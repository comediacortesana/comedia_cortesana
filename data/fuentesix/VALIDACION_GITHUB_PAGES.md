# Sistema de Validación para GitHub Pages

## ⚠️ Limitación Actual

El sistema de validación actual (`views_validacion.py`) **NO funcionará en GitHub Pages** porque:

- ❌ GitHub Pages solo sirve archivos estáticos (HTML, CSS, JS)
- ❌ Requiere Django backend (vistas, autenticación, procesamiento)
- ❌ Necesita acceso al sistema de archivos del servidor

## ✅ Soluciones Posibles

### Opción 1: Versión Estática con Supabase (Recomendada)

Crear una versión estática que use Supabase directamente:

**Ventajas:**
- ✅ Funciona en GitHub Pages
- ✅ Usa tu backend Supabase existente
- ✅ Autenticación con Supabase Auth
- ✅ Almacenamiento de validaciones en Supabase

**Implementación:**
1. Crear archivos HTML/JS estáticos
2. Usar Supabase JS client para:
   - Autenticación
   - Leer archivos JSON de síntesis (desde Supabase Storage)
   - Guardar validaciones en tabla Supabase
   - Integrar datos validados a la DB

### Opción 2: Desplegar Django en Servidor

Desplegar la aplicación Django completa:

**Opciones de hosting:**
- Railway.app (gratis con límites)
- Render.com (gratis con límites)
- Heroku (de pago)
- DigitalOcean App Platform

**Ventajas:**
- ✅ Funciona exactamente como está
- ✅ Acceso completo a Django

**Desventajas:**
- ❌ Requiere servidor (puede tener costos)
- ❌ Más complejo de mantener

### Opción 3: Híbrido

- GitHub Pages: Frontend estático
- Supabase: Backend y base de datos
- GitHub Actions: Generar síntesis y subir a Supabase Storage

## 🚀 Implementación Recomendada: Versión Estática

### Estructura Propuesta

```
github-pages/
├── index.html                    # Lista de archivos de síntesis
├── validacion.html              # Vista de validación detallada
├── js/
│   ├── supabase-client.js       # Cliente Supabase
│   ├── validacion.js            # Lógica de validación
│   └── integracion.js           # Integración a DB
└── css/
    └── validacion.css           # Estilos
```

### Flujo de Trabajo

1. **Generar síntesis** (local o GitHub Actions):
   ```bash
   python generar_sintesis_validacion.py ...
   ```

2. **Subir a Supabase Storage**:
   - Archivos `*_sintesis_validacion.json` → Supabase Storage bucket `sintesis`

3. **Frontend estático** (GitHub Pages):
   - Lista archivos desde Supabase Storage
   - Muestra síntesis para validar
   - Guarda validaciones en tabla Supabase `validaciones_analisis`

4. **Integración automática**:
   - Función Supabase Edge Function o trigger
   - Cuando se valida → integra a tablas principales

### Tabla Supabase Necesaria

```sql
CREATE TABLE validaciones_analisis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    archivo_sintesis TEXT NOT NULL,
    tipo_registro TEXT NOT NULL, -- 'representacion', 'obra', 'lugar'
    id_temporal TEXT NOT NULL,
    estado TEXT NOT NULL, -- 'validado', 'rechazado'
    usuario_id UUID REFERENCES auth.users(id),
    comentario TEXT,
    datos_json JSONB,
    fecha_validacion TIMESTAMPTZ DEFAULT NOW(),
    integrado BOOLEAN DEFAULT FALSE,
    id_integrado INTEGER -- ID del registro creado en la DB
);
```

## 📝 Próximos Pasos

1. **Crear versión estática** del sistema de validación
2. **Configurar Supabase Storage** para archivos de síntesis
3. **Crear tabla de validaciones** en Supabase
4. **Implementar integración automática** con Edge Functions

¿Quieres que implemente la versión estática para GitHub Pages?






