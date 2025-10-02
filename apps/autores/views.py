from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Autor
from .serializers import AutorSerializer


class AutorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para autores/dramaturgos del Siglo de Oro español.
    
    Permite listar, crear, actualizar y eliminar autores.
    Incluye filtros por época, nombre, etc.
    """
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['epoca']
    search_fields = ['nombre', 'nombre_completo', 'biografia']
    ordering_fields = ['nombre', 'created_at']
    ordering = ['nombre']