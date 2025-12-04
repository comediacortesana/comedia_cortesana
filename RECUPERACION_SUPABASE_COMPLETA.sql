-- ============================================================================
-- SCRIPT MAESTRO DE RECUPERACIÓN COMPLETA DE SUPABASE
-- ============================================================================
-- Este script recrea TODA la estructura de la base de datos desde cero
-- Ejecuta este script completo en Supabase SQL Editor (Dashboard > SQL Editor)
-- Fecha de creación: Diciembre 2025
-- ============================================================================

-- ============================================================================
-- PASO 1: CREAR TABLAS BASE
-- ============================================================================

-- Tabla: obras (catálogo principal)
CREATE TABLE IF NOT EXISTS obras (
    id INTEGER PRIMARY KEY,
    titulo TEXT,
    titulo_original TEXT,
    tipo_obra TEXT,
    autor_nombre TEXT,
    fuente TEXT,
    fecha_creacion TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    synced_from_sheet_at TIMESTAMPTZ
);

-- Tabla: perfiles_usuarios (información adicional de usuarios)
CREATE TABLE IF NOT EXISTS perfiles_usuarios (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    nombre_completo TEXT,
    rol TEXT DEFAULT 'colaborador',
    bio TEXT,
    avatar_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla: comentarios (comentarios de usuarios sobre obras)
CREATE TABLE IF NOT EXISTS comentarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    obra_id INTEGER REFERENCES obras(id) ON DELETE CASCADE,  -- NULL permite comentarios generales
    usuario_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    contenido TEXT NOT NULL,
    tipo TEXT DEFAULT 'comentario',
    estado TEXT DEFAULT 'pendiente',
    visto_por_admin BOOLEAN DEFAULT FALSE,
    visto_at TIMESTAMPTZ,
    visto_por UUID REFERENCES auth.users(id),
    filtros_busqueda JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla: validaciones (propuestas de cambios de usuarios)
CREATE TABLE IF NOT EXISTS validaciones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    obra_id INTEGER NOT NULL REFERENCES obras(id) ON DELETE CASCADE,
    usuario_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    campo TEXT NOT NULL,
    valor_actual TEXT,
    valor_propuesto TEXT NOT NULL,
    justificacion TEXT,
    estado TEXT DEFAULT 'pendiente',
    revisado_por UUID REFERENCES auth.users(id),
    revisado_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla: historial_validaciones (auditoría de cambios aprobados)
CREATE TABLE IF NOT EXISTS historial_validaciones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    validacion_id UUID REFERENCES validaciones(id),
    obra_id INTEGER NOT NULL,
    usuario_id UUID NOT NULL,
    campo TEXT NOT NULL,
    valor_anterior TEXT,
    valor_nuevo TEXT,
    aprobado_por UUID REFERENCES auth.users(id),
    aprobado_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla: logs_errores (sistema de logs de errores)
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

-- ============================================================================
-- PASO 2: AGREGAR CAMPOS ADICIONALES A OBRAS
-- ============================================================================

-- Campos de títulos y clasificación
ALTER TABLE obras ADD COLUMN IF NOT EXISTS titulo_alternativo TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS genero TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS subgenero TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS tema TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS idioma TEXT;

-- Campos de estructura
ALTER TABLE obras ADD COLUMN IF NOT EXISTS actos INTEGER;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS versos INTEGER;

-- Campos de música
ALTER TABLE obras ADD COLUMN IF NOT EXISTS musica_conservada BOOLEAN DEFAULT FALSE;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS compositor TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS bibliotecas_musica TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS bibliografia_musica TEXT;

-- Campos de mecenazgo
ALTER TABLE obras ADD COLUMN IF NOT EXISTS mecenas TEXT;

-- Campos de bibliografía
ALTER TABLE obras ADD COLUMN IF NOT EXISTS edicion_principe TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS notas_bibliograficas TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS manuscritos_conocidos TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS ediciones_conocidas TEXT;

-- Campos de fuente y origen
ALTER TABLE obras ADD COLUMN IF NOT EXISTS origen_datos TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS pagina_pdf TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS texto_original_pdf TEXT;

-- Campos de notas
ALTER TABLE obras ADD COLUMN IF NOT EXISTS notas TEXT;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS observaciones TEXT;

-- Campos complejos (JSONB)
ALTER TABLE obras ADD COLUMN IF NOT EXISTS autor JSONB;
ALTER TABLE obras ADD COLUMN IF NOT EXISTS representaciones JSONB;

-- ============================================================================
-- PASO 3: CREAR ÍNDICES PARA RENDIMIENTO
-- ============================================================================

-- Índices para búsquedas en obras
CREATE INDEX IF NOT EXISTS idx_obras_titulo ON obras USING gin(to_tsvector('spanish', titulo));
CREATE INDEX IF NOT EXISTS idx_obras_autor ON obras(autor_nombre);
CREATE INDEX IF NOT EXISTS idx_obras_fuente ON obras(fuente);
CREATE INDEX IF NOT EXISTS idx_obras_genero ON obras(genero);
CREATE INDEX IF NOT EXISTS idx_obras_tipo_obra ON obras(tipo_obra);
CREATE INDEX IF NOT EXISTS idx_obras_fecha_creacion ON obras(fecha_creacion);
CREATE INDEX IF NOT EXISTS idx_obras_autor_gin ON obras USING gin(autor);
CREATE INDEX IF NOT EXISTS idx_obras_representaciones_gin ON obras USING gin(representaciones);

-- Índices para comentarios
CREATE INDEX IF NOT EXISTS idx_comentarios_obra ON comentarios(obra_id);
CREATE INDEX IF NOT EXISTS idx_comentarios_usuario ON comentarios(usuario_id);
CREATE INDEX IF NOT EXISTS idx_comentarios_visto ON comentarios(visto_por_admin) WHERE visto_por_admin = FALSE;
CREATE INDEX IF NOT EXISTS idx_comentarios_generales ON comentarios(obra_id) WHERE obra_id IS NULL;

-- Índices para validaciones
CREATE INDEX IF NOT EXISTS idx_validaciones_obra ON validaciones(obra_id);
CREATE INDEX IF NOT EXISTS idx_validaciones_usuario ON validaciones(usuario_id);
CREATE INDEX IF NOT EXISTS idx_validaciones_estado ON validaciones(estado);

-- Índices para historial
CREATE INDEX IF NOT EXISTS idx_historial_obra ON historial_validaciones(obra_id);
CREATE INDEX IF NOT EXISTS idx_historial_usuario ON historial_validaciones(usuario_id);

-- Índices para logs de errores
CREATE INDEX IF NOT EXISTS idx_logs_errores_tipo ON logs_errores(tipo_error);
CREATE INDEX IF NOT EXISTS idx_logs_errores_usuario ON logs_errores(usuario_id);
CREATE INDEX IF NOT EXISTS idx_logs_errores_created ON logs_errores(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_logs_errores_visto ON logs_errores(visto_por_admin) WHERE visto_por_admin = FALSE;

-- ============================================================================
-- PASO 4: CREAR FUNCIONES Y TRIGGERS
-- ============================================================================

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para updated_at
DROP TRIGGER IF EXISTS update_obras_updated_at ON obras;
CREATE TRIGGER update_obras_updated_at BEFORE UPDATE ON obras
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_comentarios_updated_at ON comentarios;
CREATE TRIGGER update_comentarios_updated_at BEFORE UPDATE ON comentarios
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_perfiles_updated_at ON perfiles_usuarios;
CREATE TRIGGER update_perfiles_updated_at BEFORE UPDATE ON perfiles_usuarios
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Función para crear perfil automáticamente al registrarse
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.perfiles_usuarios (id, nombre_completo, rol)
  VALUES (
    NEW.id,
    COALESCE(NEW.raw_user_meta_data->>'nombre_completo', NEW.email),
    'colaborador'
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger para crear perfil al registrar usuario
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Función para marcar comentario como visto
CREATE OR REPLACE FUNCTION marcar_comentario_visto(comentario_id UUID)
RETURNS BOOLEAN AS $$
DECLARE
    es_admin BOOLEAN;
BEGIN
    SELECT EXISTS (
        SELECT 1 FROM perfiles_usuarios
        WHERE id = auth.uid() AND rol = 'admin'
    ) INTO es_admin;
    
    IF NOT es_admin THEN
        RAISE EXCEPTION 'Solo los administradores pueden marcar comentarios como vistos';
    END IF;
    
    UPDATE comentarios
    SET visto_por_admin = TRUE,
        visto_at = NOW(),
        visto_por = auth.uid()
    WHERE id = comentario_id;
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Función para marcar log de error como visto
CREATE OR REPLACE FUNCTION marcar_log_error_visto(log_id UUID)
RETURNS BOOLEAN AS $$
DECLARE
    es_admin BOOLEAN;
BEGIN
    SELECT EXISTS (
        SELECT 1 FROM perfiles_usuarios
        WHERE id = auth.uid() AND rol = 'admin'
    ) INTO es_admin;
    
    IF NOT es_admin THEN
        RAISE EXCEPTION 'Solo los administradores pueden marcar logs como vistos';
    END IF;
    
    UPDATE logs_errores
    SET visto_por_admin = TRUE,
        visto_at = NOW(),
        visto_por = auth.uid()
    WHERE id = log_id;
    
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================================================
-- PASO 5: HABILITAR ROW LEVEL SECURITY (RLS)
-- ============================================================================

ALTER TABLE obras ENABLE ROW LEVEL SECURITY;
ALTER TABLE comentarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE validaciones ENABLE ROW LEVEL SECURITY;
ALTER TABLE historial_validaciones ENABLE ROW LEVEL SECURITY;
ALTER TABLE perfiles_usuarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE logs_errores ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- PASO 6: CREAR POLÍTICAS RLS
-- ============================================================================

-- OBRAS: Lectura pública, escritura solo para admins
DROP POLICY IF EXISTS "obras_lectura_publica" ON obras;
CREATE POLICY "obras_lectura_publica"
ON obras FOR SELECT
USING (true);

DROP POLICY IF EXISTS "obras_admin_insertar" ON obras;
CREATE POLICY "obras_admin_insertar"
ON obras FOR INSERT
WITH CHECK (
    EXISTS (
        SELECT 1 FROM perfiles_usuarios
        WHERE id = auth.uid() AND rol = 'admin'
    )
);

DROP POLICY IF EXISTS "obras_admin_actualizar" ON obras;
CREATE POLICY "obras_admin_actualizar"
ON obras FOR UPDATE
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

DROP POLICY IF EXISTS "obras_admin_eliminar" ON obras;
CREATE POLICY "obras_admin_eliminar"
ON obras FOR DELETE
USING (
    EXISTS (
        SELECT 1 FROM perfiles_usuarios
        WHERE id = auth.uid() AND rol = 'admin'
    )
);

-- COMENTARIOS: Lectura pública, creación autenticados, edición propia, admins pueden marcar como visto
DROP POLICY IF EXISTS "comentarios_lectura_publica" ON comentarios;
CREATE POLICY "comentarios_lectura_publica"
ON comentarios FOR SELECT
USING (true);

DROP POLICY IF EXISTS "comentarios_crear_autenticado" ON comentarios;
CREATE POLICY "comentarios_crear_autenticado"
ON comentarios FOR INSERT
WITH CHECK (auth.role() = 'authenticated');

DROP POLICY IF EXISTS "comentarios_editar_propio" ON comentarios;
CREATE POLICY "comentarios_editar_propio"
ON comentarios FOR UPDATE
USING (auth.uid() = usuario_id)
WITH CHECK (auth.uid() = usuario_id);

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

DROP POLICY IF EXISTS "comentarios_borrar_propio" ON comentarios;
CREATE POLICY "comentarios_borrar_propio"
ON comentarios FOR DELETE
USING (auth.uid() = usuario_id);

-- VALIDACIONES: Lectura pública, creación autenticados, edición propia (pendientes), admins aprueban
DROP POLICY IF EXISTS "validaciones_lectura_publica" ON validaciones;
CREATE POLICY "validaciones_lectura_publica"
ON validaciones FOR SELECT
USING (true);

DROP POLICY IF EXISTS "validaciones_crear_autenticado" ON validaciones;
CREATE POLICY "validaciones_crear_autenticado"
ON validaciones FOR INSERT
WITH CHECK (auth.role() = 'authenticated');

DROP POLICY IF EXISTS "validaciones_editar_propio" ON validaciones;
CREATE POLICY "validaciones_editar_propio"
ON validaciones FOR UPDATE
USING (
    auth.uid() = usuario_id 
    AND estado = 'pendiente'
)
WITH CHECK (
    auth.uid() = usuario_id 
    AND estado = 'pendiente'
);

DROP POLICY IF EXISTS "validaciones_admin_aprobar" ON validaciones;
CREATE POLICY "validaciones_admin_aprobar"
ON validaciones FOR UPDATE
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

-- HISTORIAL: Solo lectura pública
DROP POLICY IF EXISTS "historial_lectura_publica" ON historial_validaciones;
CREATE POLICY "historial_lectura_publica"
ON historial_validaciones FOR SELECT
USING (true);

DROP POLICY IF EXISTS "historial_admin_insertar" ON historial_validaciones;
CREATE POLICY "historial_admin_insertar"
ON historial_validaciones FOR INSERT
WITH CHECK (
    EXISTS (
        SELECT 1 FROM perfiles_usuarios
        WHERE id = auth.uid() AND rol = 'admin'
    )
);

-- PERFILES: Lectura pública, creación propia, edición propia, admins editan cualquiera
DROP POLICY IF EXISTS "perfiles_lectura_publica" ON perfiles_usuarios;
CREATE POLICY "perfiles_lectura_publica"
ON perfiles_usuarios FOR SELECT
USING (true);

DROP POLICY IF EXISTS "perfiles_crear_propio" ON perfiles_usuarios;
CREATE POLICY "perfiles_crear_propio"
ON perfiles_usuarios FOR INSERT
WITH CHECK (auth.uid() = id);

DROP POLICY IF EXISTS "perfiles_editar_propio" ON perfiles_usuarios;
CREATE POLICY "perfiles_editar_propio"
ON perfiles_usuarios FOR UPDATE
USING (auth.uid() = id)
WITH CHECK (auth.uid() = id);

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

-- LOGS DE ERRORES: Creación autenticados, lectura solo admins, marcar visto solo admins
DROP POLICY IF EXISTS "logs_errores_crear_autenticado" ON logs_errores;
CREATE POLICY "logs_errores_crear_autenticado"
ON logs_errores FOR INSERT
WITH CHECK (auth.role() = 'authenticated');

DROP POLICY IF EXISTS "logs_errores_lectura_admin" ON logs_errores;
CREATE POLICY "logs_errores_lectura_admin"
ON logs_errores FOR SELECT
USING (
    EXISTS (
        SELECT 1 FROM perfiles_usuarios
        WHERE id = auth.uid() AND rol = 'admin'
    )
);

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
-- PASO 7: CREAR VISTAS ÚTILES
-- ============================================================================

-- Vista: Comentarios pendientes de revisar por admin
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

-- Vista: Logs de errores pendientes de revisar por admin
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
-- PASO 8: COMENTARIOS EN COLUMNAS (Documentación)
-- ============================================================================

COMMENT ON COLUMN obras.autor IS 'Información del autor como objeto JSON: {nombre, nombre_completo, fecha_nacimiento, fecha_muerte, epoca, biografia}';
COMMENT ON COLUMN obras.representaciones IS 'Array de representaciones como JSON: [{fecha, lugar, compania, ...}]';
COMMENT ON COLUMN obras.musica_conservada IS 'Indica si la música de la obra está conservada';
COMMENT ON COLUMN obras.mecenas IS 'Mecenas o patrocinador de la obra';

-- ============================================================================
-- FIN DEL SCRIPT
-- ============================================================================
-- ✅ Schema completo recreado
-- 
-- SIGUIENTE PASO: Restaurar los datos
-- Usa el script de Python: python scripts/sync_to_supabase.py
-- ============================================================================

