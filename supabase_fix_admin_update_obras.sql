-- ============================================================================
-- FIX: Permitir que admins actualicen obras directamente
-- ============================================================================
-- Este script agrega políticas RLS para que usuarios con rol 'admin' 
-- puedan actualizar obras directamente sin pasar por cambios_pendientes

-- ============================================================================
-- POLÍTICA: Admins pueden actualizar obras
-- ============================================================================

DROP POLICY IF EXISTS "obras_admin_update" ON obras;
CREATE POLICY "obras_admin_update"
ON obras FOR UPDATE
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

-- ============================================================================
-- POLÍTICA: Editores pueden crear cambios pendientes (ya existe, pero verificamos)
-- ============================================================================
-- Esta política ya debería existir en cambios_pendientes, pero la verificamos

-- ============================================================================
-- VERIFICACIÓN
-- ============================================================================
-- Ejecuta esto para verificar que las políticas están activas:
-- SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual 
-- FROM pg_policies 
-- WHERE tablename = 'obras';

