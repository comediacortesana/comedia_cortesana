from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import ReferenciaBibliografica
from .serializers import ReferenciaBibliograficaSerializer


class ReferenciaBibliograficaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para referencias bibliográficas de obras teatrales.
    
    Permite listar, crear, actualizar y eliminar referencias bibliográficas.
    Incluye filtros por obra, tipo de referencia, autor, etc.
    """
    queryset = ReferenciaBibliografica.objects.all()
    serializer_class = ReferenciaBibliograficaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'obra', 'tipo_referencia', 'año_publicacion', 'editorial'
    ]
    search_fields = [
        'titulo', 'autor', 'editor', 'lugar_publicacion', 'revista', 'editorial'
    ]
    ordering_fields = [
        'autor', 'año_publicacion', 'titulo', 'created_at'
    ]
    ordering = ['autor', 'año_publicacion']