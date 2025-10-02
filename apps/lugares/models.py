from django.db import models
from django.utils import timezone


class Lugar(models.Model):
    """Modelo para lugares geográficos donde se representaron obras teatrales"""
    
    TIPO_LUGAR_CHOICES = [
        ('palacio', 'Palacio'),
        ('corral', 'Corral de comedias'),
        ('iglesia', 'Iglesia'),
        ('plaza', 'Plaza pública'),
        ('teatro', 'Teatro'),
        ('casa', 'Casa particular'),
        ('universidad', 'Universidad'),
        ('convento', 'Convento'),
        ('otro', 'Otro'),
    ]
    
    nombre = models.CharField(
        max_length=200, 
        help_text="Nombre del lugar"
    )
    coordenadas_lat = models.FloatField(
        null=True, 
        blank=True, 
        help_text="Latitud"
    )
    coordenadas_lng = models.FloatField(
        null=True, 
        blank=True, 
        help_text="Longitud"
    )
    region = models.CharField(
        max_length=200, 
        blank=True, 
        help_text="Región o provincia"
    )
    pais = models.CharField(
        max_length=100, 
        default='España',
        help_text="País"
    )
    tipo_lugar = models.CharField(
        max_length=100,
        choices=TIPO_LUGAR_CHOICES,
        help_text="Tipo de lugar"
    )
    descripcion = models.TextField(
        blank=True, 
        help_text="Descripción del lugar"
    )
    poblacion_estimada = models.IntegerField(
        null=True, 
        blank=True, 
        help_text="Población estimada en el siglo XVII"
    )
    es_capital = models.BooleanField(
        default=False, 
        help_text="Si es capital de región o país"
    )
    notas_historicas = models.TextField(
        blank=True, 
        help_text="Notas históricas sobre el lugar"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'lugares'
        verbose_name = "Lugar"
        verbose_name_plural = "Lugares"
        ordering = ['nombre']
        unique_together = ['nombre', 'region']

    def __str__(self):
        if self.region:
            return f"{self.nombre}, {self.region}"
        return self.nombre

    @property
    def total_representaciones(self):
        """Retorna el número total de representaciones en este lugar"""
        return self.representaciones.count()

    @property
    def coordenadas(self):
        """Retorna las coordenadas como tupla"""
        if self.coordenadas_lat and self.coordenadas_lng:
            return (self.coordenadas_lat, self.coordenadas_lng)
        return None

    def save(self, *args, **kwargs):
        # Normalizar el nombre del lugar
        self.nombre = self.nombre.strip().title()
        super().save(*args, **kwargs)