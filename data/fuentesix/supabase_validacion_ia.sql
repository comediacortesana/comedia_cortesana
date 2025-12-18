-- ============================================================================
-- TABLA: validaciones_analisis
-- Almacena validaciones de investigadores sobre análisis generados por IA
-- ============================================================================

CREATE TABLE IF NOT EXISTS validaciones_analisis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Identificación del análisis
    archivo_sintesis TEXT NOT NULL, -- Nombre del archivo de síntesis
    tipo_registro TEXT NOT NULL, -- 'representacion', 'obra', 'lugar'
    id_temporal TEXT NOT NULL, -- ID temporal del registro en la síntesis
    
    -- Estado de validación
    estado TEXT NOT NULL DEFAULT 'pendiente', -- 'validado', 'rechazado', 'pendiente'
    
    -- Usuario que validó
    usuario_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    
    -- Comentario del investigador
    comentario TEXT,
    
    -- Datos JSON completos del registro
    datos_json JSONB,
    
    -- Metadata
    fecha_validacion TIMESTAMPTZ DEFAULT NOW(),
    
    -- Integración a DB principal
    integrado BOOLEAN DEFAULT FALSE,
    id_integrado INTEGER, -- ID del registro creado en la tabla principal
    
    -- Constraints
    CONSTRAINT validaciones_analisis_estado_check CHECK (estado IN ('validado', 'rechazado', 'pendiente'))
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_validaciones_archivo ON validaciones_analisis(archivo_sintesis);
CREATE INDEX IF NOT EXISTS idx_validaciones_tipo ON validaciones_analisis(tipo_registro);
CREATE INDEX IF NOT EXISTS idx_validaciones_estado ON validaciones_analisis(estado);
CREATE INDEX IF NOT EXISTS idx_validaciones_usuario ON validaciones_analisis(usuario_id);
CREATE INDEX IF NOT EXISTS idx_validaciones_fecha ON validaciones_analisis(fecha_validacion DESC);

-- RLS (Row Level Security)
ALTER TABLE validaciones_analisis ENABLE ROW LEVEL SECURITY;

-- Política: Todos pueden leer validaciones
CREATE POLICY "Todos pueden leer validaciones"
    ON validaciones_analisis
    FOR SELECT
    USING (true);

-- Política: Usuarios autenticados pueden crear validaciones
CREATE POLICY "Usuarios autenticados pueden crear validaciones"
    ON validaciones_analisis
    FOR INSERT
    WITH CHECK (auth.uid() IS NOT NULL);

-- Política: Usuarios pueden actualizar sus propias validaciones
CREATE POLICY "Usuarios pueden actualizar sus validaciones"
    ON validaciones_analisis
    FOR UPDATE
    USING (auth.uid() = usuario_id);

-- ============================================================================
-- BUCKET DE STORAGE: sintesis
-- Almacena archivos JSON de síntesis para validación
-- ============================================================================

-- Crear bucket si no existe (ejecutar desde Supabase Dashboard o usar API)
-- INSERT INTO storage.buckets (id, name, public) 
-- VALUES ('sintesis', 'sintesis', false)
-- ON CONFLICT (id) DO NOTHING;

-- Política: Todos pueden leer archivos de síntesis
-- CREATE POLICY "Todos pueden leer síntesis"
--     ON storage.objects
--     FOR SELECT
--     USING (bucket_id = 'sintesis');

-- Política: Solo admins pueden subir síntesis
-- CREATE POLICY "Admins pueden subir síntesis"
--     ON storage.objects
--     FOR INSERT
--     WITH CHECK (
--         bucket_id = 'sintesis' AND
--         auth.uid() IN (SELECT id FROM auth.users WHERE id IN (
--             SELECT usuario_id FROM perfiles_usuarios WHERE rol = 'admin'
--         ))
--     );






