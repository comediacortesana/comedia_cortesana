from django.db import models
from django.utils import timezone


class ReferenciaBibliografica(models.Model):
    """Modelo para referencias bibliográficas de obras teatrales"""
    
    TIPO_REFERENCIA_CHOICES = [
        ('libro', 'Libro'),
        ('articulo', 'Artículo'),
        ('tesis', 'Tesis'),
        ('manuscrito', 'Manuscrito'),
        ('edicion', 'Edición'),
        ('catalogo', 'Catálogo'),
        ('base_datos', 'Base de datos'),
        ('web', 'Recurso web'),
        ('otro', 'Otro'),
    ]
    
    obra = models.ForeignKey(
        'obras.Obra',
        on_delete=models.CASCADE,
        related_name='referencias_bibliograficas',
        help_text="Obra a la que se refiere"
    )
    titulo = models.CharField(
        max_length=500,
        help_text="Título de la referencia"
    )
    autor = models.CharField(
        max_length=300,
        blank=True,
        help_text="Autor de la referencia"
    )
    editor = models.CharField(
        max_length=300,
        blank=True,
        help_text="Editor o compilador"
    )
    lugar_publicacion = models.CharField(
        max_length=200,
        blank=True,
        help_text="Lugar de publicación"
    )
    año_publicacion = models.CharField(
        max_length=50,
        blank=True,
        help_text="Año de publicación"
    )
    paginas = models.CharField(
        max_length=100,
        blank=True,
        help_text="Páginas o rango de páginas"
    )
    tipo_referencia = models.CharField(
        max_length=100,
        choices=TIPO_REFERENCIA_CHOICES,
        help_text="Tipo de referencia"
    )
    url = models.URLField(
        blank=True,
        help_text="URL si es un recurso web"
    )
    isbn = models.CharField(
        max_length=20,
        blank=True,
        help_text="ISBN si es un libro"
    )
    issn = models.CharField(
        max_length=20,
        blank=True,
        help_text="ISSN si es una revista"
    )
    doi = models.CharField(
        max_length=100,
        blank=True,
        help_text="DOI si está disponible"
    )
    volumen = models.CharField(
        max_length=50,
        blank=True,
        help_text="Volumen o tomo"
    )
    numero = models.CharField(
        max_length=50,
        blank=True,
        help_text="Número de revista o publicación"
    )
    revista = models.CharField(
        max_length=200,
        blank=True,
        help_text="Nombre de la revista"
    )
    editorial = models.CharField(
        max_length=200,
        blank=True,
        help_text="Editorial"
    )
    coleccion = models.CharField(
        max_length=200,
        blank=True,
        help_text="Colección o serie"
    )
    notas = models.TextField(
        blank=True,
        help_text="Notas adicionales"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'bibliografia'
        verbose_name = "Referencia Bibliográfica"
        verbose_name_plural = "Referencias Bibliográficas"
        ordering = ['autor', 'año_publicacion']

    def __str__(self):
        if self.autor:
            return f"{self.autor}: {self.titulo}"
        return self.titulo

    @property
    def cita_completa(self):
        """Retorna la cita bibliográfica completa"""
        parts = []
        
        if self.autor:
            parts.append(self.autor)
        
        if self.titulo:
            parts.append(f'"{self.titulo}"')
        
        if self.revista:
            parts.append(f"en {self.revista}")
        
        if self.volumen:
            parts.append(f"vol. {self.volumen}")
        
        if self.numero:
            parts.append(f"núm. {self.numero}")
        
        if self.lugar_publicacion:
            parts.append(self.lugar_publicacion)
        
        if self.editorial:
            parts.append(self.editorial)
        
        if self.año_publicacion:
            parts.append(self.año_publicacion)
        
        if self.paginas:
            parts.append(f"pp. {self.paginas}")
        
        return ", ".join(parts)

    def save(self, *args, **kwargs):
        # Normalizar campos de texto
        if self.autor:
            self.autor = self.autor.strip()
        if self.titulo:
            self.titulo = self.titulo.strip()
        super().save(*args, **kwargs)