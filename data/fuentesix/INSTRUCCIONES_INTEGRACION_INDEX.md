# Instrucciones: Integrar Validación IA en index.html

## 📋 Pasos para Integrar

### 1. Preparar Supabase

Ejecuta el script SQL en Supabase:
```bash
# Ejecutar en Supabase SQL Editor
data/fuentesix/supabase_validacion_ia.sql
```

Esto crea:
- Tabla `validaciones_analisis`
- Bucket `sintesis` en Storage (crear manualmente desde Dashboard)

### 2. Subir Archivos de Síntesis a Supabase Storage

```bash
# Desde el código Python o manualmente desde Dashboard
# Subir archivos *_sintesis_validacion.json al bucket 'sintesis'
```

### 3. Integrar Código en index.html

El archivo `validacion_ia_index.html` contiene todo el código necesario:

#### 3.1. Añadir Estilos CSS
- Copiar la sección `<style>` de `validacion_ia_index.html`
- Pegar después de los estilos de comentarios (alrededor de línea 370)

#### 3.2. Añadir Botón en Barra Superior
- Buscar el botón de comentarios (alrededor de línea 503)
- Añadir el botón de "Validación IA" justo después

#### 3.3. Añadir Modal
- Buscar el modal de comentarios (alrededor de línea 650)
- Añadir el modal de validación IA justo después

#### 3.4. Añadir Funciones JavaScript
- Buscar las funciones de comentarios (alrededor de línea 2305)
- Añadir todas las funciones de validación IA después

### 4. Actualizar window.onload

En la función `window.onload` (alrededor de línea 4984), añadir:

```javascript
// Actualizar contador de análisis pendientes
setTimeout(() => {
    actualizarContadorAnalisisPendientes();
}, 2000);
```

## ✅ Verificación

1. **Cargar página**: Deberías ver el botón "🤖 Validación IA"
2. **Hacer clic**: Debería abrir el modal con análisis pendientes
3. **Validar**: Probar validar/rechazar un análisis
4. **Verificar DB**: Comprobar que se guardó en `validaciones_analisis`

## 🎨 Características

- **Similar a comentarios**: Mismo estilo y estructura
- **Distintivo IA**: Badge morado (#9b59b6) para identificar análisis de IA
- **Estados visuales**: Verde (validado), Rojo (rechazado), Morado (pendiente)
- **Referencias PDF**: Enlaces directos a páginas del PDF original
- **Contador**: Muestra número de análisis pendientes

## 📝 Notas

- Los archivos de síntesis deben estar en Supabase Storage bucket `sintesis`
- Los usuarios deben estar autenticados para validar
- Las validaciones se guardan en la tabla `validaciones_analisis`
- El contador se actualiza automáticamente cada 2 segundos después de cargar






