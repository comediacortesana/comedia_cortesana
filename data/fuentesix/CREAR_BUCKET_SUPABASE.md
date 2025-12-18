# 📦 Crear Bucket en Supabase Storage

## Pasos para crear el bucket "sintesis"

### Opción 1: Desde el Dashboard de Supabase (Recomendado)

1. **Accede a tu proyecto Supabase**
   - Ve a https://supabase.com/dashboard
   - Selecciona tu proyecto

2. **Ve a Storage**
   - En el menú lateral izquierdo, haz clic en **"Storage"**

3. **Crear nuevo bucket**
   - Haz clic en el botón **"New bucket"** o **"Create bucket"**
   - Nombre del bucket: `sintesis`
   - **Public bucket**: ❌ **NO** (dejar desmarcado - bucket privado)
   - Haz clic en **"Create bucket"**

4. **Configurar políticas (opcional)**
   - Ve a **"Policies"** del bucket `sintesis`
   - Añade política para lectura pública:
     ```sql
     -- Política: Todos pueden leer archivos de síntesis
     CREATE POLICY "Todos pueden leer síntesis"
     ON storage.objects
     FOR SELECT
     USING (bucket_id = 'sintesis');
     ```
   - Añade política para que admins puedan subir:
     ```sql
     -- Política: Admins pueden subir síntesis
     CREATE POLICY "Admins pueden subir síntesis"
     ON storage.objects
     FOR INSERT
     WITH CHECK (
         bucket_id = 'sintesis' AND
         auth.uid() IN (
             SELECT id FROM auth.users WHERE id IN (
                 SELECT usuario_id FROM perfiles_usuarios WHERE rol = 'admin'
             )
         )
     );
     ```

### Opción 2: Usando SQL

Ejecuta en el SQL Editor de Supabase:

```sql
-- Crear bucket 'sintesis'
INSERT INTO storage.buckets (id, name, public)
VALUES ('sintesis', 'sintesis', false)
ON CONFLICT (id) DO NOTHING;

-- Política de lectura pública
CREATE POLICY "Todos pueden leer síntesis"
ON storage.objects
FOR SELECT
USING (bucket_id = 'sintesis');

-- Política de inserción para admins
CREATE POLICY "Admins pueden subir síntesis"
ON storage.objects
FOR INSERT
WITH CHECK (
    bucket_id = 'sintesis' AND
    auth.uid() IN (
        SELECT id FROM auth.users WHERE id IN (
            SELECT usuario_id FROM perfiles_usuarios WHERE rol = 'admin'
        )
    )
);
```

## ✅ Verificación

Después de crear el bucket:
1. Ve a Storage → Buckets
2. Deberías ver el bucket `sintesis` en la lista
3. Haz clic en él para ver su contenido (estará vacío hasta que subas archivos)






