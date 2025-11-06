# 📖 Guía Paso a Paso: Integración Supabase para Validación Colaborativa

## 🎯 Objetivo

Añadir validación colaborativa a tu aplicación estática usando Supabase, permitiendo que usuarios:
- ✅ Se registren e inicien sesión
- ✅ Dejen comentarios en obras
- ✅ Propongan validaciones/correcciones
- ✅ Vean su historial de contribuciones

**Tiempo estimado:** 45-60 minutos  
**Dificultad:** Intermedio (paso a paso)

---

## 📋 Requisitos Previos

Antes de empezar, asegúrate de tener:
- ✅ Una cuenta de Google (ya la tienes para Sheets)
- ✅ Una cuenta de GitHub (ya la tienes)
- ✅ Una cuenta de email para crear cuenta en Supabase
- ✅ Tu aplicación funcionando en GitHub Pages

---

## 🚀 PARTE 1: Crear Proyecto en Supabase

### Paso 1.1: Crear Cuenta en Supabase

1. **Ve a:** https://supabase.com
2. **Click en:** "Start your project" o "Sign Up"
3. **Regístrate** con tu email (puedes usar GitHub, Google, etc.)
4. **Confirma tu email** si es necesario

### Paso 1.2: Crear Nuevo Proyecto

1. **Click en:** "New Project"
2. **Completa el formulario:**
   - **Name:** `comedia-cortesana` (o el nombre que prefieras)
   - **Database Password:** ⚠️ **GUARDA ESTA CONTRASEÑA** (la necesitarás después)
   - **Region:** Elige la más cercana (ej: `Europe` para Europa, `West US` para América)
   - **Pricing Plan:** Selecciona **Free** (gratis)
   
   **⚠️ IMPORTANTE:** NO necesitas cambiar nada en las opciones avanzadas:
   - **Security Options** → Deja "Data API + Connection String" (por defecto) ✅
   - **Advanced Configuration** → Deja "Postgres" (por defecto) ✅
   
   Todo está bien configurado por defecto, solo haz click en "Create new project"

3. **Click en:** "Create new project"
4. **Espera 2-3 minutos** mientras se crea el proyecto

### Paso 1.3: Anotar Credenciales

Una vez creado el proyecto, necesitas estas credenciales:

1. **Ve a:** Settings → API (en el menú lateral izquierdo)
2. **Click en:** "API Keys NEW" (en el menú lateral, justo debajo de "Data API")
   - ⚠️ NO estés en "Data API", sino en "API Keys NEW"
3. **Anota estas claves:**
   - **Project URL:** Lo encuentras en "Data API" → Campo "URL" (ej: `https://xxxxx.supabase.co`) ⚠️ GUARDA ESTO
   - **anon public key:** En "API Keys NEW" → Busca la key que dice "anon" o "public" → Click en "Copy" ⚠️ GUARDA ESTO (para frontend)
   - **service_role key:** En "API Keys NEW" → Busca la key que dice "service_role" → Click en "Copy" ⚠️ GUARDA ESTO (para Apps Script, MANTÉN SECRETO - NO la compartas)

**📝 Crea un archivo temporal con estas credenciales** (no lo subas a GitHub)

---

## 🗄️ PARTE 2: Crear Base de Datos

### Paso 2.1: Abrir SQL Editor

1. En Supabase, **click en:** "SQL Editor" (menú lateral izquierdo)
2. **Click en:** "New query"

### Paso 2.2: Ejecutar Script SQL

**Copia y pega este SQL completo** en el editor:

```sql
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
```

3. **Click en:** "Run" (botón en la esquina inferior derecha)
4. **Verifica** que aparezca "Success. No rows returned"

### Paso 2.3: Verificar Tablas Creadas

1. **Ve a:** "Table Editor" (menú lateral izquierdo)
2. **Deberías ver 5 tablas:**
   - ✅ `obras`
   - ✅ `comentarios`
   - ✅ `validaciones`
   - ✅ `historial_validaciones`
   - ✅ `perfiles_usuarios`

---

## 🔒 PARTE 3: Configurar Row Level Security (RLS)

### Paso 3.1: Habilitar RLS

**Ejecuta este SQL** en el SQL Editor:

