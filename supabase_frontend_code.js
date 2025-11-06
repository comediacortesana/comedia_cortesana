// ============================================================================
// CÓDIGO JAVASCRIPT PARA AÑADIR A index.html
// ============================================================================
// 
// INSTRUCCIONES:
// 1. Añade el script de Supabase ANTES del <script> principal
// 2. Copia la configuración y funciones de autenticación
// 3. Copia las funciones de comentarios
// 4. Modifica mostrarDetalleObra() para incluir comentarios
// 5. Añade los estilos CSS para comentarios
//
// Ver guía completa: GUIA_SUPABASE_PASO_A_PASO.md
// ============================================================================

// ============================================================================
// 1. AÑADIR EN EL <head> (antes del </head>):
// ============================================================================

<!-- Supabase Client -->
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>


// ============================================================================
// 2. AÑADIR DESPUÉS DE: let metadata = {};
// ============================================================================

// ============================================================================
// CONFIGURACIÓN SUPABASE
// ============================================================================
// ⚠️ REEMPLAZA ESTOS VALORES CON TUS CREDENCIALES DE SUPABASE
const SUPABASE_URL = 'https://kyxxpoewwjixbpcezays.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt5eHhwb2V3d2ppeGJwY2V6YXlzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI0MjAzMDksImV4cCI6MjA3Nzk5NjMwOX0.sIw7flVHQ00r3VwrhU7tvohVzKpb7LGtXVzG43FAP10';

// Inicializar cliente Supabase
const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Estado de autenticación
let usuarioActual = null;


// ============================================================================
// 3. FUNCIONES DE AUTENTICACIÓN (añadir después de la configuración)
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


// ============================================================================
// 4. FUNCIONES DE COMENTARIOS (añadir después de las funciones de auth)
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


// ============================================================================
// 5. MODIFICAR window.onload (buscar y modificar):
// ============================================================================

// ANTES:
// window.onload = function() {
//     cargarDatos();
// };

// DESPUÉS:
window.onload = function() {
    verificarSesion(); // Verificar sesión primero
    cargarDatos();
};


// ============================================================================
// 6. MODIFICAR mostrarDetalleObra() - Añadir antes de modalBody.innerHTML = html:
// ============================================================================

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

// Y DESPUÉS de modalBody.innerHTML = html; añadir:
            // Cargar comentarios después de mostrar el modal
            mostrarComentariosEnModal(obra.id);


// ============================================================================
// 7. AÑADIR ESTILOS CSS (en la sección <style>, antes de </style>):
// ============================================================================

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

