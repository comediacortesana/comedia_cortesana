-- ============================================================================
-- ACTUALIZACIÓN DE SCHEMA: Agregar todos los campos necesarios a la tabla obras
-- ============================================================================
-- Ejecuta este script en Supabase SQL Editor para agregar todos los campos
-- que faltan en la tabla obras para que funcione como fuente principal

-- ============================================================================
-- CAMPOS DE TÍTULOS Y CLASIFICACIÓN
-- ============================================================================
ALTER TABLE obras ADD COLUMN IF NOT EXISTS titulo_alternativo TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS genero TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS subgenero TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS tema TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS idioma TEXT;

-- ============================================================================
-- CAMPOS DE ESTRUCTURA
-- ============================================================================
ALTER TABLE obras ADD COLUMN IF NOT EXISTS actos INTEGER;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS versos INTEGER;

-- ============================================================================
-- CAMPOS DE MÚSICA
-- ============================================================================
ALTER TABLE obras ADD COLUMN IF NOT EXISTS musica_conservada BOOLEAN DEFAULT FALSE;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS compositor TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS bibliotecas_musica TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS bibliografia_musica TEXT;

-- ============================================================================
-- CAMPOS DE MECENAZGO
-- ============================================================================
ALTER TABLE obras ADD COLUMN IF NOT EXISTS mecenas TEXT;

-- ============================================================================
-- CAMPOS DE BIBLIOGRAFÍA
-- ============================================================================
ALTER TABLE obras ADD COLUMN IF NOT EXISTS edicion_principe TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS notas_bibliograficas TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS manuscritos_conocidos TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS ediciones_conocidas TEXT;

-- ============================================================================
-- CAMPOS DE FUENTE Y ORIGEN
-- ============================================================================
ALTER TABLE obras ADD COLUMN IF NOT EXISTS origen_datos TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS pagina_pdf TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS texto_original_pdf TEXT;

-- ============================================================================
-- CAMPOS DE NOTAS
-- ============================================================================
ALTER TABLE obras ADD COLUMN IF NOT EXISTS notas TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS observaciones TEXT;

-- ============================================================================
-- CAMPOS COMPLEJOS (JSONB para flexibilidad)
-- ============================================================================
-- Autor como objeto JSONB (puede contener nombre, nombre_completo, fechas, etc.)
ALTER TABLE obras ADD COLUMN IF NOT EXISTS autor JSONB;

-- Representaciones como array JSONB
ALTER TABLE obras ADD COLUMN IF NOT EXISTS representaciones JSONB;

-- ============================================================================
-- ÍNDICES PARA BÚSQUEDAS RÁPIDAS
-- ============================================================================
CREATE INDEX IF NOT EXISTS idx_obras_genero ON obras(genero);
CREATE INDEX IF NOT EXISTS idx_obras_tipo_obra ON obras(tipo_obra);
CREATE INDEX IF NOT EXISTS idx_obras_fecha_creacion ON obras(fecha_creacion);

-- Índice GIN para búsquedas en campos JSONB
CREATE INDEX IF NOT EXISTS idx_obras_autor_gin ON obras USING gin(autor);
CREATE INDEX IF NOT EXISTS idx_obras_representaciones_gin ON obras USING gin(representaciones);

-- ============================================================================
-- COMENTARIOS EN COLUMNAS (Documentación)
-- ============================================================================
COMMENT ON COLUMN obras.autor IS 'Información del autor como objeto JSON: {nombre, nombre_completo, fecha_nacimiento, fecha_muerte, epoca, biografia}';
COMMENT ON COLUMN obras.representaciones IS 'Array de representaciones como JSON: [{fecha, lugar, compania, ...}]';
COMMENT ON COLUMN obras.musica_conservada IS 'Indica si la música de la obra está conservada';
COMMENT ON COLUMN obras.mecenas IS 'Mecenas o patrocinador de la obra';

-- ============================================================================
-- VERIFICACIÓN
-- ============================================================================
-- Ejecuta esto para verificar que todas las columnas se agregaron correctamente
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'obras' 
ORDER BY ordinal_position;

