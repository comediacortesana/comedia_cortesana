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
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def home_view(request):
    """Vista de inicio que muestra información del proyecto"""
    # Información del usuario autenticado
    user_info = ""
    if request.user.is_authenticated:
        user_info = f"""
            <div class="user-info" style="position: absolute; top: 20px; right: 20px; background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px; backdrop-filter: blur(10px);">
                <p style="margin: 0; color: white; font-weight: 500;">👋 ¡Hola, {request.user.get_full_name()}!</p>
                <p style="margin: 5px 0 0 0; color: rgba(255,255,255,0.8); font-size: 0.9em;">
                    {'🔬 Investigador' if request.user.es_investigador else '👤 Usuario'}
                    {' - ' + request.user.institucion if request.user.institucion else ''}
                </p>
                <div style="margin-top: 10px;">
                    <a href="/usuarios/perfil/" style="color: #ffd700; text-decoration: none; margin-right: 15px;">📝 Mi Perfil</a>
                    <a href="/usuarios/logout/" style="color: #ffd700; text-decoration: none;">🚪 Salir</a>
                </div>
            </div>
        """
    else:
        user_info = """
            <div class="user-info" style="position: absolute; top: 20px; right: 20px; background: rgba(255,255,255,0.2); padding: 15px; border-radius: 10px; backdrop-filter: blur(10px);">
                <p style="margin: 0; color: white; font-weight: 500;">🎭 Teatro Español</p>
                <div style="margin-top: 10px;">
                    <a href="/usuarios/login/" style="color: #ffd700; text-decoration: none; margin-right: 15px;">🔑 Iniciar Sesión</a>
                    <a href="/usuarios/registro/" style="color: #ffd700; text-decoration: none;">📝 Registrarse</a>
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
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 0; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
            }}
            .container {{ 
                max-width: 1200px; 
                margin: 0 auto; 
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            }}
            h1 {{ 
                text-align: center; 
                color: #fff; 
                margin-bottom: 30px;
                font-size: 2.5em;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }}
            .stats {{ 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                gap: 20px; 
                margin: 30px 0; 
            }}
            .stat-card {{ 
                background: rgba(255,255,255,0.2); 
                padding: 20px; 
                border-radius: 15px; 
                text-align: center;
                border: 1px solid rgba(255,255,255,0.3);
            }}
            .stat-number {{ 
                font-size: 2em; 
                font-weight: bold; 
                color: #ffd700; 
            }}
            .api-section {{ 
                margin: 30px 0; 
            }}
            .api-grid {{ 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
                gap: 15px; 
            }}
            .api-link {{ 
                display: block; 
                background: rgba(255,255,255,0.2); 
                color: white; 
                text-decoration: none; 
                padding: 15px; 
                border-radius: 10px; 
                text-align: center;
                border: 1px solid rgba(255,255,255,0.3);
                transition: all 0.3s ease;
            }}
            .api-link:hover {{ 
                background: rgba(255,255,255,0.3); 
                transform: translateY(-2px);
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            }}
            .admin-section {{ 
                text-align: center; 
                margin: 30px 0; 
            }}
            .admin-btn {{ 
                display: inline-block; 
                background: #e74c3c; 
                color: white; 
                text-decoration: none; 
                padding: 15px 30px; 
                border-radius: 25px; 
                font-weight: bold;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(231,76,60,0.3);
            }}
            .admin-btn:hover {{ 
                background: #c0392b; 
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(231,76,60,0.4);
            }}
            .info {{ 
                background: rgba(255,255,255,0.1); 
                padding: 20px; 
                border-radius: 15px; 
                margin: 20px 0;
                border-left: 4px solid #ffd700;
            }}
        </style>
    </head>
    <body>
        {user_info}
        <div class="container">
            <h1>🎭 Teatro Español del Siglo de Oro</h1>
            
            <div class="info">
                <h3>📚 Base de datos de obras teatrales, autores, lugares y representaciones</h3>
                <p><strong>Versión:</strong> 1.0.0</p>
                <p><strong>Fuentes:</strong> FUENTESXI (PDF) + CATCOM (Web scraping)</p>
            </div>

            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">2,038</div>
                    <div>Obras únicas</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">54</div>
                    <div>Autores</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">273</div>
                    <div>Lugares</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">6,175</div>
                    <div>Representaciones</div>
                </div>
            </div>

            <div class="api-section">
                <h2>🔗 Navegación</h2>
                <div class="api-grid">
                    <a href="/obras/editor/" class="api-link">
                        <strong>✏️ Editor de Catálogos</strong><br>
                        <small>Editar obras dinámicamente</small>
                    </a>
                    <a href="/obras/catalogos/" class="api-link">
                        <strong>📚 Catálogos</strong><br>
                        <small>Explorar por fuente</small>
                    </a>
                    <a href="/obras/catalogo/" class="api-link">
                        <strong>📖 Catálogo General</strong><br>
                        <small>Ver todas las obras</small>
                    </a>
                    <a href="/api/obras/" class="api-link">
                        <strong>🔌 API Obras</strong><br>
                        <small>Endpoint REST</small>
                    </a>
                    <a href="/api/autores/" class="api-link">
                        <strong>✍️ API Autores</strong><br>
                        <small>Endpoint REST</small>
                    </a>
                    <a href="/api/lugares/" class="api-link">
                        <strong>📍 API Lugares</strong><br>
                        <small>Endpoint REST</small>
                    </a>
                    <a href="/api/representaciones/" class="api-link">
                        <strong>🎪 API Representaciones</strong><br>
                        <small>Endpoint REST</small>
                    </a>
                    <a href="/api/bibliografia/" class="api-link">
                        <strong>📚 API Bibliografía</strong><br>
                        <small>Endpoint REST</small>
                    </a>
                </div>
            </div>

            <div class="admin-section">
                <h2>⚙️ Administración</h2>
                <a href="/admin/" class="admin-btn">Panel de Administración</a>
                <p><small>Usuario: <strong>admin_teatro</strong> | Contraseña: <strong>teatro123</strong></small></p>
            </div>
            
            <div class="admin-section">
                <h2>🧪 Usuarios de Prueba (Desarrollo)</h2>
                <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; margin: 20px 0;">
                    <p><strong>Credenciales de prueba:</strong></p>
                    <ul style="text-align: left; display: inline-block; color: #ffd700;">
                        <li><strong>test1</strong> / <strong>123</strong> (Usuario básico)</li>
                        <li><strong>investigador</strong> / <strong>abc</strong> (Investigador)</li>
                        <li><strong>admin</strong> / <strong>admin</strong> (Administrador)</li>
                        <li><strong>demo</strong> / <strong>demo</strong> (Demostración)</li>
                        <li><strong>ivansimo</strong> / <strong>12345678</strong> (Usuario principal)</li>
                    </ul>
                    <p><small>💡 Puedes iniciar sesión con <strong>usuario</strong> o <strong>email</strong></small></p>
                    <p><small>En desarrollo: contraseñas mínimas de 3 caracteres</small></p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    from django.http import HttpResponse
    return HttpResponse(html_content)

urlpatterns = [
    path("", home_view, name="home"),
    path("admin/", admin.site.urls),
    path("usuarios/", include("apps.usuarios.urls")),
    path("obras/", include("apps.obras.urls")),
    path("api/", include("apps.obras.urls")),
    path("api/", include("apps.representaciones.urls")),
    path("api/", include("apps.lugares.urls")),
    path("api/", include("apps.autores.urls")),
    path("api/", include("apps.bibliografia.urls")),
]

# Servir archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)