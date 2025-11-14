-- ============================================================================
-- ELIMINAR USUARIO COMPLETAMENTE DE SUPABASE
-- ============================================================================
-- IMPORTANTE: Esto elimina el usuario de auth.users Y de perfiles_usuarios
-- El trigger ON DELETE CASCADE eliminará automáticamente el perfil

-- OPCIÓN 1: Eliminar por email (más fácil)
-- Reemplaza 'isimo@ucm.es' con el email del usuario que quieres eliminar

DELETE FROM auth.users
WHERE email = 'isimo@ucm.es';

-- OPCIÓN 2: Eliminar por UUID (más preciso)
-- Primero obtén el UUID del usuario desde Authentication > Users
-- Luego ejecuta esto (reemplaza el UUID):

-- DELETE FROM auth.users
-- WHERE id = '8a9a2143-5188-4dd1-9c0a-93cd48560c3d';

-- ============================================================================
-- VERIFICAR QUE SE ELIMINÓ
-- ============================================================================

-- Verificar que no existe en auth.users
SELECT id, email, created_at 
FROM auth.users 
WHERE email = 'isimo@ucm.es';

-- Verificar que el perfil también se eliminó (debería estar vacío por CASCADE)
SELECT * 
FROM perfiles_usuarios 
WHERE id IN (
    SELECT id FROM auth.users WHERE email = 'isimo@ucm.es'
);

-- ============================================================================
-- NOTA IMPORTANTE
-- ============================================================================
-- Si tienes la tabla perfiles_usuarios con ON DELETE CASCADE (como debería),
-- eliminar de auth.users automáticamente eliminará el perfil.
-- 
-- Si por alguna razón el perfil no se elimina automáticamente,
-- puedes eliminarlo manualmente:
--
-- DELETE FROM perfiles_usuarios WHERE id = 'UUID-DEL-USUARIO';

