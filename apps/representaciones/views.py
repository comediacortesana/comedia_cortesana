from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Representacion
from .serializers import RepresentacionSerializer


class RepresentacionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para representaciones teatrales.
    
    Permite listar, crear, actualizar y eliminar representaciones.
    Incluye filtros por obra, lugar, fecha, compañía, etc.
    """
    queryset = Representacion.objects.all()
    serializer_class = RepresentacionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'obra', 'lugar', 'tipo_lugar', 'compañia', 'director_compañia', 'tipo_funcion', 
        'mecenas', 'gestor_administrativo', 'es_anterior_1650', 'es_anterior_1665'
    ]
    search_fields = [
        'fecha', 'compañia', 'director_compañia', 'observaciones', 'fuente', 
        'mecenas', 'gestor_administrativo', 'personajes_historicos', 'organizadores_fiesta'
    ]
    ordering_fields = [
        'fecha_formateada', 'fecha', 'created_at'
    ]
    ordering = ['-fecha_formateada', 'obra__titulo_limpio']