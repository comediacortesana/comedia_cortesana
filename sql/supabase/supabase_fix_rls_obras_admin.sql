-- ============================================================================
-- FIX: Políticas RLS para OBRAS - Permitir UPDATE/INSERT/DELETE solo a admins
-- ============================================================================
-- Ejecuta este SQL en Supabase SQL Editor para agregar políticas de seguridad
-- que permitan a los administradores modificar obras desde el frontend
-- mientras protegen contra modificaciones no autorizadas.

-- ============================================================================
-- POLÍTICA PARA UPDATE: Solo admins pueden actualizar obras
-- ============================================================================
DROP POLICY IF EXISTS "obras_update_admin" ON obras;
CREATE POLICY "obras_update_admin"
ON obras FOR UPDATE
USING (
    -- Verificar que el usuario está autenticado Y es admin
    EXISTS (
        SELECT 1 FROM perfiles_usuarios
        WHERE id = auth.uid() AND rol = 'admin'
    )
)
WITH CHECK (
    -- Verificar también en WITH CHECK para validar los datos nuevos
    EXISTS (
        SELECT 1 FROM perfiles_usuarios
        WHERE id = auth.uid() AND rol = 'admin'
    )
);

-- ============================================================================
-- POLÍTICA PARA INSERT: Solo admins pueden insertar obras
-- ============================================================================
-- Descomenta esto si necesitas que los admins puedan crear obras desde el frontend
-- DROP POLICY IF EXISTS "obras_insert_admin" ON obras;
-- CREATE POLICY "obras_insert_admin"
-- ON obras FOR INSERT
-- WITH CHECK (
--     EXISTS (
--         SELECT 1 FROM perfiles_usuarios
--         WHERE id = auth.uid() AND rol = 'admin'
--     )
-- );

-- ============================================================================
-- POLÍTICA PARA DELETE: Solo admins pueden eliminar obras
-- ============================================================================
-- Descomenta esto si necesitas que los admins puedan eliminar obras desde el frontend
-- DROP POLICY IF EXISTS "obras_delete_admin" ON obras;
-- CREATE POLICY "obras_delete_admin"
-- ON obras FOR DELETE
-- USING (
--     EXISTS (
--         SELECT 1 FROM perfiles_usuarios
--         WHERE id = auth.uid() AND rol = 'admin'
--     )
-- );

-- ============================================================================
-- VERIFICACIÓN: Ver políticas actuales de la tabla obras
-- ============================================================================
-- Ejecuta esto para verificar que las políticas se crearon correctamente:
-- SELECT 
--     policyname,
--     cmd,  -- SELECT, INSERT, UPDATE, DELETE
--     qual,  -- Condición USING
--     with_check  -- Condición WITH CHECK
-- FROM pg_policies
-- WHERE tablename = 'obras'
-- ORDER BY cmd;

-- ============================================================================
-- NOTAS IMPORTANTES:
-- ============================================================================
-- 1. Estas políticas requieren que el usuario esté autenticado (auth.uid() existe)
-- 2. El usuario debe tener un perfil en perfiles_usuarios con rol = 'admin'
-- 3. La política de UPDATE usa tanto USING como WITH CHECK para máxima seguridad
-- 4. Las políticas de INSERT y DELETE están comentadas - descoméntalas si las necesitas
-- 5. La política de SELECT ya existe y permite lectura pública (no se modifica aquí)