```sql
-- ============================================================================
-- HABILITAR RLS EN TODAS LAS TABLAS
-- ============================================================================
ALTER TABLE obras ENABLE ROW LEVEL SECURITY;
ALTER TABLE comentarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE validaciones ENABLE ROW LEVEL SECURITY;
ALTER TABLE historial_validaciones ENABLE ROW LEVEL SECURITY;
ALTER TABLE perfiles_usuarios ENABLE ROW LEVEL SECURITY;
```

### Paso 3.2: Crear Políticas de Seguridad

**Ejecuta este SQL completo** (todas las políticas):

```sql
-- ============================================================================
-- OBRAS: Lectura pública, escritura solo desde Apps Script (service_role)
-- ============================================================================

-- Cualquiera puede leer obras (anon key)
DROP POLICY IF EXISTS "obras_lectura_publica" ON obras;
CREATE POLICY "obras_lectura_publica"
ON obras FOR SELECT
USING (true);

-- ============================================================================
-- COMENTARIOS: Usuarios autenticados pueden crear, todos pueden leer
-- ============================================================================

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

-- ============================================================================
-- VALIDACIONES: Usuarios autenticados pueden crear, todos pueden leer
-- ============================================================================

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

-- Admins pueden aprobar/rechazar validaciones
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

-- ============================================================================
-- HISTORIAL: Lectura pública, escritura solo desde triggers
-- ============================================================================

DROP POLICY IF EXISTS "historial_lectura_publica" ON historial_validaciones;
CREATE POLICY "historial_lectura_publica"
ON historial_validaciones FOR SELECT
USING (true);

-- ============================================================================
-- PERFILES: Lectura pública, edición propia
-- ============================================================================

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
```

3. **Click en:** "Run"
4. **Verifica:** "Success. No rows returned"

### Paso 3.3: Verificar Políticas

1. **Ve a:** Authentication → Policies
2. **Deberías ver** las políticas creadas para cada tabla

---

## 💻 PARTE 4: Integrar Frontend (HTML/JS)

### Paso 4.1: Añadir Script de Supabase

1. **Abre:** `index.html` en tu editor
2. **Busca:** La línea `<script>` donde empieza el JavaScript (alrededor de línea 487)
3. **ANTES de esa línea**, añade:

```html
<!-- Supabase Client -->
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
```

### Paso 4.2: Añadir Configuración de Supabase

**Justo después de las variables globales** (después de `let metadata = {};`), añade:

```javascript
// ============================================================================
// CONFIGURACIÓN SUPABASE
// ============================================================================
// ⚠️ REEMPLAZA ESTOS VALORES CON TUS CREDENCIALES DE SUPABASE
const SUPABASE_URL = 'https://TU-PROYECTO.supabase.co';
const SUPABASE_ANON_KEY = 'TU-ANON-KEY-AQUI';

// Inicializar cliente Supabase
const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Estado de autenticación
let usuarioActual = null;
```

### Paso 4.3: Añadir Funciones de Autenticación

**Añade estas funciones** después de la configuración de Supabase:

