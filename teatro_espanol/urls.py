"""
URL configuration for teatro_espanol project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.http import FileResponse, Http404, HttpResponse
from django.views.decorators.http import require_http_methods
from pathlib import Path
from django.shortcuts import render
import mimetypes

@require_http_methods(["GET"])
def home_view(request):
    """Vista de inicio que muestra información del proyecto"""
    # Obtener comentarios recientes
    from apps.obras.models import ComentarioUsuario
    from apps.obras.models import Obra
    from apps.autores.models import Autor
    from apps.lugares.models import Lugar
    from apps.representaciones.models import Representacion
    comentarios_recientes = ComentarioUsuario.objects.filter(
        es_publico=True
    ).select_related('usuario').prefetch_related('obras_seleccionadas').order_by('-fecha_creacion')[:5]
    total_obras = Obra.objects.count()
    total_autores = Autor.objects.count()
    total_lugares = Lugar.objects.count()
    total_representaciones = Representacion.objects.count()
    
    # Información del usuario autenticado - MINIMALISTA
    user_info = ""
    if request.user.is_authenticated:
        user_info = f"""
            <div style="font-size: 0.9rem;">
                <span style="color: var(--warm-red-dark); font-weight: 500;">👋 {request.user.get_full_name()}</span>
                <div style="margin-top: 5px;">
                    <a href="/usuarios/perfil/" style="color: var(--warm-red); text-decoration: none; margin-right: 15px; font-size: 0.8rem;">Perfil</a>
                    <a href="/usuarios/logout/" style="color: var(--warm-red); text-decoration: none; font-size: 0.8rem;">Salir</a>
                </div>
            </div>
        """
    else:
        user_info = """
            <div style="font-size: 0.9rem;">
                <div>
                    <a href="/usuarios/login/" style="color: var(--warm-red); text-decoration: none; margin-right: 15px; font-size: 0.8rem;">Iniciar Sesión</a>
                    <a href="/usuarios/registro/" style="color: var(--warm-red); text-decoration: none; font-size: 0.8rem;">Registrarse</a>
                </div>
            </div>
        """
    
    # Construir HTML de comentarios
    comentarios_html = ""
    if comentarios_recientes:
        # Contar comentarios públicos y con etiqueta IA
        total_publicos = ComentarioUsuario.objects.filter(es_publico=True).count()
        total_ia = ComentarioUsuario.objects.filter(etiqueta_ia=True).count()
        
        comentarios_html = f"""
            <div class="comentarios-section">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h2 class="nav-title" style="margin: 0;">💬 Comentarios de la Comunidad</h2>
                    <div style="display: flex; gap: 10px;">
                        <a href="/obras/comentarios/exportar-todos/" class="admin-btn" style="font-size: 0.8rem; padding: 8px 16px;">
                            📥 Descargar Todos ({total_publicos})
                        </a>
                        <a href="/obras/comentarios/exportar-ia/" class="admin-btn" style="font-size: 0.8rem; padding: 8px 16px; background: #27ae60;">
                            🤖 Descargar IA ({total_ia})
                        </a>
                    </div>
                </div>
        """
        for comentario in comentarios_recientes:
            obras_count = comentario.obras_seleccionadas.count()
            fecha = comentario.fecha_creacion.strftime('%d/%m/%Y %H:%M')
            username = comentario.usuario.get_full_name() or comentario.usuario.username
            
            # Truncar comentario si es muy largo
            comentario_text = comentario.comentario
            if len(comentario_text) > 200:
                comentario_text = comentario_text[:200] + "..."
            
            # Obtener las obras asociadas con sus enlaces
            obras_enlaces = []
            for obra in comentario.obras_seleccionadas.all():
                obras_enlaces.append(f'<a href="/obras/{obra.id}/" class="obra-link">{obra.titulo_limpio or obra.titulo}</a>')
            
            obras_html = ', '.join(obras_enlaces) if obras_enlaces else 'Sin obras asociadas'
            
            comentarios_html += f"""
                <div class="comentario-card">
                    <div class="comentario-header">
                        <div class="comentario-user">
                            <span class="user-icon">👤</span>
                            <strong>{username}</strong>
                        </div>
                        <div class="comentario-fecha">{fecha}</div>
                    </div>
                    <div class="comentario-titulo">{comentario.titulo}</div>
                    <div class="comentario-texto">{comentario_text}</div>
                    <div class="comentario-footer">
                        <div class="obras-asociadas">
                            <span class="obras-label">📚 Obras:</span>
                            <div class="obras-links">{obras_html}</div>
                        </div>
                        <span class="comentario-badge">🗂️ {comentario.catalogo.upper()}</span>
                    </div>
                </div>
            """
        
        comentarios_html += "</div>"
    else:
        # Contar comentarios aunque no haya públicos
        total_publicos = ComentarioUsuario.objects.filter(es_publico=True).count()
        total_ia = ComentarioUsuario.objects.filter(etiqueta_ia=True).count()
        
        comentarios_html = f"""
            <div class="comentarios-section">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h2 class="nav-title" style="margin: 0;">💬 Comentarios de la Comunidad</h2>
                    <div style="display: flex; gap: 10px;">
                        <a href="/obras/comentarios/exportar-todos/" class="admin-btn" style="font-size: 0.8rem; padding: 8px 16px;">
                            📥 Descargar Todos ({total_publicos})
                        </a>
                        <a href="/obras/comentarios/exportar-ia/" class="admin-btn" style="font-size: 0.8rem; padding: 8px 16px; background: #27ae60;">
                            🤖 Descargar IA ({total_ia})
                        </a>
                    </div>
                </div>
                <div class="empty-comentarios">
                    <p style="text-align: center; color: var(--text-medium); padding: 30px;">
                        📝 Aún no hay comentarios públicos. ¡Sé el primero en compartir tus descubrimientos!
                    </p>
                </div>
            </div>
        """
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Teatro Español del Siglo de Oro</title>
        <style>
            /* Colores principales */
            :root {{
                --beige-bg: #F5E6D3;
                --beige-light: #FAF3E9;
                --warm-red: #C17767;
                --warm-red-dark: #A55E4F;
                --warm-red-light: #D98B7A;
                --text-dark: #4A3428;
                --text-medium: #7A6552;
                --border-color: #E0D4C4;
            }}

            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 0; 
                padding: 0; 
                background: var(--beige-bg);
                color: var(--text-dark);
                min-height: 100vh;
            }}
            
            .container {{ 
                max-width: 1200px; 
                margin: 0 auto; 
                background: var(--beige-light);
                border: 2px solid var(--warm-red);
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 4px 20px rgba(193, 119, 103, 0.15);
                margin: 20px;
            }}
            
            /* BARRA SUPERIOR MINIMALISTA */
            .top-bar {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px 0;
                margin-bottom: 20px;
                border-bottom: 1px solid var(--border-color);
            }}
            
            .logo {{
                font-size: 1.5rem;
                font-weight: 600;
                color: var(--warm-red-dark);
                text-decoration: none;
            }}
            
            .user-info {{
                font-size: 0.9rem;
                color: var(--text-medium);
            }}
            
            /* TÍTULO PRINCIPAL */
            .main-title {{
                text-align: center;
                color: var(--warm-red-dark);
                margin: 30px 0;
                font-size: 2rem;
                font-weight: 300;
                letter-spacing: 1px;
            }}
            
            /* ESTADÍSTICAS COMPACTAS */
            .stats {{
                display: flex;
                justify-content: center;
                gap: 20px;
                margin: 30px 0;
                flex-wrap: wrap;
            }}
            
            .stat-item {{
                text-align: center;
                padding: 15px 20px;
                background: white;
                border-radius: 8px;
                border: 1px solid var(--warm-red-light);
                min-width: 100px;
            }}
            
            .stat-number {{
                font-size: 1.5rem;
                font-weight: bold;
                color: var(--warm-red-dark);
                display: block;
            }}
            
            .stat-label {{
                font-size: 0.8rem;
                color: var(--text-medium);
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-top: 5px;
            }}
            
            /* NAVEGACIÓN PRINCIPAL */
            .nav-section {{
                margin: 40px 0;
            }}
            
            .nav-title {{
                text-align: center;
                color: var(--warm-red-dark);
                font-size: 1.2rem;
                font-weight: 500;
                margin-bottom: 20px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            
            .nav-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 15px;
            }}
            
            .nav-link {{
                display: block;
                background: white;
                color: var(--text-dark);
                text-decoration: none;
                padding: 20px;
                border-radius: 10px;
                border: 1px solid var(--warm-red-light);
                transition: all 0.3s ease;
                text-align: center;
            }}
            
            .nav-link:hover {{
                background: #FFF9F5;
                border-color: var(--warm-red);
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(193, 119, 103, 0.2);
            }}
            
            .nav-link-title {{
                font-weight: 600;
                color: var(--warm-red-dark);
                font-size: 1rem;
                margin-bottom: 5px;
            }}
            
            .nav-link-desc {{
                font-size: 0.85rem;
                color: var(--text-medium);
            }}
            
            /* ADMIN SECTION */
            .admin-section {{
                text-align: center;
                margin: 30px 0;
                padding: 20px;
                background: white;
                border-radius: 10px;
                border: 1px solid var(--warm-red-light);
            }}
            
            .admin-btn {{
                display: inline-block;
                background: var(--warm-red);
                color: white;
                text-decoration: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: 500;
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                font-size: 0.9rem;
            }}
            
            .admin-btn:hover {{
                background: var(--warm-red-dark);
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(193, 119, 103, 0.3);
            }}
            
            /* INFO SECTION */
            .info-section {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid var(--warm-red);
                margin: 20px 0;
            }}
            
            .info-title {{
                color: var(--warm-red-dark);
                font-size: 1.1rem;
                font-weight: 600;
                margin-bottom: 10px;
            }}
            
            .info-text {{
                color: var(--text-medium);
                font-size: 0.9rem;
                line-height: 1.5;
            }}
            
            /* CREDENTIALS SECTION */
            .credentials {{
                background: #FFF9F5;
                padding: 15px;
                border-radius: 8px;
                border: 1px solid var(--border-color);
                margin: 15px 0;
            }}
            
            .credentials-title {{
                color: var(--warm-red-dark);
                font-size: 0.9rem;
                font-weight: 600;
                margin-bottom: 8px;
            }}
            
            .credentials-list {{
                font-size: 0.8rem;
                color: var(--text-medium);
                line-height: 1.4;
            }}
            
            /* COMENTARIOS SECTION */
            .comentarios-section {{
                margin: 30px 0;
            }}
            
            .comentario-card {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid var(--warm-red);
                margin: 15px 0;
                box-shadow: 0 2px 8px rgba(193, 119, 103, 0.1);
                transition: all 0.3s ease;
            }}
            
            .comentario-card:hover {{
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(193, 119, 103, 0.15);
            }}
            
            .comentario-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
                padding-bottom: 10px;
                border-bottom: 1px solid var(--border-color);
            }}
            
            .comentario-user {{
                display: flex;
                align-items: center;
                gap: 8px;
                color: var(--warm-red-dark);
                font-weight: 600;
            }}
            
            .user-icon {{
                font-size: 1.2rem;
            }}
            
            .comentario-fecha {{
                font-size: 0.75rem;
                color: var(--text-medium);
            }}
            
            .comentario-titulo {{
                font-size: 1rem;
                font-weight: 600;
                color: var(--text-dark);
                margin-bottom: 10px;
            }}
            
            .comentario-texto {{
                font-size: 0.9rem;
                color: var(--text-medium);
                line-height: 1.5;
                margin-bottom: 12px;
            }}
            
            .comentario-footer {{
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
                align-items: flex-start;
            }}
            
            .obras-asociadas {{
                flex: 1;
                min-width: 0;
            }}
            
            .obras-label {{
                font-size: 0.75rem;
                color: var(--warm-red-dark);
                font-weight: 600;
                display: block;
                margin-bottom: 4px;
            }}
            
            .obras-links {{
                display: flex;
                flex-wrap: wrap;
                gap: 4px;
                font-size: 0.75rem;
            }}
            
            .obra-link {{
                color: var(--warm-red);
                text-decoration: none;
                padding: 2px 6px;
                background: var(--beige-light);
                border-radius: 8px;
                border: 1px solid var(--border-color);
                transition: all 0.2s ease;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                max-width: 200px;
            }}
            
            .obra-link:hover {{
                background: var(--warm-red);
                color: white;
                transform: translateY(-1px);
                box-shadow: 0 2px 4px rgba(193, 119, 103, 0.3);
            }}
            
            .comentario-badge {{
                background: var(--beige-light);
                padding: 4px 10px;
                border-radius: 12px;
                font-size: 0.75rem;
                color: var(--warm-red-dark);
                border: 1px solid var(--border-color);
                flex-shrink: 0;
            }}
            
            .empty-comentarios {{
                background: white;
                border-radius: 10px;
                border: 2px dashed var(--border-color);
            }}
            
            /* RESPONSIVE */
            @media (max-width: 768px) {{
                .container {{
                    margin: 10px;
                    padding: 20px;
                }}
                
                .top-bar {{
                    flex-direction: column;
                    gap: 10px;
                    text-align: center;
                }}
                
                .stats {{
                    gap: 10px;
                }}
                
                .stat-item {{
                    min-width: 80px;
                    padding: 10px 15px;
                }}
                
                .nav-grid {{
                    grid-template-columns: 1fr;
                }}
                
                .main-title {{
                    font-size: 1.5rem;
                }}
                
                .comentario-header {{
                    flex-direction: column;
                    align-items: flex-start;
                    gap: 8px;
                }}
                
                .comentario-fecha {{
                    font-size: 0.7rem;
                }}
                
                .comentario-footer {{
                    flex-direction: column;
                    align-items: flex-start;
                    gap: 8px;
                }}
                
                .obras-links {{
                    flex-direction: column;
                    gap: 6px;
                }}
                
                .obra-link {{
                    max-width: 100%;
                    display: block;
                    text-align: center;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <!-- BARRA SUPERIOR MINIMALISTA -->
            <div class="top-bar">
                <a href="/" class="logo">🎭 Teatro Español</a>
                <div class="user-info">
                    {user_info}
                </div>
            </div>
            
            <!-- TÍTULO PRINCIPAL -->
            <h1 class="main-title">Siglo de Oro</h1>
            
            <!-- INFORMACIÓN DEL PROYECTO -->
            <div class="info-section">
                <div class="info-title">Base de datos de obras teatrales</div>
                <div class="info-text">
                    <strong>Versión:</strong> 1.0.0 | 
                    <strong>Fuentes:</strong> FUENTESXI (PDF) + CATCOM (Web scraping)
                </div>
            </div>

            <!-- ESTADÍSTICAS COMPACTAS -->
            <div class="stats">
                <div class="stat-item">
                    <span class="stat-number">{total_obras}</span>
                    <div class="stat-label">Obras</div>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{total_autores}</span>
                    <div class="stat-label">Autores</div>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{total_lugares}</span>
                    <div class="stat-label">Lugares</div>
                </div>
                <div class="stat-item">
                    <span class="stat-number">{total_representaciones}</span>
                    <div class="stat-label">Representaciones</div>
                </div>
            </div>

            <!-- NAVEGACIÓN PRINCIPAL -->
            <div class="nav-section">
                <h2 class="nav-title">Navegación</h2>
                <div class="nav-grid">
                    <a href="/obras/catalogo/" class="nav-link">
                        <div class="nav-link-title">📖 Catálogo General</div>
                        <div class="nav-link-desc">Ver todas las obras</div>
                    </a>
                    <a href="/obras/editor/" class="nav-link">
                        <div class="nav-link-title">✏️ Editor</div>
                        <div class="nav-link-desc">Editar obras dinámicamente</div>
                    </a>
                    <a href="/obras/catalogos/" class="nav-link">
                        <div class="nav-link-title">📚 Catálogos</div>
                        <div class="nav-link-desc">Explorar por fuente</div>
                    </a>
                    <a href="/api/obras/" class="nav-link">
                        <div class="nav-link-title">🔌 API</div>
                        <div class="nav-link-desc">Endpoints REST</div>
                    </a>
                </div>
            </div>

            <!-- COMENTARIOS DE LA COMUNIDAD -->
            {comentarios_html}

            <!-- ADMINISTRACIÓN -->
            <div class="admin-section">
                <h2 class="nav-title">Administración</h2>
                <a href="/admin/" class="admin-btn">Panel de Administración</a>
                <div class="credentials">
                    <div class="credentials-title">Credenciales:</div>
                    <div class="credentials-list">
                        Usuario: <strong>admin_teatro</strong> | Contraseña: <strong>teatro123</strong>
                    </div>
                </div>
            </div>
            
            <!-- USUARIOS DE PRUEBA -->
            <div class="admin-section">
                <h2 class="nav-title">Usuarios de Prueba</h2>
                <div class="credentials">
                    <div class="credentials-title">Credenciales de desarrollo:</div>
                    <div class="credentials-list">
                        <strong>test1</strong> / <strong>123</strong> (Usuario básico)<br>
                        <strong>investigador</strong> / <strong>abc</strong> (Investigador)<br>
                        <strong>admin</strong> / <strong>admin</strong> (Administrador)<br>
                        <strong>demo</strong> / <strong>demo</strong> (Demostración)<br>
                        <strong>ivansimo</strong> / <strong>12345678</strong> (Usuario principal)
                    </div>
                </div>
                <div class="info-text" style="margin-top: 10px; font-size: 0.8rem;">
                    💡 Puedes iniciar sesión con <strong>usuario</strong> o <strong>email</strong><br>
                    En desarrollo: contraseñas mínimas de 3 caracteres
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    from django.http import HttpResponse
    return HttpResponse(html_content)

@require_http_methods(["GET"])
def index_django_view(request):
    """Vista principal con la UI equivalente a tu index de GitHub Pages."""
    return render(request, "obras/index_django.html")

urlpatterns = [
    path("", index_django_view, name="home"),
    path("admin/", admin.site.urls),
    path("usuarios/", include("apps.usuarios.urls")),
    path("obras/", include("apps.obras.urls")),
    path("api/", include("apps.obras.urls")),
    path("api/", include("apps.representaciones.urls")),
    path("api/", include("apps.lugares.urls")),
    path("api/", include("apps.autores.urls")),
    path("api/", include("apps.bibliografia.urls")),
]

# ---- Compatibilidad UI GitHub Pages en Django ----
BASE_DIR = Path(__file__).resolve().parent.parent


@require_http_methods(["GET"])
def github_pages_index_view(request):
    """Sirve el index estático original usado en GitHub Pages."""
    # Prioridad: el frontend archivado dentro del repo (Django-only).
    file_path = BASE_DIR / "frontend" / "github-pages" / "index.html"
    if not file_path.exists():
        # Fallback por compatibilidad con setups antiguos
        file_path = BASE_DIR / "index.html"
    if not file_path.exists():
        raise Http404("index.html legacy no encontrado")
    return FileResponse(file_path.open("rb"), content_type="text/html; charset=utf-8")


@require_http_methods(["GET"])
def github_pages_datos_obras_view(request):
    """Sirve el respaldo JSON principal para el frontend estático."""
    file_path = BASE_DIR / "datos_obras.json"
    if not file_path.exists():
        raise Http404("datos_obras.json no encontrado")
    return FileResponse(file_path.open("rb"), content_type="application/json; charset=utf-8")


@require_http_methods(["GET"])
def github_pages_data_files_view(request, subpath):
    """
    Sirve archivos bajo data/ para mantener funcionalidad del index estático.
    """
    base_data_dir = (BASE_DIR / "data").resolve()
    target = (base_data_dir / subpath).resolve()
    if base_data_dir not in target.parents and target != base_data_dir:
        raise Http404("Ruta inválida")
    if not target.exists() or not target.is_file():
        raise Http404("Archivo no encontrado")
    content_type = "application/json; charset=utf-8" if target.suffix == ".json" else "text/plain; charset=utf-8"
    return FileResponse(target.open("rb"), content_type=content_type)


@require_http_methods(["GET"])
def favicon_view(request):
    """Evita 404 de favicon cuando no hay icono configurado."""
    return HttpResponse(status=204)


@require_http_methods(["GET"])
def github_pages_legacy_file_view(request, subpath):
    """
    Sirve archivos del frontend legacy bajo /legacy/.

    - Si subpath empieza por `data/`, lo mapea a `BASE_DIR/data/...` (repo root).
    - Si no, lo mapea a `BASE_DIR/frontend/github-pages/...`.
    """
    # Normalizar subpath y evitar path traversal
    subpath = str(subpath or "").lstrip("/")
    if ".." in subpath.split("/"):
        raise Http404("Ruta inválida")

    if subpath.startswith("data/"):
        target = (BASE_DIR / "data" / subpath[len("data/") :]).resolve()
        root = (BASE_DIR / "data").resolve()
    else:
        target = (BASE_DIR / "frontend" / "github-pages" / subpath).resolve()
        root = (BASE_DIR / "frontend" / "github-pages").resolve()

    if root not in target.parents and target != root:
        raise Http404("Ruta inválida")
    if not target.exists() or not target.is_file():
        raise Http404("Archivo legacy no encontrado")

    content_type, _ = mimetypes.guess_type(str(target))
    if not content_type:
        content_type = "application/octet-stream"
    return FileResponse(target.open("rb"), content_type=content_type)


# Mantener rutas legacy accesibles sin ser la portada principal
urlpatterns += [
    # Portada antigua
    path("legacy/", github_pages_index_view, name="legacy_index_root"),
    path("legacy/index.html", github_pages_index_view, name="legacy_index"),

    # Ficheros referenciados de forma relativa desde `frontend/github-pages/index.html`
    path("legacy/datos_obras.json", github_pages_datos_obras_view, name="legacy_datos_obras_json"),
    path("legacy/data/<path:subpath>", github_pages_data_files_view, name="legacy_data_files"),
    path("legacy/favicon.ico", favicon_view, name="legacy_favicon"),

    # Catch-all para otros HTML/JS/CSS dentro de frontend/github-pages
    path("legacy/<path:subpath>", github_pages_legacy_file_view, name="legacy_file"),
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)