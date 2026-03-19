-- ============================================================================
-- SISTEMA DE COMENTARIOS Y LOGS MEJORADO
-- ============================================================================
-- Este script añade funcionalidades para:
-- 1. Sistema de comentarios con marcado "OK, visto" por admin
-- 2. Sistema de logs de errores de carga de datos
-- ============================================================================

-- ============================================================================
-- 1. ACTUALIZAR TABLA COMENTARIOS
-- ============================================================================

-- Permitir comentarios generales (sin obra_id)
ALTER TABLE comentarios 
ALTER COLUMN obra_id DROP NOT NULL;

-- Añadir campo para marcar comentarios como vistos por admin
ALTER TABLE comentarios 
ADD COLUMN IF NOT EXISTS visto_por_admin BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS visto_at TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS visto_por UUID REFERENCES auth.users(id);

-- Añadir campo para almacenar filtros de búsqueda asociados al comentario
ALTER TABLE comentarios
ADD COLUMN IF NOT EXISTS filtros_busqueda JSONB;

-- Crear índice para búsquedas rápidas de comentarios no vistos
CREATE INDEX IF NOT EXISTS idx_comentarios_visto ON comentarios(visto_por_admin) WHERE visto_por_admin = FALSE;

-- Crear índice para comentarios generales (sin obra_id)
CREATE INDEX IF NOT EXISTS idx_comentarios_generales ON comentarios(obra_id) WHERE obra_id IS NULL;

-- ============================================================================
-- 2. CREAR TABLA LOGS_ERRORES
-- ============================================================================

CREATE TABLE IF NOT EXISTS logs_errores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tipo_error TEXT NOT NULL DEFAULT 'carga_datos',
    mensaje TEXT NOT NULL,
    detalles JSONB,
    usuario_id UUID REFERENCES auth.users(id),
    usuario_email TEXT,
    url TEXT,
    user_agent TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    visto_por_admin BOOLEAN DEFAULT FALSE,
    visto_at TIMESTAMPTZ,
    visto_por UUID REFERENCES auth.users(id)
);

CREATE INDEX IF NOT EXISTS idx_logs_errores_tipo ON logs_errores(tipo_error);
CREATE INDEX IF NOT EXISTS idx_logs_errores_usuario ON logs_errores(usuario_id);
CREATE INDEX IF NOT EXISTS idx_logs_errores_created ON logs_errores(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_logs_errores_visto ON logs_errores(visto_por_admin) WHERE visto_por_admin = FALSE;

-- ============================================================================
-- 3. ACTUALIZAR POLÍTICAS RLS PARA COMENTARIOS
-- ============================================================================

-- Permitir que admins marquen comentarios como vistos
DROP POLICY IF EXISTS "comentarios_admin_marcar_visto" ON comentarios;
CREATE POLICY "comentarios_admin_marcar_visto"
ON comentarios FOR UPDATE
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

-- Permitir lectura pública de comentarios (ya existe, pero la mantenemos)
-- Los comentarios son públicos para cualquier usuario autenticado

-- ============================================================================
-- 4. POLÍTICAS RLS PARA LOGS_ERRORES
-- ============================================================================

ALTER TABLE logs_errores ENABLE ROW LEVEL SECURITY;

-- Cualquier usuario autenticado puede crear logs de errores
DROP POLICY IF EXISTS "logs_errores_crear_autenticado" ON logs_errores;
CREATE POLICY "logs_errores_crear_autenticado"
ON logs_errores FOR INSERT
WITH CHECK (auth.role() = 'authenticated');

-- Solo admins pueden leer logs de errores
DROP POLICY IF EXISTS "logs_errores_lectura_admin" ON logs_errores;
CREATE POLICY "logs_errores_lectura_admin"
ON logs_errores FOR SELECT
USING (
    EXISTS (
        SELECT 1 FROM perfiles_usuarios
        WHERE id = auth.uid() AND rol = 'admin'
    )
);

-- Solo admins pueden marcar logs como vistos
DROP POLICY IF EXISTS "logs_errores_admin_marcar_visto" ON logs_errores;
CREATE POLICY "logs_errores_admin_marcar_visto"
ON logs_errores FOR UPDATE
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
-- 5. FUNCIÓN PARA MARCAR COMENTARIO COMO VISTO
-- ============================================================================

CREATE OR REPLACE FUNCTION marcar_comentario_visto(comentario_id UUID)
RETURNS BOOLEAN AS $$
DECLARE
    es_admin BOOLEAN;
BEGIN
    -- Verificar que el usuario es admin
    SELECT EXISTS (
        SELECT 1 FROM perfiles_usuarios
        WHERE id = auth.uid() AND rol = 'admin'
    ) INTO es_admin;
    
    IF NOT es_admin THEN
        RAISE EXCEPTION 'Solo los administradores pueden marcar comentarios como vistos';
    END IF;
    
    -- Marcar como visto
    UPDATE comentarios
    SET visto_por_admin = TRUE,
        visto_at = NOW(),
        visto_por = auth.uid()
    WHERE id = comentario_id;
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================================================
-- 6. FUNCIÓN PARA MARCAR LOG DE ERROR COMO VISTO
-- ============================================================================

CREATE OR REPLACE FUNCTION marcar_log_error_visto(log_id UUID)
RETURNS BOOLEAN AS $$
DECLARE
    es_admin BOOLEAN;
BEGIN
    -- Verificar que el usuario es admin
    SELECT EXISTS (
        SELECT 1 FROM perfiles_usuarios
        WHERE id = auth.uid() AND rol = 'admin'
    ) INTO es_admin;
    
    IF NOT es_admin THEN
        RAISE EXCEPTION 'Solo los administradores pueden marcar logs como vistos';
    END IF;
    
    -- Marcar como visto
    UPDATE logs_errores
    SET visto_por_admin = TRUE,
        visto_at = NOW(),
        visto_por = auth.uid()
    WHERE id = log_id;
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================================================
-- 7. VISTA PARA ADMINS: COMENTARIOS NO VISTOS
-- ============================================================================

CREATE OR REPLACE VIEW comentarios_pendientes AS
SELECT 
    c.id,
    c.obra_id,
    o.titulo as obra_titulo,
    c.usuario_id,
    pu.nombre_completo as usuario_nombre,
    c.contenido,
    c.tipo,
    c.estado,
    c.visto_por_admin,
    c.created_at,
    c.updated_at
FROM comentarios c
LEFT JOIN obras o ON c.obra_id = o.id
LEFT JOIN perfiles_usuarios pu ON c.usuario_id = pu.id
WHERE c.visto_por_admin = FALSE
ORDER BY c.created_at DESC;

-- ============================================================================
-- 8. VISTA PARA ADMINS: LOGS DE ERRORES NO VISTOS
-- ============================================================================

CREATE OR REPLACE VIEW logs_errores_pendientes AS
SELECT 
    l.id,
    l.tipo_error,
    l.mensaje,
    l.detalles,
    l.usuario_id,
    l.usuario_email,
    l.url,
    l.created_at,
    l.visto_por_admin,
    pu.nombre_completo as usuario_nombre
FROM logs_errores l
LEFT JOIN perfiles_usuarios pu ON l.usuario_id = pu.id
WHERE l.visto_por_admin = FALSE
ORDER BY l.created_at DESC;

-- ============================================================================
-- FIN DEL SCRIPT
-- ============================================================================
-- Ejecuta este script en Supabase SQL Editor
-- Luego actualiza el código JavaScript en index.html
-- ============================================================================

