from django.contrib import admin
from .models import Representacion


@admin.register(Representacion)
class RepresentacionAdmin(admin.ModelAdmin):
    """Administración de representaciones"""
    
    list_display = [
        'obra', 'fecha_formateada', 'lugar', 'compañia', 'tipo_lugar', 'pagina_pdf', 'created_at'
    ]
    list_filter = [
        'tipo_lugar', 'tipo_funcion', 'publico', 'obra__autor', 'lugar', 
        'es_anterior_1650', 'es_anterior_1665', 'created_at'
    ]
    search_fields = [
        'fecha', 'compañia', 'director_compañia', 'observaciones', 'fuente',
        'obra__titulo_limpio', 'lugar__nombre', 'personajes_historicos', 'organizadores_fiesta'
    ]
    readonly_fields = ['created_at', 'updated_at', 'siglo', 'decada']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('obra', 'fecha', 'fecha_formateada')
        }),
        ('Lugar y espacio', {
            'fields': ('lugar', 'tipo_lugar')
        }),
        ('Compañía y dirección', {
            'fields': ('compañia', 'director_compañia')
        }),
        ('Detalles de la función', {
            'fields': ('tipo_funcion', 'publico', 'entrada', 'duracion'),
            'classes': ('collapse',)
        }),
        ('Personajes y organizadores', {
            'fields': ('personajes_historicos', 'organizadores_fiesta'),
            'classes': ('collapse',)
        }),
        ('Época', {
            'fields': ('es_anterior_1650', 'es_anterior_1665'),
            'classes': ('collapse',)
        }),
        ('Información adicional', {
            'fields': ('fuente', 'observaciones', 'mecenas', 'gestor_administrativo', 'notas'),
            'classes': ('collapse',)
        }),
        ('Referencia PDF', {
            'fields': ('pagina_pdf', 'texto_original_pdf'),
            'classes': ('collapse',)
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at', 'siglo', 'decada'),
            'classes': ('collapse',)
        }),
    )