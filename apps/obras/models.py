from django.db import models
from django.utils import timezone


class Obra(models.Model):
    """Modelo principal para obras teatrales del Siglo de Oro español"""
    
    TIPO_OBRA_CHOICES = [
        ('comedia', 'Comedia'),
        ('auto', 'Auto sacramental'),
        ('zarzuela', 'Zarzuela'),
        ('entremes', 'Entremés'),
        ('tragedia', 'Tragedia'),
        ('loa', 'Loa'),
        ('sainete', 'Sainete'),
        ('baile', 'Baile'),
        ('otro', 'Otro'),
    ]
    
    FUENTE_CHOICES = [
        ('FUENTESXI', 'FUENTES XI (Varey & Shergold)'),
        ('CATCOM', 'CATCOM (Base de datos web)'),
        ('AMBAS', 'Ambas fuentes'),
    ]
    
    ORIGEN_DATOS_CHOICES = [
        ('web', 'Web'),
        ('pdf', 'PDF'),
        ('manual', 'Manual'),
    ]
    
    titulo = models.CharField(
        max_length=500, 
        help_text="Título original de la obra"
    )
    titulo_limpio = models.CharField(
        max_length=500, 
        unique=True,
        help_text="Título normalizado y limpio"
    )
    titulo_alternativo = models.CharField(
        max_length=500, 
        blank=True, 
        help_text="Títulos alternativos o variaciones"
    )
    autor = models.ForeignKey(
        'autores.Autor', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='obras',
        help_text="Autor de la obra"
    )
    tipo_obra = models.CharField(
        max_length=100,
        choices=TIPO_OBRA_CHOICES,
        help_text="Tipo de obra teatral"
    )
    genero = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Género específico"
    )
    edicion_principe = models.TextField(
        blank=True, 
        help_text="Información sobre la edición príncipe"
    )
    notas_bibliograficas = models.TextField(
        blank=True, 
        help_text="Notas bibliográficas"
    )
    fuente_principal = models.CharField(
        max_length=50,
        choices=FUENTE_CHOICES,
        help_text="Fuente principal de los datos"
    )
    origen_datos = models.CharField(
        max_length=20,
        choices=ORIGEN_DATOS_CHOICES,
        default='web',
        help_text="Origen de los datos (web, pdf, manual)"
    )
    pagina_pdf = models.IntegerField(
        null=True,
        blank=True,
        help_text="Número de página del PDF donde aparece la información"
    )
    texto_original_pdf = models.TextField(
        blank=True,
        help_text="Texto original extraído del PDF para esta obra"
    )
    tema = models.CharField(
        max_length=200, 
        blank=True, 
        help_text="Tema principal de la obra"
    )
    musica_conservada = models.BooleanField(
        default=False, 
        help_text="Si se conserva música de la obra"
    )
    compositor = models.CharField(
        max_length=200, 
        blank=True, 
        help_text="Compositor de la música"
    )
    bibliotecas_musica = models.TextField(
        blank=True, 
        help_text="Bibliotecas donde se conserva la música"
    )
    bibliografia_musica = models.TextField(
        blank=True, 
        help_text="Bibliografía sobre la música"
    )
    mecenas = models.CharField(
        max_length=200, 
        blank=True, 
        help_text="Mecenas o patrocinador"
    )
    fecha_creacion_estimada = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Fecha estimada de creación"
    )
    idioma = models.CharField(
        max_length=50, 
        default='español', 
        help_text="Idioma de la obra"
    )
    versos = models.IntegerField(
        null=True, 
        blank=True, 
        help_text="Número de versos"
    )
    actos = models.IntegerField(
        null=True, 
        blank=True, 
        help_text="Número de actos"
    )
    notas = models.TextField(
        blank=True, 
        help_text="Notas adicionales"
    )
    manuscritos_conocidos = models.TextField(
        blank=True, 
        help_text="Manuscritos conocidos"
    )
    ediciones_conocidas = models.TextField(
        blank=True, 
        help_text="Ediciones conocidas"
    )
    observaciones = models.TextField(
        blank=True, 
        help_text="Observaciones generales"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'obras'
        verbose_name = "Obra"
        verbose_name_plural = "Obras"
        ordering = ['titulo_limpio']

    def __str__(self):
        return self.titulo_limpio or self.titulo

    @property
    def total_representaciones(self):
        """Retorna el número total de representaciones de esta obra"""
        return self.representaciones.count()

    @property
    def primera_representacion(self):
        """Retorna la fecha de la primera representación"""
        primera = self.representaciones.order_by('fecha').first()
        return primera.fecha if primera else None

    @property
    def ultima_representacion(self):
        """Retorna la fecha de la última representación"""
        ultima = self.representaciones.order_by('-fecha').first()
        return ultima.fecha if ultima else None

    @property
    def lugares_representacion(self):
        """Retorna la lista de lugares donde se ha representado"""
        lugares = self.representaciones.values_list('lugar__nombre', flat=True).distinct()
        return list(lugares)


class Manuscrito(models.Model):
    """Modelo para manuscritos de obras"""
    
    obra = models.ForeignKey(
        Obra, 
        on_delete=models.CASCADE, 
        related_name='manuscritos',
        help_text="Obra a la que pertenece el manuscrito"
    )
    biblioteca = models.CharField(
        max_length=200, 
        default='',
        help_text="Biblioteca donde se conserva"
    )
    signatura = models.CharField(
        max_length=100, 
        help_text="Signatura del manuscrito"
    )
    fecha_manuscrito = models.CharField(
        max_length=50, 
        blank=True, 
        help_text="Fecha del manuscrito"
    )
    descripcion = models.TextField(
        blank=True, 
        help_text="Descripción del manuscrito"
    )
    notas = models.TextField(
        blank=True, 
        help_text="Notas adicionales"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'obras'
        verbose_name = "Manuscrito"
        verbose_name_plural = "Manuscritos"
        ordering = ['biblioteca', 'signatura']

    def __str__(self):
        return f"{self.obra.titulo_limpio} - {self.biblioteca} ({self.signatura})"


class TemaLiterario(models.Model):
    """Modelo para temas literarios"""
    
    nombre = models.CharField(
        max_length=200, 
        unique=True,
        help_text="Nombre del tema literario"
    )
    descripcion = models.TextField(
        blank=True, 
        help_text="Descripción del tema"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'obras'
        verbose_name = "Tema Literario"
        verbose_name_plural = "Temas Literarios"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class ObraTema(models.Model):
    """Modelo de relación entre obras y temas literarios"""
    
    obra = models.ForeignKey(
        Obra, 
        on_delete=models.CASCADE,
        related_name='obratema_set'
    )
    tema = models.ForeignKey(
        TemaLiterario, 
        on_delete=models.CASCADE,
        related_name='obras'
    )
    es_principal = models.BooleanField(
        default=False,
        help_text="Si es el tema principal de la obra"
    )
    notas = models.TextField(
        blank=True,
        help_text="Notas sobre la relación obra-tema"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'obras'
        verbose_name = "Obra-Tema"
        verbose_name_plural = "Obras-Temas"
        unique_together = ['obra', 'tema']
        ordering = ['-es_principal', 'tema__nombre']

    def __str__(self):
        return f"{self.obra.titulo_limpio} - {self.tema.nombre}"


class PaginaPDF(models.Model):
    """Modelo para gestionar las páginas del PDF FUENTES IX 1"""
    
    numero_pagina = models.IntegerField(
        unique=True,
        help_text="Número de página en el PDF"
    )
    texto_extraido = models.TextField(
        blank=True,
        help_text="Texto extraído de esta página"
    )
    archivo_imagen = models.CharField(
        max_length=500,
        blank=True,
        help_text="Ruta al archivo de imagen de la página"
    )
    part_file = models.CharField(
        max_length=100,
        blank=True,
        help_text="Archivo de texto del que proviene (ej: part_001)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'obras'
        verbose_name = "Página PDF"
        verbose_name_plural = "Páginas PDF"
        ordering = ['numero_pagina']

    def __str__(self):
        return f"Página {self.numero_pagina}"

    @property
    def ruta_imagen_completa(self):
        """Retorna la ruta completa a la imagen de la página"""
        if self.archivo_imagen:
            return f"/media/pdf_pages/{self.archivo_imagen}"
        return None


class ComentarioUsuario(models.Model):
    """Modelo para comentarios de usuario sobre selecciones de obras"""
    
    usuario = models.ForeignKey(
        'usuarios.Usuario', 
        on_delete=models.CASCADE,
        related_name='comentarios',
        help_text="Usuario que hizo el comentario"
    )
    catalogo = models.CharField(
        max_length=50,
        choices=[
            ('fuentesxi', 'FUENTES XI'),
            ('catcom', 'CATCOM'),
        ],
        help_text="Catálogo al que pertenece la selección"
    )
    obras_seleccionadas = models.ManyToManyField(
        Obra,
        related_name='comentarios_usuario',
        help_text="Obras seleccionadas para el comentario"
    )
    titulo = models.CharField(
        max_length=200,
        help_text="Título del comentario"
    )
    comentario = models.TextField(
        help_text="Contenido del comentario"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha de creación del comentario"
    )
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        help_text="Fecha de última modificación"
    )
    es_publico = models.BooleanField(
        default=False,
        help_text="Si el comentario es visible para otros usuarios"
    )

    class Meta:
        app_label = 'obras'
        verbose_name = "Comentario de Usuario"
        verbose_name_plural = "Comentarios de Usuario"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.usuario.username} - {self.titulo} ({self.catalogo})"

    @property
    def numero_obras(self):
        """Retorna el número de obras seleccionadas"""
        return self.obras_seleccionadas.count()

    @property
    def obras_titulos(self):
        """Retorna una lista de títulos de las obras seleccionadas"""
        return [obra.titulo_limpio for obra in self.obras_seleccionadas.all()]