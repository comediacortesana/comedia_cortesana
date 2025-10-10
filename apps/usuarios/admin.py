from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import Usuario, PerfilUsuario, SesionUsuario


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    """
    Administración personalizada para el modelo Usuario
    """
    list_display = ('email', 'username', 'get_full_name', 'es_investigador', 'institucion', 'is_active', 'fecha_registro')
    list_filter = ('es_investigador', 'is_active', 'is_staff', 'fecha_registro', 'institucion')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'institucion')
    ordering = ('-fecha_registro',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'email', 'avatar')}),
        ('Información profesional', {'fields': ('es_investigador', 'institucion', 'biografia')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Configuración', {'fields': ('notificaciones_email', 'tema_oscuro')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined', 'fecha_registro')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'es_investigador', 'institucion'),
        }),
    )
    
    readonly_fields = ('fecha_registro', 'date_joined', 'last_login')
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Nombre completo'


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    """
    Administración para el modelo PerfilUsuario
    """
    list_display = ('usuario', 'perfil_publico', 'fecha_actualizacion')
    list_filter = ('perfil_publico', 'mostrar_email', 'mostrar_institucion', 'fecha_actualizacion')
    search_fields = ('usuario__username', 'usuario__email', 'usuario__first_name', 'usuario__last_name')
    readonly_fields = ('fecha_actualizacion',)
    
    fieldsets = (
        ('Usuario', {'fields': ('usuario',)}),
        ('Información profesional', {'fields': ('especialidades', 'intereses', 'publicaciones')}),
        ('Redes sociales', {'fields': ('redes_sociales',)}),
        ('Configuración de privacidad', {'fields': ('perfil_publico', 'mostrar_email', 'mostrar_institucion')}),
        ('Fechas', {'fields': ('fecha_actualizacion',)}),
    )


@admin.register(SesionUsuario)
class SesionUsuarioAdmin(admin.ModelAdmin):
    """
    Administración para el modelo SesionUsuario
    """
    list_display = ('usuario', 'ip_address', 'fecha_inicio', 'fecha_ultima_actividad', 'activa')
    list_filter = ('activa', 'fecha_inicio', 'fecha_ultima_actividad')
    search_fields = ('usuario__username', 'usuario__email', 'ip_address')
    readonly_fields = ('fecha_inicio', 'fecha_ultima_actividad')
    ordering = ('-fecha_inicio',)
    
    fieldsets = (
        ('Información de sesión', {'fields': ('usuario', 'ip_address', 'user_agent')}),
        ('Estado', {'fields': ('activa',)}),
        ('Fechas', {'fields': ('fecha_inicio', 'fecha_ultima_actividad')}),
    )
    
    def has_add_permission(self, request):
        # No permitir agregar sesiones manualmente
        return False


