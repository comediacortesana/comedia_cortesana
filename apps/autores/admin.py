from django.contrib import admin
from .models import Autor


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    """Administración de autores"""
    
    list_display = [
        'nombre', 'epoca', 'total_obras', 'total_representaciones', 'created_at'
    ]
    list_filter = [
        'epoca', 'created_at'
    ]
    search_fields = [
        'nombre', 'nombre_completo', 'biografia', 'obras_principales'
    ]
    readonly_fields = ['created_at', 'updated_at', 'total_obras', 'total_representaciones']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'nombre_completo')
        }),
        ('Datos biográficos', {
            'fields': ('fecha_nacimiento', 'fecha_muerte', 'epoca')
        }),
        ('Información adicional', {
            'fields': ('biografia', 'obras_principales', 'notas'),
            'classes': ('collapse',)
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at', 'total_obras', 'total_representaciones'),
            'classes': ('collapse',)
        }),
    )