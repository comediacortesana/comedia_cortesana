-- ============================================================================
-- PERMITIR COMENTARIOS GENERALES (SIN obra_id)
-- ============================================================================
-- Este script elimina la restricción NOT NULL de obra_id para permitir
-- comentarios generales que no están asociados a una obra específica
-- ============================================================================

-- Verificar la restricción actual
SELECT 
    column_name, 
    is_nullable,
    data_type
FROM information_schema.columns
WHERE table_name = 'comentarios' 
AND column_name = 'obra_id';

-- Eliminar la restricción NOT NULL de obra_id
ALTER TABLE comentarios 
ALTER COLUMN obra_id DROP NOT NULL;

-- Verificar que se eliminó correctamente
SELECT 
    column_name, 
    is_nullable,
    data_type
FROM information_schema.columns
WHERE table_name = 'comentarios' 
AND column_name = 'obra_id';

-- Deberías ver is_nullable = 'YES' después de ejecutar este script

