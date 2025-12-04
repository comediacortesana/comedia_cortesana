-- ============================================================================
-- AÑADIR COLUMNA filtros_busqueda A COMENTARIOS
-- ============================================================================
-- Este script añade la columna filtros_busqueda si no existe
-- Ejecuta este script en Supabase SQL Editor si obtienes el error:
-- "Could not find the 'filtros_busqueda' column"
-- ============================================================================

-- Añadir campo para almacenar filtros de búsqueda asociados al comentario
ALTER TABLE comentarios
ADD COLUMN IF NOT EXISTS filtros_busqueda JSONB;

-- Verificar que se añadió correctamente
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'comentarios' 
AND column_name = 'filtros_busqueda';

