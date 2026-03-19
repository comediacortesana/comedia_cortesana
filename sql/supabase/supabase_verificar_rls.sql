-- ============================================================================
-- VERIFICAR Y CORREGIR POLÍTICAS RLS PARA perfiles_usuarios
-- ============================================================================
-- Ejecuta este SQL en Supabase SQL Editor si tienes problemas cargando el rol

-- 1. Verificar políticas actuales
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual,
    with_check
FROM pg_policies
WHERE tablename = 'perfiles_usuarios';

-- 2. Verificar que RLS está habilitado
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public' AND tablename = 'perfiles_usuarios';

-- 3. Si RLS está bloqueando, asegurar que la política de lectura pública existe
DROP POLICY IF EXISTS "perfiles_lectura_publica" ON perfiles_usuarios;
CREATE POLICY "perfiles_lectura_publica"
ON perfiles_usuarios FOR SELECT
USING (true);

-- 4. Verificar que puedes leer tu propio perfil (debería funcionar siempre)
-- Esta política permite que cualquier usuario autenticado lea su propio perfil
DROP POLICY IF EXISTS "perfiles_lectura_propia" ON perfiles_usuarios;
CREATE POLICY "perfiles_lectura_propia"
ON perfiles_usuarios FOR SELECT
USING (auth.uid() = id);

-- 5. Probar consulta directa (reemplaza el UUID con el tuyo)
-- SELECT * FROM perfiles_usuarios WHERE id = '0ee04c53-39ca-4083-838e-14fbb66567b6';

-- 6. Ver todos los perfiles (debería funcionar con la política pública)
SELECT id, nombre_completo, rol FROM perfiles_usuarios;

