from django.contrib import admin
from .models import Lugar


@admin.register(Lugar)
class LugarAdmin(admin.ModelAdmin):
    """Administración de lugares"""
    
    list_display = [
        'nombre', 'region', 'pais', 'tipo_lugar', 'total_representaciones', 'created_at'
    ]
    list_filter = [
        'tipo_lugar', 'region', 'pais', 'es_capital', 'created_at'
    ]
    search_fields = [
        'nombre', 'region', 'descripcion', 'notas_historicas'
    ]
    readonly_fields = ['created_at', 'updated_at', 'total_representaciones', 'coordenadas']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'region', 'pais')
        }),
        ('Clasificación', {
            'fields': ('tipo_lugar', 'es_capital')
        }),
        ('Coordenadas', {
            'fields': ('coordenadas_lat', 'coordenadas_lng'),
            'classes': ('collapse',)
        }),
        ('Información histórica', {
            'fields': ('poblacion_estimada', 'descripcion', 'notas_historicas'),
            'classes': ('collapse',)
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at', 'total_representaciones', 'coordenadas'),
            'classes': ('collapse',)
        }),
    )