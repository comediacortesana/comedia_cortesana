-- ============================================================================
-- TABLA: analisis_ia_fuentes_ix
-- ============================================================================
-- Almacena análisis, interpretaciones y contexto de la IA al procesar
-- textos de Fuentes IX, similar a comentarios pero específico para IA
-- ============================================================================

CREATE TABLE IF NOT EXISTS analisis_ia_fuentes_ix (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Relación con registros (puede ser obra, representacion, lugar, etc.)
    tipo_registro VARCHAR(50) NOT NULL, -- 'obra', 'representacion', 'lugar', 'mecenas', 'compañia'
    registro_id VARCHAR(200), -- ID del registro relacionado (puede ser temporal antes de integrar)
    
    -- Tipo de análisis
    tipo_analisis VARCHAR(50) DEFAULT 'analisis_ia_fuentes_ix', -- 'analisis_ia_fuentes_ix', 'discrepancia_fuentes', 'patron_deteccion', 'frase_contexto'
    
    -- Datos extraídos (resumen estructurado)
    datos_extraidos JSONB,
    
    -- Frases originales donde se encontraron los datos
    frases_originales JSONB DEFAULT '[]'::jsonb, -- Array de frases
    
    -- Interpretaciones de la IA
    interpretaciones JSONB DEFAULT '[]'::jsonb, -- Array de interpretaciones
    
    -- Discrepancias detectadas
    discrepancias JSONB DEFAULT '[]'::jsonb, -- Array de discrepancias
    
    -- Patrones detectados
    patrones_detectados JSONB DEFAULT '[]'::jsonb, -- Array de patrones
    
    -- Nivel de confianza
    confianza VARCHAR(20) DEFAULT 'medio', -- 'alto', 'medio', 'bajo'
    
    -- Contexto adicional
    contexto_adicional JSONB DEFAULT '{}'::jsonb,
    
    -- Metadata de fuente
    archivo_fuente VARCHAR(200),
    pagina_pdf INTEGER,
    linea_texto INTEGER,
    
    -- Metadata de IA
    fuente_ia VARCHAR(100) DEFAULT 'sistema_extraccion_inteligente',
    version_ia VARCHAR(20) DEFAULT '1.0.0',
    
    -- Metadata de versionado
    version_datos VARCHAR(50),
    fecha_extraccion TIMESTAMPTZ,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Estado
    estado VARCHAR(50) DEFAULT 'pendiente_revision', -- 'pendiente_revision', 'revisado', 'integrado', 'rechazado'
    revisado_por UUID REFERENCES auth.users(id),
    revisado_at TIMESTAMPTZ,
    notas_revision TEXT
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_analisis_tipo_registro ON analisis_ia_fuentes_ix(tipo_registro);
CREATE INDEX IF NOT EXISTS idx_analisis_registro_id ON analisis_ia_fuentes_ix(registro_id);
CREATE INDEX IF NOT EXISTS idx_analisis_tipo_analisis ON analisis_ia_fuentes_ix(tipo_analisis);
CREATE INDEX IF NOT EXISTS idx_analisis_confianza ON analisis_ia_fuentes_ix(confianza);
CREATE INDEX IF NOT EXISTS idx_analisis_estado ON analisis_ia_fuentes_ix(estado);
CREATE INDEX IF NOT EXISTS idx_analisis_archivo ON analisis_ia_fuentes_ix(archivo_fuente);
CREATE INDEX IF NOT EXISTS idx_analisis_version ON analisis_ia_fuentes_ix(version_datos);

-- Índice GIN para búsqueda en JSONB
CREATE INDEX IF NOT EXISTS idx_analisis_frases_gin ON analisis_ia_fuentes_ix USING gin(frases_originales);
CREATE INDEX IF NOT EXISTS idx_analisis_interpretaciones_gin ON analisis_ia_fuentes_ix USING gin(interpretaciones);
CREATE INDEX IF NOT EXISTS idx_analisis_discrepancias_gin ON analisis_ia_fuentes_ix USING gin(discrepancias);

-- Comentarios de la tabla
COMMENT ON TABLE analisis_ia_fuentes_ix IS 'Análisis e interpretaciones de IA al procesar textos de Fuentes IX';
COMMENT ON COLUMN analisis_ia_fuentes_ix.tipo_registro IS 'Tipo de registro: obra, representacion, lugar, mecenas, compañia';
COMMENT ON COLUMN analisis_ia_fuentes_ix.registro_id IS 'ID del registro relacionado (puede ser temporal antes de integrar)';
COMMENT ON COLUMN analisis_ia_fuentes_ix.frases_originales IS 'Array JSON con frases originales donde se encontraron los datos';
COMMENT ON COLUMN analisis_ia_fuentes_ix.interpretaciones IS 'Array JSON con interpretaciones de la IA';
COMMENT ON COLUMN analisis_ia_fuentes_ix.discrepancias IS 'Array JSON con discrepancias detectadas entre fuentes';
COMMENT ON COLUMN analisis_ia_fuentes_ix.patrones_detectados IS 'Array JSON con patrones que llevaron a esta extracción';
COMMENT ON COLUMN analisis_ia_fuentes_ix.confianza IS 'Nivel de confianza: alto, medio, bajo';

-- ============================================================================
-- POLÍTICAS RLS (Row Level Security)
-- ============================================================================

ALTER TABLE analisis_ia_fuentes_ix ENABLE ROW LEVEL SECURITY;

-- Política: Lectura pública para usuarios autenticados
CREATE POLICY "Usuarios autenticados pueden leer análisis IA"
    ON analisis_ia_fuentes_ix
    FOR SELECT
    USING (auth.role() = 'authenticated');

-- Política: Solo sistema/IA puede crear análisis (o usuarios con permisos especiales)
CREATE POLICY "Sistema puede crear análisis IA"
    ON analisis_ia_fuentes_ix
    FOR INSERT
    WITH CHECK (true); -- Permitir creación desde sistema

-- Política: Solo admins pueden actualizar (marcar como revisado, etc.)
CREATE POLICY "Admins pueden actualizar análisis IA"
    ON analisis_ia_fuentes_ix
    FOR UPDATE
    USING (
        EXISTS (
            SELECT 1 FROM perfiles_usuarios
            WHERE perfiles_usuarios.usuario_id = auth.uid()
            AND perfiles_usuarios.rol IN ('admin', 'editor')
        )
    );

-- ============================================================================
-- FUNCIÓN: Actualizar updated_at automáticamente
-- ============================================================================

CREATE OR REPLACE FUNCTION update_analisis_ia_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_analisis_ia_updated_at
    BEFORE UPDATE ON analisis_ia_fuentes_ix
    FOR EACH ROW
    EXECUTE FUNCTION update_analisis_ia_updated_at();

-- ============================================================================
-- VISTA: Análisis pendientes de revisión
-- ============================================================================

CREATE OR REPLACE VIEW analisis_ia_pendientes AS
SELECT 
    id,
    tipo_registro,
    registro_id,
    tipo_analisis,
    confianza,
    estado,
    archivo_fuente,
    created_at,
    CASE 
        WHEN discrepancias::text != '[]'::text THEN true
        ELSE false
    END AS tiene_discrepancias,
    jsonb_array_length(frases_originales) as total_frases,
    jsonb_array_length(interpretaciones) as total_interpretaciones
FROM analisis_ia_fuentes_ix
WHERE estado = 'pendiente_revision'
ORDER BY created_at DESC;

COMMENT ON VIEW analisis_ia_pendientes IS 'Vista de análisis IA pendientes de revisión';






