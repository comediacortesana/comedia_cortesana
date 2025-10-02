from django.db import models
from django.utils import timezone
from datetime import datetime


class Representacion(models.Model):
    """Modelo para representaciones teatrales"""
    
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
    
    obra = models.ForeignKey(
        'obras.Obra',
        on_delete=models.CASCADE,
        related_name='representaciones',
        help_text="Obra representada"
    )
    fecha = models.CharField(
        max_length=50,
        help_text="Fecha original del texto"
    )
    fecha_formateada = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha formateada para consultas"
    )
    compañia = models.CharField(
        max_length=200,
        blank=True,
        help_text="Compañía teatral"
    )
    lugar = models.ForeignKey(
        'lugares.Lugar',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='representaciones',
        help_text="Lugar de la representación"
    )
    tipo_lugar = models.CharField(
        max_length=100,
        choices=TIPO_LUGAR_CHOICES,
        blank=True,
        help_text="Tipo de lugar de representación"
    )
    director_compañia = models.CharField(
        max_length=200,
        blank=True,
        help_text="Director de la compañía"
    )
    fuente = models.CharField(
        max_length=200,
        blank=True,
        help_text="Fuente de la información"
    )
    observaciones = models.TextField(
        blank=True,
        help_text="Observaciones sobre la representación"
    )
    mecenas = models.CharField(
        max_length=200,
        blank=True,
        help_text="Mecenas o patrocinador"
    )
    gestor_administrativo = models.CharField(
        max_length=200,
        blank=True,
        help_text="Gestor administrativo"
    )
    # Personajes históricos y cargos
    personajes_historicos = models.TextField(
        blank=True,
        help_text="Menciones de personajes históricos o cargos (nobles, embajadores, etc.)"
    )
    organizadores_fiesta = models.TextField(
        blank=True,
        help_text="Nombres propios o títulos de organizadores (Heliche, gremios, etc.)"
    )
    # Época de la representación
    es_anterior_1650 = models.BooleanField(
        default=False,
        help_text="Si la representación es anterior a 1650"
    )
    es_anterior_1665 = models.BooleanField(
        default=False,
        help_text="Si la representación es anterior a 1665"
    )
    tipo_funcion = models.CharField(
        max_length=100,
        blank=True,
        help_text="Tipo de función (fiesta, celebración, etc.)"
    )
    publico = models.CharField(
        max_length=100,
        blank=True,
        help_text="Tipo de público (corte, pueblo, etc.)"
    )
    entrada = models.CharField(
        max_length=100,
        blank=True,
        help_text="Información sobre entrada o precio"
    )
    duracion = models.CharField(
        max_length=100,
        blank=True,
        help_text="Duración de la representación"
    )
    notas = models.TextField(
        blank=True,
        help_text="Notas adicionales"
    )
    pagina_pdf = models.IntegerField(
        null=True,
        blank=True,
        help_text="Número de página del PDF donde aparece esta representación"
    )
    texto_original_pdf = models.TextField(
        blank=True,
        help_text="Texto original extraído del PDF para esta representación"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'representaciones'
        verbose_name = "Representación"
        verbose_name_plural = "Representaciones"
        ordering = ['-fecha_formateada', 'obra__titulo_limpio']

    def __str__(self):
        fecha_str = self.fecha_formateada.strftime('%d/%m/%Y') if self.fecha_formateada else self.fecha
        lugar_str = f" en {self.lugar.nombre}" if self.lugar else ""
        return f"{self.obra.titulo_limpio} - {fecha_str}{lugar_str}"

    @property
    def siglo(self):
        """Retorna el siglo de la representación"""
        if self.fecha_formateada:
            year = self.fecha_formateada.year
            if 1600 <= year < 1700:
                return "XVII"
            elif 1500 <= year < 1600:
                return "XVI"
            elif 1700 <= year < 1800:
                return "XVIII"
        return None

    @property
    def decada(self):
        """Retorna la década de la representación"""
        if self.fecha_formateada:
            year = self.fecha_formateada.year
            return f"{year//10*10}s"
        return None

    def save(self, *args, **kwargs):
        # Intentar parsear la fecha si no está formateada
        if not self.fecha_formateada and self.fecha:
            try:
                # Formato DD/MM/YYYY
                if '/' in self.fecha:
                    parts = self.fecha.split('/')
                    if len(parts) == 3:
                        day, month, year = parts
                        self.fecha_formateada = datetime.strptime(f"{day}/{month}/{year}", "%d/%m/%Y").date()
                # Formato YYYY-MM-DD
                elif '-' in self.fecha:
                    self.fecha_formateada = datetime.strptime(self.fecha, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                pass
        
        # Calcular automáticamente los campos de época
        if self.fecha_formateada:
            year = self.fecha_formateada.year
            self.es_anterior_1650 = year < 1650
            self.es_anterior_1665 = year < 1665
        
        super().save(*args, **kwargs)