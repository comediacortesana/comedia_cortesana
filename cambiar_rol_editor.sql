-- ============================================================================
-- CAMBIAR ROL DE USUARIO A "editor"
-- ============================================================================
-- Cambia el rol de f.saez@filol.ucm.es a "editor"
-- Ejecuta este SQL en Supabase SQL Editor

-- Método 1: Cambiar por email (Recomendado)
UPDATE perfiles_usuarios
SET rol = 'editor'
WHERE id IN (
    SELECT id FROM auth.users WHERE email = 'f.saez@filol.ucm.es'
);

-- Verificar que el cambio se aplicó
SELECT 
    pu.id,
    au.email,
    pu.nombre_completo,
    pu.rol,
    pu.updated_at
FROM perfiles_usuarios pu
JOIN auth.users au ON pu.id = au.id
WHERE au.email = 'f.saez@filol.ucm.es';

-- ============================================================================
-- NOTAS:
-- ============================================================================
-- 1. Después de ejecutar este SQL, el usuario debe:
--    - Cerrar sesión
--    - Volver a iniciar sesión
--    - Para que los cambios de rol surtan efecto
--
-- 2. Roles disponibles:
--    - 'colaborador' - Por defecto. Puede ver, filtrar, exportar y comentar
--    - 'editor' - Puede editar datos (cambios requieren aprobación)
--    - 'admin' - Acceso completo: gestionar usuarios, aprobar cambios, persistir datos
--
-- 3. Si el usuario no existe, verifica:
--    SELECT * FROM auth.users WHERE email = 'f.saez@filol.ucm.es';
--    SELECT * FROM perfiles_usuarios WHERE nombre_completo LIKE '%saez%';