```javascript
// ============================================================================
// FUNCIONES DE AUTENTICACIÓN
// ============================================================================

// Verificar sesión al cargar
async function verificarSesion() {
    const { data: { session } } = await supabase.auth.getSession();
    if (session) {
        usuarioActual = session.user;
        mostrarUIUsuario();
    } else {
        mostrarUILogin();
    }
}

// Escuchar cambios de autenticación
supabase.auth.onAuthStateChange((event, session) => {
    if (event === 'SIGNED_IN') {
        usuarioActual = session.user;
        mostrarUIUsuario();
    } else if (event === 'SIGNED_OUT') {
        usuarioActual = null;
        mostrarUILogin();
    }
});

// Login con email/password
async function login(email, password) {
    const { data, error } = await supabase.auth.signInWithPassword({
        email: email,
        password: password
    });
    
    if (error) {
        console.error('Error de login:', error);
        alert('Error: ' + error.message);
        return false;
    }
    
    usuarioActual = data.user;
    mostrarUIUsuario();
    return true;
}

// Registro
async function registro(email, password, nombreCompleto) {
    const { data, error } = await supabase.auth.signUp({
        email: email,
        password: password,
        options: {
            data: {
                nombre_completo: nombreCompleto
            }
        }
    });
    
    if (error) {
        console.error('Error de registro:', error);
        alert('Error: ' + error.message);
        return false;
    }
    
    // Crear perfil
    if (data.user) {
        await crearPerfilUsuario(data.user.id, nombreCompleto);
    }
    
    alert('¡Registro exitoso! Revisa tu email para confirmar.');
    return true;
}

// Magic Link (sin contraseña)
async function loginMagicLink(email) {
    const { error } = await supabase.auth.signInWithOtp({
        email: email,
        options: {
            emailRedirectTo: window.location.href
        }
    });
    
    if (error) {
        console.error('Error:', error);
        alert('Error: ' + error.message);
        return false;
    }
    
    alert('¡Revisa tu email para el enlace de acceso!');
    return true;
}

// Logout
async function logout() {
    await supabase.auth.signOut();
    usuarioActual = null;
    mostrarUILogin();
}

// Crear perfil de usuario
async function crearPerfilUsuario(userId, nombreCompleto) {
    const { error } = await supabase
        .from('perfiles_usuarios')
        .insert({
            id: userId,
            nombre_completo: nombreCompleto,
            rol: 'colaborador'
        });
    
    if (error && error.code !== '23505') { // Ignorar si ya existe
        console.error('Error creando perfil:', error);
    }
}

// Cargar perfil de usuario
async function cargarPerfilUsuario() {
    if (!usuarioActual) return;
    
    const { data } = await supabase
        .from('perfiles_usuarios')
        .select('nombre_completo')
        .eq('id', usuarioActual.id)
        .single();
    
    if (data) {
        const userNameElement = document.getElementById('user-name');
        if (userNameElement) {
            userNameElement.textContent = data.nombre_completo || usuarioActual.email;
        }
    }
}
```

### Paso 4.4: Añadir UI de Login

**Busca la línea:** `<div class="container">` (alrededor de línea 350)

**Justo DESPUÉS de esa línea**, añade:

```html
<!-- Sección de Autenticación -->
<div id="auth-section" style="margin-bottom: 20px; padding: 15px; background: #f0f0f0; border-radius: 5px;">
    <!-- Estado: No autenticado -->
    <div id="login-ui" style="display: none;">
        <h3 style="margin-bottom: 10px;">🔐 Iniciar Sesión</h3>
        <div style="display: flex; gap: 10px; flex-wrap: wrap; align-items: center;">
            <input type="email" id="login-email" placeholder="Email" style="padding: 8px; border-radius: 4px; border: 1px solid #ddd;">
            <input type="password" id="login-password" placeholder="Contraseña" style="padding: 8px; border-radius: 4px; border: 1px solid #ddd;">
            <button onclick="handleLogin()" style="padding: 8px 15px; background: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer;">Entrar</button>
            <button onclick="handleMagicLink()" style="padding: 8px 15px; background: #95a5a6; color: white; border: none; border-radius: 4px; cursor: pointer;">Enlace mágico</button>
            <button onclick="mostrarRegistro()" style="padding: 8px 15px; background: #27ae60; color: white; border: none; border-radius: 4px; cursor: pointer;">Registrarse</button>
        </div>
        
        <!-- Formulario de registro (oculto por defecto) -->
        <div id="registro-form" style="display: none; margin-top: 15px; padding: 15px; background: white; border-radius: 4px;">
            <h4>Nuevo Usuario</h4>
            <input type="text" id="registro-nombre" placeholder="Nombre completo" style="padding: 8px; width: 200px; margin-right: 10px; border-radius: 4px; border: 1px solid #ddd;">
            <input type="email" id="registro-email" placeholder="Email" style="padding: 8px; width: 200px; margin-right: 10px; border-radius: 4px; border: 1px solid #ddd;">
            <input type="password" id="registro-password" placeholder="Contraseña" style="padding: 8px; width: 200px; margin-right: 10px; border-radius: 4px; border: 1px solid #ddd;">
            <button onclick="handleRegistro()" style="padding: 8px 15px; background: #27ae60; color: white; border: none; border-radius: 4px; cursor: pointer;">Registrar</button>
            <button onclick="ocultarRegistro()" style="padding: 8px 15px; background: #95a5a6; color: white; border: none; border-radius: 4px; cursor: pointer;">Cancelar</button>
        </div>
    </div>
    
    <!-- Estado: Autenticado -->
    <div id="user-ui" style="display: none;">
        <span>👤 <strong id="user-name">Usuario</strong></span>
        <button onclick="logout()" style="margin-left: 10px; padding: 8px 15px; background: #e74c3c; color: white; border: none; border-radius: 4px; cursor: pointer;">Salir</button>
    </div>
</div>
```

### Paso 4.5: Añadir Funciones de UI

**Añade estas funciones** después de las funciones de autenticación:

```javascript
// Funciones de UI
function mostrarUIUsuario() {
    document.getElementById('login-ui').style.display = 'none';
    document.getElementById('user-ui').style.display = 'block';
    cargarPerfilUsuario();
}

function mostrarUILogin() {
    document.getElementById('login-ui').style.display = 'block';
    document.getElementById('user-ui').style.display = 'none';
}

function mostrarRegistro() {
    document.getElementById('registro-form').style.display = 'block';
}

function ocultarRegistro() {
    document.getElementById('registro-form').style.display = 'none';
}

function handleLogin() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    if (!email || !password) {
        alert('Ingresa email y contraseña');
        return;
    }
    login(email, password);
}

function handleRegistro() {
    const nombre = document.getElementById('registro-nombre').value;
    const email = document.getElementById('registro-email').value;
    const password = document.getElementById('registro-password').value;
    if (!nombre || !email || !password) {
        alert('Completa todos los campos');
        return;
    }
    registro(email, password, nombre);
}

function handleMagicLink() {
    const email = document.getElementById('login-email').value;
    if (!email) {
        alert('Ingresa tu email');
        return;
    }
    loginMagicLink(email);
}
```

### Paso 4.6: Llamar verificarSesion() al Cargar

**Busca la función:** `window.onload` (alrededor de línea 1077)

**Modifícala** para incluir verificación de sesión:

```javascript
// Cargar datos iniciales
window.onload = function() {
    verificarSesion(); // Verificar sesión primero
    cargarDatos();
};
```

---

## 💬 PARTE 5: Añadir Comentarios al Modal

### Paso 5.1: Añadir Funciones de Comentarios

**Añade estas funciones** después de las funciones de autenticación:

```javascript
// ============================================================================
// FUNCIONES DE COMENTARIOS
// ============================================================================

// Cargar comentarios de una obra
async function cargarComentarios(obraId) {
    const { data, error } = await supabase
        .from('comentarios')
        .select(`
            *,
            perfiles_usuarios (
                nombre_completo,
                avatar_url
            )
        `)
        .eq('obra_id', obraId)
        .order('created_at', { ascending: false });
    
    if (error) {
        console.error('Error cargando comentarios:', error);
        return [];
    }
    
    return data || [];
}

// Crear comentario
async function crearComentario(obraId, contenido, tipo = 'comentario') {
    if (!usuarioActual) {
        alert('Debes iniciar sesión para comentar');
        return false;
    }
    
    const { data, error } = await supabase
        .from('comentarios')
        .insert({
            obra_id: obraId,
            usuario_id: usuarioActual.id,
            contenido: contenido,
            tipo: tipo
        })
        .select()
        .single();
    
    if (error) {
        console.error('Error creando comentario:', error);
        alert('Error: ' + error.message);
        return false;
    }
    
    return data;
}

// Renderizar comentarios en el modal
async function mostrarComentariosEnModal(obraId) {
    const comentarios = await cargarComentarios(obraId);
    const container = document.getElementById('comentarios-container');
    
    if (!container) return;
    
    if (comentarios.length === 0) {
        container.innerHTML = '<p style="color: #999; padding: 10px;">No hay comentarios aún.</p>';
        return;
    }
    
    let html = '<div class="comentarios-list">';
    comentarios.forEach(comentario => {
        const fecha = new Date(comentario.created_at).toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
        const nombre = comentario.perfiles_usuarios?.nombre_completo || 'Usuario';
        html += `
            <div class="comentario-item">
                <div class="comentario-header">
                    <strong>${escapeHtml(nombre)}</strong>
                    <span class="comentario-fecha">${fecha}</span>
                </div>
                <div class="comentario-contenido">${escapeHtml(comentario.contenido)}</div>
                <div class="comentario-tipo">${comentario.tipo}</div>
            </div>
        `;
    });
    html += '</div>';
    
    container.innerHTML = html;
}

// Función helper para escapar HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Enviar comentario
async function enviarComentario(obraId) {
    const texto = document.getElementById('comentario-texto');
    if (!texto || !texto.value.trim()) {
        alert('Escribe un comentario');
        return;
    }
    
    const resultado = await crearComentario(obraId, texto.value.trim());
    if (resultado) {
        texto.value = '';
        await mostrarComentariosEnModal(obraId);
    }
}
```

