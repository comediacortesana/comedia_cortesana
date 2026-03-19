-- ============================================================================
-- FIX: Políticas RLS para perfiles_usuarios
-- ============================================================================
-- Si las consultas se quedan colgadas, ejecuta esto completo

-- 1. Deshabilitar RLS temporalmente para probar (SOLO PARA DEBUG)
-- ALTER TABLE perfiles_usuarios DISABLE ROW LEVEL SECURITY;

-- 2. O mejor: Asegurar que las políticas están correctas

-- Eliminar todas las políticas existentes
DROP POLICY IF EXISTS "perfiles_lectura_publica" ON perfiles_usuarios;
DROP POLICY IF EXISTS "perfiles_lectura_propia" ON perfiles_usuarios;
DROP POLICY IF EXISTS "perfiles_crear_propio" ON perfiles_usuarios;
DROP POLICY IF EXISTS "perfiles_editar_propio" ON perfiles_usuarios;
DROP POLICY IF EXISTS "perfiles_admin_editar" ON perfiles_usuarios;

-- Crear política de lectura pública (permite leer todos los perfiles)
CREATE POLICY "perfiles_lectura_publica"
ON perfiles_usuarios FOR SELECT
USING (true);

-- Crear política para que usuarios puedan leer su propio perfil
CREATE POLICY "perfiles_lectura_propia"
ON perfiles_usuarios FOR SELECT
USING (auth.uid() = id);

-- Crear política para INSERT (usuarios pueden crear su propio perfil)
CREATE POLICY "perfiles_crear_propio"
ON perfiles_usuarios FOR INSERT
WITH CHECK (auth.uid() = id);

-- Crear política para UPDATE (usuarios pueden editar su propio perfil)
CREATE POLICY "perfiles_editar_propio"
ON perfiles_usuarios FOR UPDATE
USING (auth.uid() = id)
WITH CHECK (auth.uid() = id);

-- Crear política para que admins puedan editar cualquier perfil
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

-- 3. Verificar que RLS está habilitado
ALTER TABLE perfiles_usuarios ENABLE ROW LEVEL SECURITY;

-- 4. Verificar políticas creadas
SELECT policyname, cmd, qual, with_check
FROM pg_policies
WHERE tablename = 'perfiles_usuarios';

-- 5. Probar consulta directa (debería funcionar ahora)
-- SELECT * FROM perfiles_usuarios WHERE id = '0ee04c53-39ca-4083-838e-14fbb66567b6';

