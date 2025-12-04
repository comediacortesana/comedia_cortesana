-- ============================================================================
-- HACER ADMIN A UN USUARIO
-- ============================================================================
-- Ejecuta este SQL en Supabase SQL Editor

-- OPCIÓN 1: Cambiar por EMAIL (Más fácil)
-- Reemplaza 'isimosanchez@gmail.com' con el email del usuario que quieres hacer admin

UPDATE perfiles_usuarios
SET rol = 'admin'
WHERE id IN (
    SELECT id FROM auth.users WHERE email = 'isimosanchez@gmail.com'
);

-- OPCIÓN 2: Cambiar por UUID (Más preciso)
-- Primero obtén el UUID desde Authentication > Users
-- Luego ejecuta esto (reemplaza el UUID):

-- UPDATE perfiles_usuarios
-- SET rol = 'admin'
-- WHERE id = 'TU-UUID-AQUI';

-- Verificar que se actualizó
SELECT id, nombre_completo, rol, created_at
FROM perfiles_usuarios 
WHERE rol = 'admin';

-- Ver todos los usuarios y sus roles
SELECT 
    pu.id,
    pu.nombre_completo,
    pu.rol,
    au.email
FROM perfiles_usuarios pu
LEFT JOIN auth.users au ON pu.id = au.id
ORDER BY pu.created_at DESC;

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

