-- ============================================================================
-- CAMBIAR ROL DE USUARIOS A "admin"
-- ============================================================================
-- Cambia el rol de los siguientes usuarios a "admin":
-- - f.saez@filol.ucm.es
-- - delia.gavela@gmail.com
-- Ejecuta este SQL en Supabase SQL Editor

-- Cambiar ambos usuarios a admin
UPDATE perfiles_usuarios
SET rol = 'admin'
WHERE id IN (
    SELECT id FROM auth.users 
    WHERE email IN ('f.saez@filol.ucm.es', 'delia.gavela@gmail.com')
);

-- Verificar que los cambios se aplicaron
SELECT 
    pu.id,
    au.email,
    pu.nombre_completo,
    pu.rol,
    pu.updated_at
FROM perfiles_usuarios pu
JOIN auth.users au ON pu.id = au.id
WHERE au.email IN ('f.saez@filol.ucm.es', 'delia.gavela@gmail.com')
ORDER BY au.email;

-- ============================================================================
-- NOTAS:
-- ============================================================================
-- 1. Después de ejecutar este SQL, los usuarios deben:
--    - Cerrar sesión
--    - Volver a iniciar sesión
--    - Para que los cambios de rol surtan efecto
--
-- 2. Roles disponibles:
--    - 'colaborador' - Por defecto. Puede ver, filtrar, exportar y comentar
--    - 'editor' - Puede editar datos (cambios requieren aprobación)
--    - 'admin' - Acceso completo: gestionar usuarios, aprobar cambios, persistir datos
--
-- 3. Si algún usuario no existe, verifica:
--    SELECT * FROM auth.users WHERE email IN ('f.saez@filol.ucm.es', 'delia.gavela@gmail.com');
--    SELECT * FROM perfiles_usuarios WHERE nombre_completo LIKE '%saez%' OR nombre_completo LIKE '%delia%';
