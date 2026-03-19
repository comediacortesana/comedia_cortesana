-- ============================================================================
-- FIX: Política RLS para que admins puedan editar roles de otros usuarios
-- ============================================================================
-- Ejecuta esto en Supabase SQL Editor si los admins no pueden cambiar roles

-- Verificar políticas actuales
SELECT policyname, cmd, qual, with_check
FROM pg_policies
WHERE tablename = 'perfiles_usuarios';

-- Eliminar política de admin si existe (para recrearla)
DROP POLICY IF EXISTS "perfiles_admin_editar" ON perfiles_usuarios;

-- Crear política para que admins puedan editar cualquier perfil
-- IMPORTANTE: Esta política permite a los admins actualizar CUALQUIER campo,
-- incluyendo el rol de otros usuarios
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

-- Verificar que se creó correctamente
SELECT policyname, cmd, qual, with_check
FROM pg_policies
WHERE tablename = 'perfiles_usuarios' AND policyname = 'perfiles_admin_editar';

-- Nota: Esta política funciona así:
-- 1. USING: Verifica que el usuario actual (auth.uid()) tiene rol 'admin' en perfiles_usuarios
-- 2. WITH CHECK: Verifica lo mismo para la fila después de la actualización
-- 3. Si ambas condiciones son verdaderas, permite la actualización

