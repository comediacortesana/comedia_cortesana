# 📤 Subir Archivos de Síntesis a Supabase Storage

## ✅ Bucket Creado

El bucket `sintesis` ya está creado en Supabase Storage.

## 📋 Pasos para Subir Archivos

### Paso 1: Obtener Service Role Key

1. Ve a **Supabase Dashboard** → **Settings** → **API**
2. Busca la sección **"Project API keys"**
3. Copia la **"service_role"** key (⚠️ es secreta, no la anon key)
4. Se ve algo como: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

### Paso 2: Instalar Dependencia

```bash
pip install supabase
```

### Paso 3: Configurar la Key

**Opción A: Variable de entorno (recomendado)**
```bash
export SUPABASE_SERVICE_ROLE_KEY='tu-service-role-key-aqui'
```

**Opción B: Crear archivo .env**
```bash
# Crear archivo .env en la raíz del proyecto
echo "SUPABASE_SERVICE_ROLE_KEY=tu-service-role-key-aqui" >> .env
```

### Paso 4: Subir Archivos

**Subir todos los archivos de síntesis:**
```bash
cd /Users/ivansimo/Documents/2025/ITEM/DELIA_DJANGO
python data/fuentesix/subir_sintesis_supabase.py
```

**Subir un archivo específico:**
```bash
python data/fuentesix/subir_sintesis_supabase.py \
    data/fuentesix/extraccion_part_001_con_metadata_con_referencias_paginas_sintesis_validacion.json
```

## ✅ Verificar

1. Ve a **Supabase Dashboard** → **Storage** → **Bucket `sintesis`**
2. Deberías ver los archivos subidos
3. Abre `index.html` en el navegador
4. Inicia sesión
5. Haz clic en **"🤖 Validación IA"**
6. Deberías ver los análisis listos para validar

## 🔧 Solución de Problemas

### Error: "Necesitas configurar SUPABASE_SERVICE_ROLE_KEY"
- Verifica que exportaste la variable: `echo $SUPABASE_SERVICE_ROLE_KEY`
- O configúrala de nuevo: `export SUPABASE_SERVICE_ROLE_KEY='tu-key'`

### Error: "ModuleNotFoundError: No module named 'supabase'"
- Instala la librería: `pip install supabase`

### Error: "Bucket not found"
- Verifica que el bucket `sintesis` existe en Storage
- Verifica que el nombre es exactamente `sintesis` (sin espacios)

### Error de permisos
- Asegúrate de usar la **service_role** key, no la anon key
- La service_role key tiene permisos completos