### Paso 5.2: Modificar mostrarDetalleObra()

**Busca la función:** `mostrarDetalleObra()` (alrededor de línea 788)

**Justo ANTES de la línea:** `modalBody.innerHTML = html;` (alrededor de línea 953)

**Añade esta sección de comentarios:**

```javascript
            // Sección de Comentarios (añadir antes de modalBody.innerHTML = html)
            html += '<div class="field-section">';
            html += '<div class="section-title">💬 Comentarios y Validaciones</div>';
            
            // Formulario de comentario (solo si está autenticado)
            if (usuarioActual) {
                html += '<div id="comentario-form" style="margin-bottom: 20px;">';
                html += '<textarea id="comentario-texto" placeholder="Escribe un comentario sobre esta obra..." style="width: 100%; padding: 10px; border-radius: 4px; border: 1px solid #ddd; min-height: 80px; font-family: inherit;"></textarea>';
                html += '<button onclick="enviarComentario(' + obra.id + ')" style="margin-top: 10px; padding: 8px 15px; background: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer;">Enviar Comentario</button>';
                html += '</div>';
            } else {
                html += '<p style="color: #999; padding: 10px;">Inicia sesión para dejar comentarios</p>';
            }
            
            // Contenedor de comentarios
            html += '<div id="comentarios-container">';
            html += '<p style="color: #999; padding: 10px;">Cargando comentarios...</p>';
            html += '</div>';
            html += '</div>';
```

**Y justo DESPUÉS de:** `modalBody.innerHTML = html;`

**Añade:**

```javascript
            // Cargar comentarios después de mostrar el modal
            mostrarComentariosEnModal(obra.id);
```

### Paso 5.3: Añadir Estilos CSS para Comentarios

**Busca la sección:** `<style>` (alrededor de línea 7)

**Al final de los estilos**, antes de `</style>`, añade:

```css
        /* Estilos para Comentarios */
        .comentarios-list {
            max-height: 400px;
            overflow-y: auto;
        }
        
        .comentario-item {
            background: #f8f9fa;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 5px;
            border-left: 3px solid #3498db;
        }
        
        .comentario-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 13px;
        }
        
        .comentario-fecha {
            color: #999;
            font-size: 12px;
        }
        
        .comentario-contenido {
            color: #333;
            line-height: 1.5;
            margin-bottom: 8px;
        }
        
        .comentario-tipo {
            display: inline-block;
            background: #e3f2fd;
            color: #1976d2;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 11px;
            font-weight: 600;
        }
        
        #comentario-form textarea {
            resize: vertical;
        }
```

---

## 🔄 PARTE 6: Configurar Apps Script para Sincronizar con Supabase

### Paso 6.1: Añadir Funciones de Sincronización

**Abre:** `sheets-github-sync.gs` en Apps Script

**Al final del archivo**, antes de las funciones de testing, añade:

