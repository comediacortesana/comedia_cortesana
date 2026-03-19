-- ============================================================================
-- CORRECCIÓN DE FUENTE: FUENTESXI → Fuentes IX
-- ============================================================================
-- Este script actualiza todas las obras que tienen "FUENTESXI" en el campo fuente
-- y las cambia a "Fuentes IX"
--
-- IMPORTANTE: Ejecuta este script en Supabase SQL Editor
-- ============================================================================

-- Verificar cuántas obras tienen FUENTESXI antes del cambio
SELECT COUNT(*) as total_obras_con_fuentesxi
FROM obras
WHERE fuente = 'FUENTESXI';

-- Mostrar algunas obras afectadas (opcional, para verificación)
SELECT id, titulo, fuente
FROM obras
WHERE fuente = 'FUENTESXI'
ORDER BY id
LIMIT 10;

-- ============================================================================
-- ACTUALIZAR FUENTE
-- ============================================================================
-- ⚠️ Esta operación actualizará todas las obras con FUENTESXI
-- Se recomienda hacer backup antes de ejecutar

UPDATE obras
SET fuente = 'Fuentes IX',
    updated_at = NOW()
WHERE fuente = 'FUENTESXI';

-- ============================================================================
-- VERIFICACIÓN POST-ACTUALIZACIÓN
-- ============================================================================

-- Verificar que no quedan obras con FUENTESXI
SELECT COUNT(*) as obras_con_fuentesxi_restantes
FROM obras
WHERE fuente = 'FUENTESXI';
-- Debería retornar 0

-- Verificar cuántas obras tienen ahora "Fuentes IX"
SELECT COUNT(*) as obras_con_fuentes_ix
FROM obras
WHERE fuente = 'Fuentes IX';

-- Mostrar algunas obras actualizadas (opcional)
SELECT id, titulo, fuente, updated_at
FROM obras
WHERE fuente = 'Fuentes IX'
ORDER BY updated_at DESC
LIMIT 10;

