-- ============================================================================
-- ELIMINAR USUARIO COMPLETAMENTE DE SUPABASE
-- ============================================================================
-- Este script elimina un usuario y todos sus datos relacionados
-- Uso: Reemplaza 'isimo@ucm.es' con el email del usuario que quieres eliminar

-- ============================================================================
-- PASO 1: Obtener el ID del usuario desde su email
-- ============================================================================
-- Primero ejecuta esto para obtener el ID:
-- SELECT id, email FROM auth.users WHERE email = 'isimo@ucm.es';

-- ============================================================================
-- PASO 2: Eliminar datos relacionados (en orden)
-- ============================================================================

-- 1. Eliminar cambios pendientes del usuario
DELETE FROM cambios_pendientes 
WHERE usuario_id IN (
    SELECT id FROM auth.users WHERE email = 'isimo@ucm.es'
);

-- 2. Eliminar comentarios del usuario
DELETE FROM comentarios 
WHERE usuario_id IN (
    SELECT id FROM auth.users WHERE email = 'isimo@ucm.es'
);

-- 3. Eliminar validaciones del usuario (si existe la tabla)
-- DELETE FROM validaciones 
-- WHERE usuario_id IN (
--     SELECT id FROM auth.users WHERE email = 'isimo@ucm.es'
-- );

-- 4. Eliminar perfil del usuario
-- Esto se eliminará automáticamente por CASCADE cuando se elimine de auth.users
-- Pero lo hacemos explícitamente por si acaso:
DELETE FROM perfiles_usuarios 
WHERE id IN (
    SELECT id FROM auth.users WHERE email = 'isimo@ucm.es'
);

-- ============================================================================
-- PASO 3: Eliminar usuario de auth.users (esto eliminará todo por CASCADE)
-- ============================================================================
-- ⚠️ IMPORTANTE: Esto requiere permisos de admin en Supabase
-- Si no tienes permisos, ve a Authentication → Users y elimínalo desde ahí

DELETE FROM auth.users 
WHERE email = 'isimo@ucm.es';

-- ============================================================================
-- VERIFICACIÓN
-- ============================================================================
-- Ejecuta esto después para verificar que se eliminó:
-- SELECT id, email FROM auth.users WHERE email = 'isimo@ucm.es';
-- SELECT id, email FROM perfiles_usuarios WHERE id IN (SELECT id FROM auth.users WHERE email = 'isimo@ucm.es');

-- ============================================================================
-- NOTA: Método alternativo desde la UI de Supabase
-- ============================================================================
-- Si el DELETE no funciona por permisos, puedes eliminar desde la UI:
-- 1. Ve a Authentication → Users
-- 2. Busca el usuario por email
-- 3. Click en los tres puntos (...) → Delete user
-- Esto eliminará automáticamente todos los datos relacionados por CASCADE

