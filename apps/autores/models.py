from django.db import models
from django.utils import timezone


class Autor(models.Model):
    """Modelo para autores/dramaturgos del teatro español del Siglo de Oro"""
    
    nombre = models.CharField(max_length=200, help_text="Nombre del autor")
    nombre_completo = models.CharField(
        max_length=300, 
        blank=True, 
        help_text="Nombre completo del autor"
    )
    fecha_nacimiento = models.CharField(
        max_length=50, 
        blank=True, 
        help_text="Fecha de nacimiento (formato original)"
    )
    fecha_muerte = models.CharField(
        max_length=50, 
        blank=True, 
        help_text="Fecha de muerte (formato original)"
    )
    biografia = models.TextField(
        blank=True, 
        help_text="Biografía del autor"
    )
    obras_principales = models.TextField(
        blank=True, 
        help_text="Lista de obras principales"
    )
    epoca = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="Época histórica (ej: Siglo de Oro)"
    )
    notas = models.TextField(
        blank=True, 
        help_text="Notas adicionales sobre el autor"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'autores'
        verbose_name = "Autor"
        verbose_name_plural = "Autores"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    @property
    def total_obras(self):
        """Retorna el número total de obras del autor"""
        return self.obras.count()

    @property
    def total_representaciones(self):
        """Retorna el número total de representaciones de sus obras"""
        return sum(obra.representaciones.count() for obra in self.obras.all())