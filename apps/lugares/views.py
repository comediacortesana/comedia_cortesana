from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Lugar
from .serializers import LugarSerializer


class LugarViewSet(viewsets.ModelViewSet):
    """
    ViewSet para lugares geográficos donde se representaron obras teatrales.
    
    Permite listar, crear, actualizar y eliminar lugares.
    Incluye filtros por tipo de lugar, región, país, etc.
    """
    queryset = Lugar.objects.all()
    serializer_class = LugarSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo_lugar', 'region', 'pais', 'es_capital']
    search_fields = ['nombre', 'region', 'descripcion']
    ordering_fields = ['nombre', 'region', 'created_at']
    ordering = ['nombre']