# 📋 Instrucciones Completas: Sistema de Validación IA

## ✅ Paso 1: Ejecutar SQL en Supabase (YA HECHO)

✅ Ya ejecutaste el SQL en Supabase. La tabla `validaciones_analisis` está creada.

## 📦 Paso 2: Crear Bucket en Supabase Storage

### Método Rápido (Dashboard):

1. Ve a https://supabase.com/dashboard
2. Selecciona tu proyecto
3. En el menú lateral: **Storage**
4. Clic en **"New bucket"** o **"Create bucket"**
5. Nombre: `sintesis`
6. **Public bucket**: ❌ NO (dejar desmarcado)
7. Clic en **"Create bucket"**

**¡Listo!** El bucket está creado.

### Verificar:
- Ve a Storage → Buckets
- Deberías ver `sintesis` en la lista

## 📤 Paso 3: Subir Archivos de Síntesis

### Opción A: Usando el Script Python (Recomendado)

1. **Instalar dependencia**:
   ```bash
   pip install supabase
   ```

2. **Configurar Service Role Key**:
   ```bash
   # Obtener la key desde: Supabase Dashboard → Settings → API → service_role key
   export SUPABASE_SERVICE_ROLE_KEY='tu-service-role-key-aqui'
   ```

3. **Subir archivos**:
   ```bash
   # Subir todos los archivos de síntesis del directorio
   python data/fuentesix/subir_sintesis_supabase.py
   
   # O subir un archivo específico
   python data/fuentesix/subir_sintesis_supabase.py data/fuentesix/extraccion_part_001_con_metadata_con_referencias_paginas_sintesis_validacion.json
   ```

### Opción B: Manualmente desde Dashboard

1. Ve a Supabase Dashboard → Storage → Bucket `sintesis`
2. Clic en **"Upload file"**
3. Selecciona el archivo `*_sintesis_validacion.json`
4. Clic en **"Upload"**

## ✅ Paso 4: Verificar Integración en index.html

El código ya está integrado en `index.html`. Verifica:

1. **Botón "🤖 Validación IA"** aparece junto a "💬 Comentarios"
2. Al hacer clic, se abre el modal con análisis
3. Puedes validar/rechazar análisis

## 🧪 Probar el Sistema

1. **Generar síntesis** (si aún no lo has hecho):
   ```bash
   python data/fuentesix/generar_sintesis_validacion.py \
       "data/fuentesix/extraccion_part_001_con_metadata_con_referencias_paginas.json"
   ```

2. **Subir síntesis a Supabase**:
   ```bash
   export SUPABASE_SERVICE_ROLE_KEY='tu-key'
   python data/fuentesix/subir_sintesis_supabase.py
   ```

3. **Abrir index.html** en el navegador
4. **Iniciar sesión**
5. **Clic en "🤖 Validación IA"**
6. **Ver análisis y validar/rechazar**

## 🎯 Resumen de Archivos

- ✅ `supabase_validacion_ia.sql` - SQL ejecutado
- ✅ `index.html` - Código integrado
- 📦 Crear bucket `sintesis` manualmente
- 📤 Subir archivos con script o manualmente

## 🔑 Obtener Service Role Key

1. Ve a Supabase Dashboard
2. Settings → API
3. Busca **"service_role"** key (es secreta, no la anon key)
4. Cópiala y úsala en el script






