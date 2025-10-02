from django.contrib import admin
from .models import ReferenciaBibliografica


@admin.register(ReferenciaBibliografica)
class ReferenciaBibliograficaAdmin(admin.ModelAdmin):
    """Administración de referencias bibliográficas"""
    
    list_display = [
        'titulo', 'autor', 'año_publicacion', 'tipo_referencia', 'obra', 'created_at'
    ]
    list_filter = [
        'tipo_referencia', 'año_publicacion', 'editorial', 'obra__autor', 'created_at'
    ]
    search_fields = [
        'titulo', 'autor', 'editor', 'lugar_publicacion', 'revista', 'editorial',
        'obra__titulo_limpio'
    ]
    readonly_fields = ['created_at', 'updated_at', 'cita_completa']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('obra', 'titulo', 'autor', 'editor')
        }),
        ('Publicación', {
            'fields': ('tipo_referencia', 'lugar_publicacion', 'año_publicacion', 'editorial')
        }),
        ('Detalles de la publicación', {
            'fields': ('volumen', 'numero', 'revista', 'coleccion', 'paginas'),
            'classes': ('collapse',)
        }),
        ('Identificadores', {
            'fields': ('isbn', 'issn', 'doi', 'url'),
            'classes': ('collapse',)
        }),
        ('Información adicional', {
            'fields': ('notas', 'cita_completa'),
            'classes': ('collapse',)
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )