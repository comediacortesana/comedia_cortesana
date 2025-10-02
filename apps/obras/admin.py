from django.contrib import admin
from .models import Obra, Manuscrito, PaginaPDF, TemaLiterario, ObraTema, ComentarioUsuario


@admin.register(Obra)
class ObraAdmin(admin.ModelAdmin):
    """Administración de obras teatrales"""
    
    list_display = [
        'titulo_limpio', 'autor', 'tipo_obra', 'fuente_principal', 'origen_datos',
        'pagina_pdf', 'total_representaciones', 'created_at'
    ]
    list_filter = [
        'tipo_obra', 'fuente_principal', 'origen_datos', 'genero', 'musica_conservada',
        'autor', 'created_at'
    ]
    search_fields = [
        'titulo', 'titulo_limpio', 'titulo_alternativo', 'tema', 'compositor',
        'bibliotecas_musica', 'bibliografia_musica', 'manuscritos_conocidos', 'ediciones_conocidas'
    ]
    readonly_fields = ['created_at', 'updated_at', 'total_representaciones']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('titulo', 'titulo_limpio', 'titulo_alternativo', 'autor')
        }),
        ('Clasificación', {
            'fields': ('tipo_obra', 'genero', 'tema', 'idioma')
        }),
        ('Detalles técnicos', {
            'fields': ('versos', 'actos', 'fecha_creacion_estimada')
        }),
        ('Música', {
            'fields': ('musica_conservada', 'compositor', 'bibliotecas_musica', 'bibliografia_musica'),
            'classes': ('collapse',)
        }),
        ('Historia textual', {
            'fields': ('manuscritos_conocidos', 'ediciones_conocidas'),
            'classes': ('collapse',)
        }),
        ('Información adicional', {
            'fields': ('edicion_principe', 'notas_bibliograficas', 'mecenas', 'notas'),
            'classes': ('collapse',)
        }),
        ('Fuente de datos', {
            'fields': ('fuente_principal', 'origen_datos', 'pagina_pdf', 'texto_original_pdf'),
            'classes': ('collapse',)
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Manuscrito)
class ManuscritoAdmin(admin.ModelAdmin):
    """Administración de manuscritos"""
    
    list_display = [
        'obra', 'biblioteca', 'signatura', 'fecha_manuscrito', 'created_at'
    ]
    list_filter = [
        'biblioteca', 'obra__autor', 'created_at'
    ]
    search_fields = [
        'biblioteca', 'signatura', 'descripcion', 'obra__titulo_limpio'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('obra', 'biblioteca', 'signatura')
        }),
        ('Detalles', {
            'fields': ('fecha_manuscrito', 'descripcion')
        }),
        ('Metadatos', {
            'fields': ('notas', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PaginaPDF)
class PaginaPDFAdmin(admin.ModelAdmin):
    """Administración de páginas PDF"""
    
    list_display = [
        'numero_pagina', 'part_file', 'archivo_imagen', 'created_at'
    ]
    list_filter = [
        'part_file', 'created_at'
    ]
    search_fields = [
        'numero_pagina', 'texto_extraido', 'part_file'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('numero_pagina', 'part_file', 'archivo_imagen')
        }),
        ('Contenido', {
            'fields': ('texto_extraido',)
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TemaLiterario)
class TemaLiterarioAdmin(admin.ModelAdmin):
    """Administración de temas literarios"""
    
    list_display = [
        'nombre', 'descripcion', 'created_at'
    ]
    list_filter = [
        'created_at'
    ]
    search_fields = [
        'nombre', 'descripcion'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'descripcion')
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ObraTema)
class ObraTemaAdmin(admin.ModelAdmin):
    """Administración de relaciones obra-tema"""
    
    list_display = [
        'obra', 'tema', 'es_principal', 'created_at'
    ]
    list_filter = [
        'es_principal', 'created_at'
    ]
    search_fields = [
        'obra__titulo_limpio', 'tema__nombre', 'notas'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Relación', {
            'fields': ('obra', 'tema', 'es_principal')
        }),
        ('Detalles', {
            'fields': ('notas',)
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ComentarioUsuario)
class ComentarioUsuarioAdmin(admin.ModelAdmin):
    """Administración de comentarios de usuario"""
    
    list_display = [
        'usuario', 'titulo', 'catalogo', 'numero_obras', 'fecha_creacion', 'es_publico'
    ]
    list_filter = [
        'catalogo', 'es_publico', 'fecha_creacion'
    ]
    search_fields = [
        'usuario__username', 'titulo', 'comentario'
    ]
    readonly_fields = ['fecha_creacion', 'fecha_modificacion', 'numero_obras']
    filter_horizontal = ['obras_seleccionadas']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('usuario', 'catalogo', 'titulo')
        }),
        ('Contenido', {
            'fields': ('comentario',)
        }),
        ('Obras seleccionadas', {
            'fields': ('obras_seleccionadas',)
        }),
        ('Configuración', {
            'fields': ('es_publico',)
        }),
        ('Metadatos', {
            'fields': ('numero_obras', 'fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )