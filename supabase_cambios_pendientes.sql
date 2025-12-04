-- ============================================================================
-- TABLA: cambios_pendientes
-- Cambios propuestos por editores que requieren aprobación de admin
-- ============================================================================
CREATE TABLE IF NOT EXISTS cambios_pendientes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    obra_id TEXT NOT NULL, -- ID de la obra (puede ser string o número)
    campo TEXT NOT NULL, -- Nombre del campo editado (ej: 'titulo', 'autor')
    valor_anterior TEXT, -- Valor antes del cambio
    valor_nuevo TEXT NOT NULL, -- Nuevo valor propuesto
    usuario_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    estado TEXT DEFAULT 'pendiente', -- 'pendiente', 'aprobado', 'rechazado'
    revisado_por UUID REFERENCES auth.users(id),
    revisado_at TIMESTAMPTZ,
    justificacion TEXT, -- Justificación del cambio (opcional)
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para búsquedas rápidas
CREATE INDEX IF NOT EXISTS idx_cambios_obra ON cambios_pendientes(obra_id);
CREATE INDEX IF NOT EXISTS idx_cambios_usuario ON cambios_pendientes(usuario_id);
CREATE INDEX IF NOT EXISTS idx_cambios_estado ON cambios_pendientes(estado);
CREATE INDEX IF NOT EXISTS idx_cambios_created ON cambios_pendientes(created_at DESC);

-- Trigger para updated_at
DROP TRIGGER IF EXISTS update_cambios_updated_at ON cambios_pendientes;
CREATE TRIGGER update_cambios_updated_at BEFORE UPDATE ON cambios_pendientes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- ROW LEVEL SECURITY (RLS)
-- ============================================================================

ALTER TABLE cambios_pendientes ENABLE ROW LEVEL SECURITY;

-- Lectura pública (todos pueden ver cambios pendientes)
DROP POLICY IF EXISTS "cambios_lectura_publica" ON cambios_pendientes;
CREATE POLICY "cambios_lectura_publica"
ON cambios_pendientes FOR SELECT
USING (true);

-- Cualquier usuario autenticado puede crear cambios pendientes
DROP POLICY IF EXISTS "cambios_crear_autenticado" ON cambios_pendientes;
CREATE POLICY "cambios_crear_autenticado"
ON cambios_pendientes FOR INSERT
WITH CHECK (auth.role() = 'authenticated');

-- Solo el usuario que creó el cambio puede editarlo si está pendiente
DROP POLICY IF EXISTS "cambios_editar_propio" ON cambios_pendientes;
CREATE POLICY "cambios_editar_propio"
ON cambios_pendientes FOR UPDATE
USING (
    auth.uid() = usuario_id 
    AND estado = 'pendiente'
)
WITH CHECK (
    auth.uid() = usuario_id 
    AND estado = 'pendiente'
);

-- Solo admins pueden aprobar/rechazar cambios
DROP POLICY IF EXISTS "cambios_admin_revisar" ON cambios_pendientes;
CREATE POLICY "cambios_admin_revisar"
ON cambios_pendientes FOR UPDATE
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

-- ============================================================================
-- FUNCIÓN: Agrupar cambios por obra
-- ============================================================================
CREATE OR REPLACE FUNCTION obtener_cambios_por_obra()
RETURNS TABLE (
    obra_id TEXT,
    total_cambios BIGINT,
    cambios_pendientes BIGINT,
    cambios_aprobados BIGINT,
    cambios_rechazados BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        cp.obra_id,
        COUNT(*)::BIGINT as total_cambios,
        COUNT(*) FILTER (WHERE cp.estado = 'pendiente')::BIGINT as cambios_pendientes,
        COUNT(*) FILTER (WHERE cp.estado = 'aprobado')::BIGINT as cambios_aprobados,
        COUNT(*) FILTER (WHERE cp.estado = 'rechazado')::BIGINT as cambios_rechazados
    FROM cambios_pendientes cp
    GROUP BY cp.obra_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

