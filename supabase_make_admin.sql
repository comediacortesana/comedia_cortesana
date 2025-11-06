-- ============================================================================
-- HACER ADMIN AL USUARIO isimo@ucm.es
-- ============================================================================
-- Ejecuta este SQL en Supabase SQL Editor

-- Primero, necesitas el UUID del usuario
-- Ve a Authentication > Users y copia el UUID de isimo@ucm.es
-- Luego ejecuta esto (reemplaza el UUID):

UPDATE perfiles_usuarios
SET rol = 'admin'
WHERE id = '8a9a2143-5188-4dd1-9c0a-93cd48560c3d';  -- ⚠️ Reemplaza con el UUID real si es diferente

-- Verificar que se actualizó
SELECT id, nombre_completo, rol 
FROM perfiles_usuarios 
WHERE id = '8a9a2143-5188-4dd1-9c0a-93cd48560c3d';

-- ============================================================================
-- POLÍTICA RLS PARA QUE ADMINS PUEDAN EDITAR ROLES
-- ============================================================================
-- Esta política ya debería estar en supabase_schema.sql, pero por si acaso:

DROP POLICY IF EXISTS "perfiles_admin_editar" ON perfiles_usuarios;
CREATE POLICY "perfiles_admin_editar"
ON perfiles_usuarios FOR UPDATE
USING (
    EXISTS (
        SELECT 1 FROM perfiles_usuarios
        WHERE id = auth.uid() AND rol = 'admin'
    )
)
WITH CHECK (
    EXISTS (
        SELECT 1 FROM perfiles_usuarios
        WHERE id = auth.uid() AND rol = 'admin'
    )
);

