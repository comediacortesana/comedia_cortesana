-- ============================================================================
-- SUPABASE: Script SQL Completo
-- ============================================================================
-- Ejecuta este script completo en Supabase SQL Editor
-- Paso a paso: https://github.com/.../GUIA_SUPABASE_PASO_A_PASO.md

-- ============================================================================
-- TABLA: obras
-- Sincronizada desde Google Sheets
-- ============================================================================
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

-- Índices para búsquedas rápidas
CREATE INDEX IF NOT EXISTS idx_obras_titulo ON obras USING gin(to_tsvector('spanish', titulo));
CREATE INDEX IF NOT EXISTS idx_obras_autor ON obras(autor_nombre);
CREATE INDEX IF NOT EXISTS idx_obras_fuente ON obras(fuente);

-- ============================================================================
-- TABLA: comentarios
-- Comentarios de usuarios sobre obras
-- ============================================================================
CREATE TABLE IF NOT EXISTS comentarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    obra_id INTEGER NOT NULL REFERENCES obras(id) ON DELETE CASCADE,
    usuario_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    contenido TEXT NOT NULL,
    tipo TEXT DEFAULT 'comentario',
    estado TEXT DEFAULT 'pendiente',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_comentarios_obra ON comentarios(obra_id);
CREATE INDEX IF NOT EXISTS idx_comentarios_usuario ON comentarios(usuario_id);

-- ============================================================================
-- TABLA: validaciones
-- Validaciones de usuarios sobre campos de obras
-- ============================================================================
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

CREATE INDEX IF NOT EXISTS idx_validaciones_obra ON validaciones(obra_id);
CREATE INDEX IF NOT EXISTS idx_validaciones_usuario ON validaciones(usuario_id);
CREATE INDEX IF NOT EXISTS idx_validaciones_estado ON validaciones(estado);

-- ============================================================================
-- TABLA: historial_validaciones
-- Historial de cambios aprobados (auditoría)
-- ============================================================================
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

CREATE INDEX IF NOT EXISTS idx_historial_obra ON historial_validaciones(obra_id);
CREATE INDEX IF NOT EXISTS idx_historial_usuario ON historial_validaciones(usuario_id);

-- ============================================================================
-- TABLA: perfiles_usuarios
-- Información adicional de usuarios
-- ============================================================================
CREATE TABLE IF NOT EXISTS perfiles_usuarios (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    nombre_completo TEXT,
    rol TEXT DEFAULT 'colaborador',
    bio TEXT,
    avatar_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================================
-- FUNCIONES AUXILIARES
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

-- ============================================================================
-- ROW LEVEL SECURITY (RLS)
-- ============================================================================

-- Habilitar RLS
ALTER TABLE obras ENABLE ROW LEVEL SECURITY;
ALTER TABLE comentarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE validaciones ENABLE ROW LEVEL SECURITY;
ALTER TABLE historial_validaciones ENABLE ROW LEVEL SECURITY;
ALTER TABLE perfiles_usuarios ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- POLÍTICAS RLS
-- ============================================================================

-- OBRAS: Lectura pública
DROP POLICY IF EXISTS "obras_lectura_publica" ON obras;
CREATE POLICY "obras_lectura_publica"
ON obras FOR SELECT
USING (true);

-- COMENTARIOS
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

DROP POLICY IF EXISTS "comentarios_borrar_propio" ON comentarios;
CREATE POLICY "comentarios_borrar_propio"
ON comentarios FOR DELETE
USING (auth.uid() = usuario_id);

-- VALIDACIONES
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

-- HISTORIAL
DROP POLICY IF EXISTS "historial_lectura_publica" ON historial_validaciones;
CREATE POLICY "historial_lectura_publica"
ON historial_validaciones FOR SELECT
USING (true);

-- PERFILES
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

-- Admins pueden editar cualquier perfil (para cambiar roles)
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

-- ============================================================================
-- TRIGGER: Crear perfil automáticamente al registrarse
-- ============================================================================

-- Función que se ejecuta cuando se crea un nuevo usuario
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

-- Trigger que ejecuta la función cuando se crea un usuario en auth.users
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