```javascript
// ============================================================================
// SINCRONIZACIÓN CON SUPABASE
// ============================================================================

/**
 * Sincroniza Google Sheets con Supabase
 * Ejecutar después de syncToGitHub() o en paralelo
 */
function syncToSupabase() {
  try {
    log('🚀 Iniciando sincronización con Supabase...', 'INFO');
    
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = spreadsheet.getSheetByName('obras_completas');
    
    if (!sheet) {
      throw new Error('Hoja "obras_completas" no encontrada');
    }
    
    // Leer datos de la hoja
    const data = readSheetData(sheet);
    
    if (data.length === 0) {
      log('⚠️ La hoja está vacía', 'WARN');
      return;
    }
    
    // Convertir a objetos
    const headers = data[0];
    const obras = data.slice(1).map(row => {
      const obj = {};
      headers.forEach((header, index) => {
        obj[header] = row[index] || null;
      });
      return obj;
    });
    
    log(`📊 ${obras.length} obras procesadas`, 'INFO');
    
    // Configuración de Supabase
    const SUPABASE_URL = 'https://TU-PROYECTO.supabase.co'; // ⚠️ REEMPLAZAR
    const serviceKey = getSupabaseServiceKey();
    
    // Sincronizar cada obra
    let successCount = 0;
    let errorCount = 0;
    
    for (const obra of obras) {
      try {
        await syncObraToSupabase(obra, SUPABASE_URL, serviceKey);
        successCount++;
      } catch (error) {
        log(`❌ Error sincronizando obra ${obra.ID}: ${error.message}`, 'ERROR');
        errorCount++;
      }
    }
    
    log(`✅ Sincronización completada: ${successCount} exitosas, ${errorCount} errores`, 'INFO');
    
  } catch (error) {
    log(`❌ Error general: ${error.message}`, 'ERROR');
    throw error;
  }
}

/**
 * Sincroniza una obra individual con Supabase
 */
function syncObraToSupabase(obra, supabaseUrl, serviceKey) {
  const obraId = obra.ID || obra.id;
  if (!obraId) {
    throw new Error('Obra sin ID');
  }
  
  const url = `${supabaseUrl}/rest/v1/obras?id=eq.${obraId}`;
  
  // Verificar si existe
  const checkResponse = UrlFetchApp.fetch(url, {
    method: 'GET',
    headers: {
      'apikey': serviceKey,
      'Authorization': `Bearer ${serviceKey}`,
      'Content-Type': 'application/json'
    }
  });
  
  const existing = JSON.parse(checkResponse.getContentText());
  
  // Mapear campos del Sheet a la tabla de Supabase
  const obraData = {
    id: obraId,
    titulo: obra['Título'] || obra['T?tulo'] || null,
    titulo_original: obra['Título Original'] || obra['T?tulo Original'] || null,
    tipo_obra: obra['Tipo de Obra'] || null,
    autor_nombre: obra['Autor'] || null,
    fuente: obra['Fuente Principal'] || obra['Fuente'] || null,
    fecha_creacion: obra['Fecha de Creación'] || null,
    synced_from_sheet_at: new Date().toISOString()
  };
  
  if (existing && existing.length > 0) {
    // Actualizar existente
    const updateUrl = `${supabaseUrl}/rest/v1/obras?id=eq.${obraId}`;
    const updateResponse = UrlFetchApp.fetch(updateUrl, {
      method: 'PATCH',
      headers: {
        'apikey': serviceKey,
        'Authorization': `Bearer ${serviceKey}`,
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
      },
      payload: JSON.stringify(obraData)
    });
    
    if (updateResponse.getResponseCode() !== 204 && updateResponse.getResponseCode() !== 200) {
      throw new Error(`Error actualizando: ${updateResponse.getContentText()}`);
    }
  } else {
    // Insertar nuevo
    const insertUrl = `${supabaseUrl}/rest/v1/obras`;
    const insertResponse = UrlFetchApp.fetch(insertUrl, {
      method: 'POST',
      headers: {
        'apikey': serviceKey,
        'Authorization': `Bearer ${serviceKey}`,
        'Content-Type': 'application/json',
        'Prefer': 'return=minimal'
      },
      payload: JSON.stringify(obraData)
    });
    
    if (insertResponse.getResponseCode() !== 201 && insertResponse.getResponseCode() !== 200) {
      throw new Error(`Error insertando: ${insertResponse.getContentText()}`);
    }
  }
}

/**
 * Obtiene la service key de Supabase de forma segura
 */
function getSupabaseServiceKey() {
  const properties = PropertiesService.getScriptProperties();
  const key = properties.getProperty('SUPABASE_SERVICE_KEY');
  
  if (!key) {
    throw new Error('SUPABASE_SERVICE_KEY no configurado. Usa setSupabaseServiceKey()');
  }
  
  return key;
}

/**
 * Guarda la service key de Supabase
 */
function setSupabaseServiceKey() {
  const ui = SpreadsheetApp.getUi();
  const result = ui.prompt(
    'Configurar Supabase Service Key',
    'Ingresa tu Service Role Key de Supabase:\n\n' +
    '⚠️ Esta key tiene permisos completos. Manténla segura.\n\n' +
    'Encuéntrala en: Supabase → Settings → API → service_role key',
    ui.ButtonSet.OK_CANCEL
  );
  
  if (result.getSelectedButton() === ui.Button.OK) {
    const key = result.getResponseText().trim();
    PropertiesService.getScriptProperties().setProperty('SUPABASE_SERVICE_KEY', key);
    ui.alert('✅ Service Key guardada exitosamente');
  }
}

/**
 * Función combinada: Sincroniza a GitHub Y Supabase
 */
function syncToGitHubAndSupabase() {
  log('🔄 Sincronizando a GitHub y Supabase...', 'INFO');
  
  // Primero GitHub (como antes)
  const githubResults = syncToGitHub();
  
  // Luego Supabase
  try {
    syncToSupabase();
  } catch (error) {
    log(`⚠️ Error en Supabase (GitHub OK): ${error.message}`, 'WARN');
  }
  
  return githubResults;
}
```

### Paso 6.2: Configurar Service Key

1. **En Apps Script**, ejecuta la función: `setSupabaseServiceKey()`
2. **Pega tu service_role key** de Supabase
3. **Click en:** OK

### Paso 6.3: Actualizar CONFIG para Supabase

**En la sección CONFIG**, añade:

```javascript
  // Configuración de Supabase
  supabase: {
    url: 'https://TU-PROYECTO.supabase.co',  // ⚠️ REEMPLAZAR
    enabled: true                            // true para habilitar sync con Supabase
  },
```

### Paso 6.4: Actualizar Función Principal (Opcional)

**Modifica `syncToGitHub()`** para que también sincronice con Supabase si está habilitado:

```javascript
function syncToGitHub() {
  // ... código existente ...
  
  // Al final, antes de return results:
  
  // Sincronizar con Supabase si está habilitado
  if (CONFIG.supabase && CONFIG.supabase.enabled) {
    try {
      syncToSupabase();
    } catch (error) {
      log(`⚠️ Error en Supabase: ${error.message}`, 'WARN');
    }
  }
  
  return results;
}
```

---

## ✅ PARTE 7: Probar Todo

### Paso 7.1: Probar Registro de Usuario

1. **Abre tu sitio** en GitHub Pages
2. **Click en:** "Registrarse"
3. **Completa el formulario:**
   - Nombre completo
   - Email
   - Contraseña
4. **Click en:** "Registrar"
5. **Revisa tu email** y confirma la cuenta
6. **Inicia sesión** con tus credenciales

### Paso 7.2: Probar Comentarios

1. **Inicia sesión** en tu sitio
2. **Click en una obra** para abrir el modal
3. **Desplázate** hasta la sección "Comentarios"
4. **Escribe un comentario** y click en "Enviar Comentario"
5. **Verifica** que el comentario aparece

### Paso 7.3: Verificar en Supabase

1. **Ve a Supabase** → Table Editor
2. **Abre la tabla:** `comentarios`
3. **Deberías ver** tu comentario ahí

### Paso 7.4: Probar Sincronización desde Sheets

1. **En Apps Script**, ejecuta: `syncToSupabase()`
2. **Revisa los logs** para ver el progreso
3. **Ve a Supabase** → Table Editor → `obras`
4. **Deberías ver** las obras sincronizadas

---

## 🎉 ¡Listo!

Ya tienes:
- ✅ Autenticación de usuarios
- ✅ Comentarios en obras
- ✅ Sincronización Sheets → Supabase
- ✅ Base de datos segura con RLS

---

## 📝 Próximos Pasos (Opcional)

1. **Añadir validaciones:** Permite que usuarios propongan cambios
2. **Panel de admin:** Para revisar y aprobar validaciones
3. **Notificaciones:** Email cuando se aprueba una validación
4. **Estadísticas:** Contador de comentarios por obra

---

## ❓ Troubleshooting

### Error: "Invalid API key"
- Verifica que copiaste correctamente las keys de Supabase
- Asegúrate de usar `anon key` en el frontend y `service_role key` en Apps Script

### Error: "Row Level Security policy violation"
- Verifica que ejecutaste todas las políticas RLS del Paso 3.2
- Asegúrate de estar autenticado para crear comentarios

### Los comentarios no aparecen
- Abre la consola del navegador (F12) y revisa errores
- Verifica que el `obra_id` coincide con el ID de la obra

### La sincronización falla
- Verifica que configuraste `setSupabaseServiceKey()` correctamente
- Revisa los logs en Apps Script para ver el error específico

---

**¿Necesitas ayuda?** Revisa los logs en la consola del navegador (F12) y en Apps Script.

